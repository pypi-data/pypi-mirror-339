import inspect
import textwrap
import warnings
import time

warnings.filterwarnings("ignore", category=DeprecationWarning)
from typing import Union

from dataheroes.data.common import DataParams
from dataheroes.services.common import CoresetParamsDTC, CoresetParams, PreprocessingStage
from dh_pyspark.model.tree_model import SaveOrig
from dh_pyspark.services._coreset_service_base import CoresetTreeServiceBase, OutputFormat


def get_id():
    return round(time.time())


class RemoteCoresetTreeService(CoresetTreeServiceBase):

    def get_service_class(self):
        raise NotImplementedError("Subclasses must implement this method")

    def get_wrapped_code(self, text):
        text = textwrap.indent(textwrap.dedent(text), "    ")
        job_text = textwrap.dedent(f"""from pyspark.sql import SparkSession
from {self.service_module_name} import {self.service_class_name}
from dh_pyspark.services._coreset_service_base import DataParams

spark = SparkSession.builder.appName("build_from_file").getOrCreate()

if __name__ == "__main__":
{text}""")
        return job_text

    def __init__(self, *, dhspark_path, data_params: Union[DataParams, dict] = None,
                 chunk_size: int = None,
                 chunk_by=None, coreset_size=None,
                 coreset_params: Union[CoresetParams, dict] = CoresetParamsDTC(),
                 n_instances: int = None, n_instances_exact: bool = None,
                 sample_all=None, chunk_sample_ratio=None, class_size=None,
                 save_orig: SaveOrig = SaveOrig.NONE,
                 remote_service_config
                 ):
        self.remote_service_config = remote_service_config
        self.remote_jobs = []
        self.workflow_id = f"wf-{get_id()}"
        all_params = locals()
        # Get default values from the function signature
        signature = inspect.signature(self.__init__)
        default_values = {k: v.default for k, v in signature.parameters.items() if v.default is not inspect.Parameter.empty}
        # Filter out parameters that have default values and were not explicitly passed
        explicitly_passed = {
            k: v for k, v in all_params.items()
            if k not in default_values or (v != default_values[k] and not (v is None and default_values[k] is None))
        }
        del explicitly_passed["self"]
        del explicitly_passed["remote_service_config"]
        self.init_params = explicitly_passed
        service_class = self.get_service_class()
        self.service_class_name = service_class.get("class_name")
        self.service_module_name = service_class.get("module_name")
        self.cluster_name = f"cluster-id-{get_id()}"
        self.cluster_params = {}

    def get_job_spark_config(self, job_name):
        """
        Return spark configuration for certain job_name
        """
        spark_config = self.remote_service_config.get('spark_config') or {}
        default_config = spark_config.get('default') or {}
        job_config = spark_config.get(job_name) or {}
        default_config.update(job_config)
        return default_config

    def build_from_file(self, input_path: str, input_format: str = "parquet", partial=False):
        job_text = self.get_wrapped_code(f"""\
            print("Starting build_preprocess_from_file")
            init_params = {self.init_params}
            service = {self.service_class_name}(**init_params)
            service.{'partial_' if partial else ''}build_preprocess_from_file(
                spark, input_path="{input_path}", input_format="{input_format}"
            )
            print("build_preprocess_from_file finished, the data is saved to {self.init_params.get('dhspark_path')}")
        """)

        self.remote_jobs.append({
            "job_name": f"{'partial_' if partial else ''}preprocess",
            "job_text": job_text,
            "spark_config": self.get_job_spark_config("preprocess")
        })

        job_text = self.get_wrapped_code(f"""\
            print(f"Starting build")
            init_params = {self.init_params}
            service = CoresetTreeServiceDTC(**init_params)
            service.{'partial_' if partial else ''}build(spark)
            print(f"build finished, the data is saved to {self.init_params.get('dhspark_path')}")
        """)

        self.remote_jobs.append({
            "job_name": f"{'partial_' if partial else ''}build",
            "job_text": job_text,
            "spark_config": self.get_job_spark_config("build")
        })

    def partial_build_from_file(self, input_path: str, input_format: str = "parquet"):
        self.build_from_file(input_path=input_path, input_format=input_format, partial=True)

    def get_coreset(self,
                    level: int = 0,
                    seq_from=None,
                    seq_to=None,
                    save_path=None,
                    preprocessing_stage: str = PreprocessingStage.AUTO,
                    output_format: str = OutputFormat.SPARK_DF,
                    sparse_threshold: float = 0.01,
                    ):
        get_coreset_params = locals()
        del get_coreset_params['self']
        job_text = self.get_wrapped_code(text=f"""\
            print(f"Starting get_coreset")
            init_params = {self.init_params}
            get_coreset_params = {get_coreset_params}
            service = CoresetTreeServiceDTC(
                **init_params
            )
            service.get_coreset(spark_session=spark, **get_coreset_params)
            print(f"get_coreset finished, the data is saved to {save_path}")
        """)
        self.remote_jobs.append({
            "job_name": f"get_coreset_level_{level}",
            "job_text": job_text,
            "spark_config": self.get_job_spark_config("get_coreset")
        })

    def callable_remote_run(self, job_name, func):
        source = inspect.getsource(func)  # Get full function source
        source_lines = source.split("\n")  # Split into lines
        body_lines = source_lines[1:]
        self.remote_jobs.append({
            "job_name": job_name,
            "job_text": self.get_wrapped_code("\n".join(body_lines)),
            "spark_config": self.get_job_spark_config("default")
        })

    def upload_text_to_cloud(self, destination_file_name, text):
        raise NotImplementedError("Subclasses must implement this method")

    def get_pip_install_text(self):
        pip_packages = f"dh_pyspark {self.get_config_value('python_libraries')}"
        return f"python3 -m pip install {pip_packages}"

    def upload_scripts(self):
        scripts = []

        # Upload initialization script
        initial_script_path = self.upload_text_to_cloud(
            destination_file_name="bootstrap.sh",
            text=self.get_pip_install_text()
        )

        scripts.append({"step": "bootstrap", "path": initial_script_path})

        for index, workflow_step in enumerate(self.remote_jobs):
            step_name = f"step_{index}_{workflow_step.get('job_name')}"
            exec_name = self.upload_text_to_cloud(
                destination_file_name=f"{step_name}.py",
                text=workflow_step.get('job_text')
            )
            scripts.append({"name": step_name, "path": exec_name, "spark_config": workflow_step['spark_config']})

        return scripts

    def get_config_value(self, name):
        return self.remote_service_config['main'][name]

    def get_cluster_web_interfaces(self):
        raise NotImplementedError("Subclasses must implement this method")

    def print_cluster_web_interfaces(self):
        ui_list = self.get_cluster_web_interfaces()
        if ui_list and len(ui_list) > 0:
            print()
            print("Web Interfaces available:")
            for ui in ui_list:
                print(f"{ui.get('name')}: {ui.get('url')}")
            print()
            print("Web Interfaces available only after cluster's start")
        else:
            print("Web Interfaces are not available")
        return ui_list

    def execute(self):
        raise NotImplementedError("Subclasses must implement this method")

    def get_cluster_status(self):
        raise NotImplementedError("Subclasses must implement this method")

    def get_cluster_finished(self):
        raise NotImplementedError("Subclasses must implement this method")

    def download_from_cloud(self, source_folder, local_dir):
        raise NotImplementedError("Subclasses must implement this method")
