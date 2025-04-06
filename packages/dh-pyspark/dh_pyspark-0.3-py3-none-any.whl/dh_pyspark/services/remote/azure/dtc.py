from dh_pyspark.services.remote.azure.base import RemoteAzureCoresetTreeService


class RemoteAzureCoresetTreeServiceDTC(RemoteAzureCoresetTreeService):

    def get_service_class(self):
        return {
            "class_name": "CoresetTreeServiceDTC",
            "module_name": "dh_pyspark.services.coreset.dtc"
        }