from dh_pyspark.services.remote.aws.base import RemoteAWSCoresetTreeService


class RemoteAWSCoresetTreeServiceDTC(RemoteAWSCoresetTreeService):

    def get_service_class(self):
        return {
            "class_name": "CoresetTreeServiceDTC",
            "module_name": "dh_pyspark.services.coreset.dtc"
        }