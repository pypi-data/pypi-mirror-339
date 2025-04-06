"""
End-to-end tests for cluster deployment and workflow
at the moment implements checks for AWS, GCP and Azure
At the moment could be executed locally only, before running requires command line authentication
 - az login
 - gcloud auth login
 - aws configure

# TODO implement in workflow grid_search and model training, check results
# TODO implement login to clouds to make it possible run these tests in the CI/CD cloud
"""
import time
from uuid import uuid4
import pandas as pd
import pytest
from pyspark.pandas import spark
from dh_pyspark.services.remote.aws.dtc import RemoteAWSCoresetTreeServiceDTC
from dh_pyspark.services.remote.azure.dtc import RemoteAzureCoresetTreeServiceDTC
from dh_pyspark.services.remote.gcp.dtc import RemoteGCPCoresetTreeServiceDTC

aws_remote_service_config = {
    "main": {
        "region": "us-east-1",
        "destination_path": "spark-deploy-test/run-folder",
        "python_libraries": "xgboost"
    },
    "cluster_config": {
        "InstanceGroups": [
            {
                "Name": "Master Node",
                "InstanceRole": "MASTER",
                "InstanceType": "m5.xlarge",
                "InstanceCount": 1,
            },
            {
                "Name": "Worker Nodes",
                "InstanceRole": "CORE",
                "InstanceType": "m5.xlarge",
                "InstanceCount": 2,
            },
        ],
    },
}
azure_remote_service_config = {
    "main": {
        "region": "eastus",
        "destination_path": "run-folder",
        "python_libraries": "xgboost",
        # Azure-specific fields
        "spark_pool_name": "pool",
        "synapse_workspace": "daatheroes042",
        "subscription_id": "4c4ba3cb-c76a-4dd5-893b-967677466561",
        "resource_group": "dataheroes",
        "storage_account_name": "dataheroes",
        "storage_account_key": "V+F5wAQau2QsAxeSxz4ck6obFyidAX6jRb+1GP6hGtJpmOwlnkJS6nq0DBaw/mNogjSXoIbRo/38+ASto1IIow==",
    },
    "cluster_config": {
        "driver_memory": "1g",
        "driver_cores": 4,
        "executor_memory": "1g",
        "executor_cores": 4,
        "executor_count": 1,
    },
}
gcp_remote_service_config = {
    "main": {
        "region": "us-central1",
        "destination_path": "dh-spark-runs/spark-test",
        "python_libraries": "xgboost zipp",
        # GCP-specific field
        "project_id": "dataheros"
    },
    "cluster_config": {
        "master_config": {
            "num_instances": 1,
            "machine_type_uri": "n1-standard-2",
            "disk_config": {"boot_disk_type": "pd-standard", "boot_disk_size_gb": 30},
        },
        "worker_config": {
            "num_instances": 2,
            "machine_type_uri": "n1-standard-2",
            "disk_config": {"boot_disk_type": "pd-standard", "boot_disk_size_gb": 30},
        },
    }
}

cloud_params_const = [
    {
        "name": "AWS",
        "remote_service_config": aws_remote_service_config,
        "main_input_path": "s3://spark-deploy-test/test-dataset/main-dataset",
        "add_input_path": "s3://spark-deploy-test/test-dataset/additional-dataset",
        "output_path_prefix": "s3://spark-deploy-test/run-folder/my-output",
        "service_class": RemoteAWSCoresetTreeServiceDTC
    },
    {
        "name": "Azure",
        "remote_service_config": azure_remote_service_config,
        "main_input_path": "abfss://spark-inout@dataheroes.dfs.core.windows.net/dataset/main",
        "add_input_path": "abfss://spark-inout@dataheroes.dfs.core.windows.net/dataset/add",
        "output_path_prefix": "abfss://spark-inout@dataheroes.dfs.core.windows.net/output",
        "service_class": RemoteAzureCoresetTreeServiceDTC
    },
    {
        "name": "GCP",
        "remote_service_config": gcp_remote_service_config,
        "main_input_path": "gs://dh-spark-runs/test-dataset/main-dataset",
        "add_input_path": "gs://dh-spark-runs/test-dataset/additional-dataset",
        "output_path_prefix": "gs://dh-spark-runs/spark-test/my-output",
        "service_class": RemoteGCPCoresetTreeServiceDTC
    }
]


def run_single_remote(cloud_params):
    output_path = f"{cloud_params.get('output_path_prefix')}"
    service_class = cloud_params.get("service_class")
    remote_service_config = cloud_params.get("remote_service_config")
    add_input_path = cloud_params.get("add_input_path")
    main_input_path = cloud_params.get("main_input_path")
    # The code below does not depend on cloud platform (works for AWS, Azure, GCP)
    data_params = {
        'target': {'name': 'y'},
        'features': [{'name': 'col1'}, {'name': 'col2'}, {'name': 'col3'}],
    }
    # The service object for the Coreset tree building
    service = service_class(
        chunk_size=100,
        coreset_size=0.2,
        data_params=data_params,
        dhspark_path=output_path,
        remote_service_config=remote_service_config
    )
    # adding the job for building Coreset tree from the file
    service.build_from_file(input_path=main_input_path)
    service.partial_build_from_file(input_path=add_input_path)
    service.get_coreset(level=0, save_path=f"{output_path}/coreset/level-0")
    service.get_coreset(level=1, save_path=f"{output_path}/coreset/level-1")
    service.execute()
    return service


@pytest.mark.parametrize('cloud_params', cloud_params_const)
def test_remote(cloud_params, tmp_path):
    service = run_single_remote(cloud_params)
    output_path = f"{cloud_params.get('output_path_prefix')}"
    while not service.get_cluster_finished():
        status = service.get_cluster_status()
        print(f"{status}")
        time.sleep(60)
    # Download coreset and check dataframe columns and size
    download_path = tmp_path
    service.download_from_cloud(
        source_folder=f'{output_path}/coreset/level-1',
        local_dir=download_path
    )
    coreset_df = pd.read_parquet(download_path)
    print(f'{coreset_df.columns=}')
    print(f'{coreset_df.shape[0]=}')
    assert set(coreset_df.columns) == set(['w', 'features', 'y'])
    assert coreset_df.shape[0] > 30
