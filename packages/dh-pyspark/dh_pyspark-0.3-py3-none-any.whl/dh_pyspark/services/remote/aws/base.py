import os

import boto3
from dh_pyspark.services.remote.base import RemoteCoresetTreeService


class RemoteAWSCoresetTreeService(RemoteCoresetTreeService):

    def upload_text_to_cloud(self, destination_file_name, text):
        s3_client = boto3.client("s3", region_name=self.get_config_value("region"))
        full_destination_path = "/".join(
            [self.remote_service_config["main"]["destination_path"],
             self.workflow_id,
             destination_file_name
             ]
        )
        bucket_name = full_destination_path.split('/')[0]
        path_without_bucket = "/".join(full_destination_path.split('/')[1:])
        s3_client.put_object(Bucket=bucket_name, Key=path_without_bucket, Body=text)
        s3_path = f"s3://{full_destination_path}"
        print(f"✅ Text uploaded to: {s3_path}")
        return s3_path

    def download_from_cloud(self, source_folder, local_dir):
        from smart_open import open as s3_open
        s3 = boto3.client("s3", region_name=self.get_config_value("region"))
        paginator = s3.get_paginator("list_objects_v2")
        source_folder_clean = source_folder.replace('s3://','')
        bucket_name = source_folder_clean.split('/')[0]
        path_without_bucket = "/".join(source_folder_clean.split('/')[1:])
        pages = paginator.paginate(Bucket=bucket_name, Prefix=path_without_bucket)
        for page in pages:
            for obj in page.get("Contents", []):
                key = obj["Key"]
                relative_path = key[len(path_without_bucket):].lstrip("/")
                local_path = os.path.join(local_dir, relative_path)
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                s3_uri = f"s3://{bucket_name}/{key}"
                with s3_open(s3_uri, "rb") as src, open(local_path, "wb") as dst:
                    dst.write(src.read())
                print(f"✅ Downloaded: {s3_uri} → {local_path}")

    def get_pip_install_text(self):
        pip_packages = f"dataheroes pyarrow scikit-learn==1.4.2 numpy==1.26 dh_pyspark {self.get_config_value('python_libraries')}"
        return f"""#!/bin/bash\nsudo python3 -m pip install {pip_packages}"""

    def execute(self):
        emr_client = boto3.client("emr", region_name=self.get_config_value("region"))
        scripts = self.upload_scripts()
        bootstrap_path = scripts[0]["path"]
        job_steps = []

        for workflow_step in scripts[1:]:
            step_name = workflow_step["name"]
            exec_name = workflow_step["path"]
            job_args = ["spark-submit", exec_name]
            for conf_item in [f"{c}={workflow_step['spark_config'][c]}"
                              for c in workflow_step['spark_config']
                              ]:
                job_args.append("--conf")
                job_args.append(conf_item)
            job_steps.append({
                "Name": step_name,
                "ActionOnFailure": "TERMINATE_CLUSTER",
                "HadoopJarStep": {
                    "Jar": "command-runner.jar",
                    "Args": job_args,
                },
            })

        cluster_response = emr_client.run_job_flow(
            Name=self.cluster_name,
            LogUri=f"s3://{self.get_config_value('destination_path')}/logs/",
            ReleaseLabel="emr-7.6.0",
            Applications=[{"Name": "Spark"}],
            Instances={
                **self.remote_service_config['cluster_config'],
                "KeepJobFlowAliveWhenNoSteps": False,
                "TerminationProtected": False,
            },
            BootstrapActions=[  # ✅ Run bootstrap script on master + workers
                {
                    "Name": "Bootstrap Script",
                    "ScriptBootstrapAction": {
                        "Path": bootstrap_path,  # Path to script in S3
                        "Args": []  # Optional arguments
                    },
                }
            ],
            Steps=job_steps,
            VisibleToAllUsers=True,
            JobFlowRole="EMR_EC2_DefaultRole",
            ServiceRole="EMR_DefaultRole",
        )

        self.cluster_params['cluster_id'] = cluster_response["JobFlowId"]
        print(f"✅ EMR Cluster Created: {self.cluster_params['cluster_id']}")
        self.print_cluster_web_interfaces()

    def get_cluster_web_interfaces(self):
        return [
            {"name": "EMR Console UI",
             "url": f"https://console.aws.amazon.com/elasticmapreduce"
                    f"/home?region={self.get_config_value('region')}#cluster-details:{self.cluster_params['cluster_id']}"
             },
            {"name": "Spark History Server",
             "url": f"https://{self.cluster_params['cluster_id']}.emrappui-prod.{self.get_config_value('region')}.amazonaws.com/shs/"
             }
        ]

    def get_cluster_status(self):
        emr_client = boto3.client("emr", region_name=self.get_config_value("region"))
        response = emr_client.describe_cluster(ClusterId=self.cluster_params['cluster_id'])
        state = response["Cluster"]["Status"]["State"]
        return state

    def get_cluster_finished(self):
        status = self.get_cluster_status()
        return status in ['TERMINATED', 'TERMINATED_WITH_ERRORS', 'WAITING']

