from dh_pyspark.services.remote.gcp.base import RemoteGCPCoresetTreeService


class RemoteGCPCoresetTreeServiceDTC(RemoteGCPCoresetTreeService):

    def get_service_class(self):
        return {
            "class_name": "CoresetTreeServiceDTC",
            "module_name": "dh_pyspark.services.coreset.dtc"
        }