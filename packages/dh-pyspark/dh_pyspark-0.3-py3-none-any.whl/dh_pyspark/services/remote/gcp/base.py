import os
import time

from google.cloud.dataproc_v1.types import Component

from dh_pyspark.services.remote.base import RemoteCoresetTreeService, get_id
from google.cloud import dataproc_v1, storage
import google.api_core.exceptions


class RemoteGCPCoresetTreeService(RemoteCoresetTreeService):

    def upload_text_to_cloud(self, destination_file_name, text):
        client = storage.Client()
        full_destination_path = "/".join(
            [self.remote_service_config["main"]["destination_path"],
             self.workflow_id,
             destination_file_name
             ]
        )
        bucket = client.bucket(full_destination_path.split('/')[0])
        path_without_bucket = "/".join(full_destination_path.split('/')[1:])
        blob = bucket.blob(path_without_bucket)
        blob.upload_from_string(text, content_type="text/plain")
        gcp_path = f"gs://{full_destination_path}"
        print(f"✅ Text uploaded to: {gcp_path}")
        return gcp_path

    def download_from_cloud(self, source_folder, local_dir):
        storage_client = storage.Client()
        source_folder_clean = source_folder.replace('gs://', '')
        bucket_name = source_folder_clean.split('/')[0]
        prefix = "/".join(source_folder_clean.split('/')[1:])

        blobs = storage_client.list_blobs(bucket_name, prefix=prefix)

        for blob in blobs:
            if blob.name.endswith("/"):
                continue
            relative_path = blob.name[len(prefix):].lstrip("/")
            local_path = os.path.join(local_dir, relative_path)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            blob.download_to_filename(local_path)
            print(f"✅ Downloaded: gs://{bucket_name}/{blob.name} → {local_path}")

    def get_gcp_workflow_template(self):
        scripts = self.upload_scripts()
        initial_script_path = scripts[0]["path"]

        previous_step = None
        jobs = []
        for workflow_step in scripts[1:]:
            step_name = workflow_step["name"]
            exec_name = workflow_step["path"]
            step_config = {
                "step_id": step_name,
                "pyspark_job": {
                    "main_python_file_uri": exec_name,
                    "file_uris": [initial_script_path],
                    "properties": workflow_step['spark_config']
                }
            }
            if previous_step:
                step_config["prerequisite_step_ids"] = [previous_step]

            jobs.append(step_config)
            previous_step = step_name

        cluster_config = self.remote_service_config['cluster_config']
        cluster_config['initialization_actions'] = [{
            "executable_file": initial_script_path,
        }]
        cluster_config['gce_cluster_config'] = {
            "metadata": {"PIP_PACKAGES": self.get_config_value("python_libraries")},
            "internal_ip_only": False
        }
        cluster_config['software_config'] = {
            "optional_components": [Component.JUPYTER]
        }
        cluster_config['endpoint_config'] = {
            "enable_http_port_access": True
        }
        workflow_template = {
            "id": self.workflow_id,
            "placement": {
                "managed_cluster": {
                    "cluster_name": self.cluster_name,
                    "config": {**cluster_config}
                }
            },
            "jobs": jobs,
        }
        return workflow_template

    def get_cluster_web_interfaces(self):
        # Wait for cluster to appear and become RUNNING
        cluster_client = dataproc_v1.ClusterControllerClient(
            client_options={"api_endpoint": f"{self.get_config_value('region')}-dataproc.googleapis.com:443"}
        )
        start_time = time.time()
        timeout_sec = 300
        while time.time() - start_time < timeout_sec:
            clusters = cluster_client.list_clusters(
                project_id=self.get_config_value('project_id'),
                region=self.get_config_value('region'))
            for cluster in clusters.clusters:
                if cluster.cluster_name.startswith(self.cluster_name):
                    print(f"Updating cluster name {cluster.cluster_name}")
                    self.cluster_name = cluster.cluster_name
                    cluster = cluster_client.get_cluster(
                        project_id=self.get_config_value('project_id'),
                        region=self.get_config_value('region'),
                        cluster_name=self.cluster_name
                    )

                    if cluster.config.endpoint_config.enable_http_port_access:
                        endpoints = cluster.config.endpoint_config.http_ports
                        ui_list = []
                        for name, url in endpoints.items():
                            ui_list.append({"name": name, "url": url})
                        return ui_list
                    else:
                        return None
            print(f"🛰 Waiting for cluster: {self.cluster_name} {time.strftime('%H:%M:%S', time.localtime(time.time()))}")
            time.sleep(10)

        raise RuntimeError("Failed to get a cluster")

    def execute(self):
        workflow_template = self.get_gcp_workflow_template()
        request = dataproc_v1.CreateWorkflowTemplateRequest(
            parent=f"projects/{self.get_config_value('project_id')}/regions/"
                   f"{self.get_config_value('region')}",
            template=workflow_template,
        )
        try:
            # ✅ Set the regional API endpoint for Dataproc
            client_options = {"api_endpoint": f"{self.get_config_value('region')}-dataproc.googleapis.com:443"}
            workflow_template_client = dataproc_v1.WorkflowTemplateServiceClient(client_options=client_options)
            workflow_template_client.create_workflow_template(request=request)
            print(f"Workflow template created: {self.workflow_id}")
        except google.api_core.exceptions.AlreadyExists:
            print(f"Workflow template already exists: {self.workflow_id}")

        request = dataproc_v1.InstantiateWorkflowTemplateRequest(
            name=f"projects/{self.get_config_value('project_id')}/regions/"
                 f"{self.get_config_value('region')}/workflowTemplates/{self.workflow_id}"
        )
        workflow_template_client.instantiate_workflow_template(request=request)
        return self.print_cluster_web_interfaces()

    def get_cluster_status(self):
        cluster_client = dataproc_v1.ClusterControllerClient(
            client_options={"api_endpoint": f"{self.get_config_value('region')}-dataproc.googleapis.com:443"}
        )
        clusters = cluster_client.list_clusters(
            project_id=self.get_config_value('project_id'),
            region=self.get_config_value('region'))
        for cluster in clusters.clusters:
            if cluster.cluster_name.startswith(self.cluster_name):
                return cluster.status.state.name
        return None

    def get_cluster_finished(self):
        status = self.get_cluster_status()
        return status in ['DELETING', 'ERROR', 'STOPPED']
