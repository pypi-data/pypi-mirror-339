import os
import re
import textwrap
import time
from typing import Union

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.synapse.spark import SparkClient
from azure.synapse.spark.models import SparkBatchJobOptions

from dataheroes import CoresetParams, CoresetParamsDTC, DataParams
from dh_pyspark.model.tree_model import SaveOrig
from dh_pyspark.services.remote.base import RemoteCoresetTreeService


class RemoteAzureCoresetTreeService(RemoteCoresetTreeService):
    def __init__(self, *, dhspark_path, data_params: Union[DataParams, dict] = None,
                 chunk_size: int = None,
                 chunk_by=None, coreset_size=None,
                 coreset_params: Union[CoresetParams, dict] = CoresetParamsDTC(),
                 n_instances: int = None, n_instances_exact: bool = None,
                 sample_all=None, chunk_sample_ratio=None, class_size=None,
                 save_orig: SaveOrig = SaveOrig.NONE,
                 remote_service_config
                 ):
        super().__init__(
            dhspark_path=dhspark_path,
            data_params=data_params,
            chunk_size=chunk_size,
            chunk_by=chunk_by,
            coreset_size=coreset_size,
            coreset_params=coreset_params,
            n_instances=n_instances,
            n_instances_exact=n_instances_exact,
            sample_all=sample_all,
            chunk_sample_ratio=chunk_sample_ratio,
            class_size=class_size,
            save_orig=save_orig,
            remote_service_config=remote_service_config
        )
        self.container_name = self.cluster_name

    def upload_text_to_cloud(self, destination_file_name, text):
        blob_service_client = BlobServiceClient(
            account_url=f"https://{self.get_config_value('storage_account_name')}.blob.core.windows.net",
            credential=self.get_config_value("storage_account_key")
        )

        destination_path = self.get_config_value("destination_path")
        container_client = blob_service_client.get_container_client(self.container_name)
        if not container_client.exists():
            container_client.create_container()
            print(f"✅ Container '{self.container_name}' created.")
        path_in_container = "/".join([destination_path, destination_file_name])
        blob_client = blob_service_client.get_blob_client(
            container=self.container_name,
            blob=path_in_container
        )
        blob_client.upload_blob(text, overwrite=True)
        print(f"✅ Uploaded: {path_in_container}")
        return path_in_container

    def download_from_cloud(self, source_folder, local_dir):
        if source_folder.startswith("abfss://"):
            # Parse abfss://<container>@<account>.dfs.core.windows.net/<prefix>
            match = re.match(r"abfss://(.+?)@(.+?)\.dfs\.core\.windows\.net/(.*)", source_folder)
            if not match:
                raise ValueError(f"Invalid abfss path: {source_folder}")
            container_name, account_name, prefix = match.groups()
        else:
            raise ValueError("Only abfss:// paths are supported here")
        account_url = f"https://{account_name}.blob.core.windows.net"
        credential = self.get_config_value("storage_account_key")
        blob_service_client = BlobServiceClient(account_url=account_url, credential=credential)
        container_client = blob_service_client.get_container_client(container_name)

        blobs = container_client.list_blobs(name_starts_with=prefix)

        for blob in blobs:
            if blob.name.endswith("/"):
                continue
            relative_path = blob.name[len(prefix):].lstrip("/")
            local_path = os.path.join(local_dir, relative_path)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            with open(local_path, "wb") as file:
                file.write(container_client.download_blob(blob.name).readall())
            print(
                f"✅ Downloaded: abfss://{container_name}@{account_name}.dfs.core.windows.net/{blob.name} → {local_path}")

    def get_wrapped_code(self, text):
        text = textwrap.indent(textwrap.dedent(text), "        ") #
        job_text = textwrap.dedent(f"""from pyspark.sql import SparkSession
from dh_pyspark.services.coreset.dtc import CoresetTreeServiceDTC
from dh_pyspark.services._coreset_service_base import DataParams

import pandas as pd
import fsspec
from adlfs import AzureBlobFileSystem

ACCOUNT_KEY = "{self.get_config_value('storage_account_key')}"

def parse_wasbs_path(wasbs_path):
    path_wo_scheme = wasbs_path[len("wasbs://"):]
    container, rest = path_wo_scheme.split("@", 1)
    account, blob_path = rest.split(".blob.core.windows.net/", 1)
    return account, container, blob_path

# ===   PATCH: pandas.to_parquet
original_to_parquet = pd.DataFrame.to_parquet

def patched_to_parquet(self, path, *args, **kwargs):
    if isinstance(path, str) and path.startswith("wasbs://"):
        account, container, blob_path = parse_wasbs_path(path)
        fs = AzureBlobFileSystem(account_name=account, account_key=ACCOUNT_KEY)
        print(f"[patched] Writing to: az://{{container}}/{{blob_path}}")
        with fs.open(f"{{container}}/{{blob_path}}", "wb") as f:
            return original_to_parquet(self, f, *args, **kwargs)
    return original_to_parquet(self, path, *args, **kwargs)

pd.DataFrame.to_parquet = patched_to_parquet

# ===   PATCH: pandas.read_parquet
original_read_parquet = pd.read_parquet

def patched_read_parquet(path, *args, **kwargs):
    if isinstance(path, str) and path.startswith("wasbs://"):
        account, container, blob_path = parse_wasbs_path(path)
        if not blob_path.endswith(".parquet"):
            blob_path = blob_path.rstrip("/") + "/categories.parquet"
        fs = AzureBlobFileSystem(account_name=account, account_key=ACCOUNT_KEY)
        print(f"[patched] Reading from: az://{{container}}/{{blob_path}}")
        with fs.open(f"{{container}}/{{blob_path}}", "rb") as f:
            return original_read_parquet(f, *args, **kwargs)
    return original_read_parquet(path, *args, **kwargs)

pd.read_parquet = patched_read_parquet

# === 🚀 Spark session
# spark = SparkSession.builder.appName("job").config(
#     "spark.jars.packages",
#     "org.apache.hadoop:hadoop-azure:3.2.0,com.microsoft.azure:azure-storage:8.6.6"
# ).getOrCreate()

spark = SparkSession.builder.appName("job").getOrCreate()

if __name__ == "__main__":
    try:
{text}
    except Exception as e:
        import traceback
        print("❌ Exception occurred during the step:")
        traceback.print_exc()
        raise    
""")
        return job_text

    def upload_main_script(self, job_scripts):
        pip_packages = f"dataheroes pyarrow fsspec adlfs scikit-learn numpy==1.26.4 dh_pyspark {self.get_config_value('python_libraries')}"

        text = f"""
import subprocess
import sys
from pyspark.sql import SparkSession
from azure.storage.filedatalake import DataLakeServiceClient

# Import libs on the driver
print("🚀 Starting libs_to_workers.py")
print("🚀 [driver] Initializing SparkSession early")
spark = SparkSession.builder.getOrCreate()
subprocess.run([sys.executable, "-m", "ensurepip", "--upgrade"], check=False)
subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
subprocess.run([sys.executable, "-m", "pip", "install"]+"{pip_packages}".split(' '), check=True)
result = subprocess.run(
  [sys.executable, "-m", "pip", "show", "scikit-learn"], 
  check=True, capture_output=True, text=True)

print("📦 pip show output:")
print(result.stdout)

df = spark.createDataFrame([("install",), ("libs",)], ["dummy"])
def install_packages(row):
    import subprocess
    import sys
    subprocess.run([sys.executable, "-m", "pip", "install"]+"{pip_packages}".split(' '), check=True)
    return f"✅ Done on {{row}}"

# Import libs on the workers
results = df.rdd.map(install_packages).collect()
print("✅ All done:")
for r in results:
    print(r)
    
account_name = "{self.get_config_value('storage_account_name')}"
container = "{self.container_name}"
storage_key = "{self.get_config_value('storage_account_key')}"

scripts = {str(job_scripts)}
remote_base_path = "run-folder/"

service_client = DataLakeServiceClient(
    account_url=f"https://{{account_name}}.dfs.core.windows.net",
    credential=storage_key
)
fs_client = service_client.get_file_system_client(container)

for workflow_step in scripts:
    remote_path = workflow_step['path']
    local_path = workflow_step['name']+'.py'
    print(f"📥 Downloading {{remote_path}}")
    file_client = fs_client.get_file_client(remote_path)
    with open(local_path, "wb") as f:
        f.write(file_client.download_file().readall())

    print(f"🚀 Running {{local_path}}")
    subprocess.run(["spark-submit", "--master", "yarn", "--deploy-mode", "client", local_path], check=True)
"""
        return self.upload_text_to_cloud("run.py", text)

    def get_spark_client(self):
        credential = DefaultAzureCredential()
        return SparkClient(
            endpoint=f"https://{self.get_config_value('synapse_workspace')}.dev.azuresynapse.net",
            credential=credential,
            spark_pool_name=self.get_config_value("spark_pool_name")
        )

    def execute(self):
        print("🚀 Preparing Spark job for Azure Synapse...")
        scripts = self.upload_scripts()
        main_script_path = self.upload_main_script(scripts[1:])
        spark_file_path = (f"abfss://{self.container_name}@{self.get_config_value('storage_account_name')}."
                           f"dfs.core.windows.net/{main_script_path}")
        job = SparkBatchJobOptions(
            name="dh-spark-job",
            file=spark_file_path,
            class_name="org.apache.spark.deploy.PythonRunner",
            configuration={
                "spark.hadoop.fs.azure.account.key.dataheroes.blob.core.windows.net":
                    self.get_config_value('storage_account_key')
            },
            driver_memory=self.remote_service_config.get('cluster_config').get("driver_memory"),
            driver_cores=self.remote_service_config.get('cluster_config').get("driver_cores"),
            executor_memory=self.remote_service_config.get('cluster_config').get("executor_memory"),
            executor_cores=self.remote_service_config.get('cluster_config').get("executor_cores"),
            executor_count=self.remote_service_config.get('cluster_config').get("executor_count"),
        )
        job_response = self.get_spark_client().spark_batch.create_spark_batch_job(spark_batch_job_options=job)
        print("✅ Spark job submitted.")
        self.cluster_params['job_id'] = job_response.id
        print("🧾 Job ID:", self.cluster_params['job_id'])
        return self.print_cluster_web_interfaces()

    def get_cluster_web_interfaces(self):
        # Wait for cluster to appear and become RUNNING
        timeout_sec = 300
        spark_client = self.get_spark_client()
        start_time = time.time()
        while time.time() - start_time < timeout_sec:
            job = spark_client.spark_batch.get_spark_batch_job(self.cluster_params.get('job_id'))
            state = job.state
            print(f"⏳ Job state: {state}")
            if state == 'running':
                return [
                    {"name": "Synapse Analytics Job page",
                     "url": f"https://web.azuresynapse.net/en/monitoring/sparkapplication/dh-spark-job?workspace"
                            f"=%2Fsubscriptions%2F"
                            f"{self.get_config_value('subscription_id')}"
                            f"%2FresourceGroups%2F{self.get_config_value('resource_group')}%2Fproviders%"
                            f"2FMicrosoft.Synapse%2Fworkspaces%2F"
                            f"{self.get_config_value('synapse_workspace')}"
                            f"&sparkPoolName={self.get_config_value('spark_pool_name')}&"
                            f"livyId={self.cluster_params.get('job_id')}",
                     },
                    {"name": "Spark UI", "url": job.app_info['sparkUiUrl']},
                    {"name": "Driver Log", "url": job.app_info['driverLogUrl']},
                ]
            time.sleep(10)
        raise TimeoutError(f"Job {self.cluster_params.get('job_id')} did not become ready in {timeout_sec} seconds")

    def get_cluster_status(self):
        spark_client = self.get_spark_client()
        job = spark_client.spark_batch.get_spark_batch_job(self.cluster_params.get('job_id'))
        return job.state

    def get_cluster_finished(self):
        status = self.get_cluster_status()
        return status in ['success', 'error', 'dead', 'killed']