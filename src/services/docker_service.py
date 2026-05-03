import docker
from typing import List, Dict, Any
from src.model.docker_resource import DockerResource

class DockerService:
    def __init__(self):
        try:
            self.client = docker.from_env()
        except Exception as e:
            raise ConnectionError(f"Could not connect to Docker daemon: {e}")

    def get_detailed_usage(self) -> Dict[str, Any]:
        """Get detailed counts and sizes of Docker resources."""
        df_data = self.client.df()
        
        # Helper to sum sizes from a list of objects/dicts
        def sum_size(items, size_key='Size'):
            total = 0
            for item in items:
                # If it's a dict, get key, if object, get attribute
                if isinstance(item, dict):
                    if size_key == 'UsageData': # Special case for Volumes
                        total += item.get('UsageData', {}).get('Size', 0)
                    else:
                        total += item.get(size_key, 0)
                else:
                    if size_key == 'UsageData':
                        total += getattr(item, 'UsageData', {}).get('Size', 0)
                    else:
                        total += getattr(item, size_key, 0)
            return total

        return {
            "containers": {
                "count": len(df_data.get('Containers', [])),
                "size": sum_size(df_data.get('Containers', []))
            },
            "images": {
                "count": len(df_data.get('Images', [])),
                "size": sum_size(df_data.get('Images', []))
            },
            "volumes": {
                "count": len(df_data.get('Volumes', [])),
                "size": sum_size(df_data.get('Volumes', []), 'UsageData')
            },
            "build_cache": {
                "size": sum_size(df_data.get('BuildCache', []))
            }
        }

    def get_disk_usage(self) -> Dict[str, Any]:

        """Equivalent to docker system df."""
        return self.client.df()

    def prune_containers(self, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        return self.client.containers.prune(filters=filters)

    def prune_images(self, filters: Dict[str, Any] = None, dangling: bool = True) -> Dict[str, Any]:
        # If dangling=False, it's equivalent to -a in CLI
        if not dangling:
            if filters is None:
                filters = {}
            filters['dangling'] = False
        return self.client.images.prune(filters=filters)

    def prune_volumes(self, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        return self.client.volumes.prune(filters=filters)

    def prune_networks(self, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        return self.client.networks.prune(filters=filters)

    def prune_system(self, filters: Dict[str, Any] = None, volumes: bool = False) -> Dict[str, Any]:
        return self.client.system.prune(filters=filters, volumes=volumes)

    def prune_builder(self, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        return self.client.api.prune_build_cache(filters=filters)

    def get_containers_to_prune(self, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        # Stopped containers (status=exited)
        if filters is None:
            filters = {}
        filters['status'] = 'exited'
        return self.client.containers.list(all=True, filters=filters)

    def get_images_to_prune(self, filters: Dict[str, Any] = None, dangling: bool = True) -> List[Dict[str, Any]]:
        if filters is None:
            filters = {}
        filters['dangling'] = dangling
        return self.client.images.list(filters=filters)

    def get_volumes_to_prune(self, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        if filters is None:
            filters = {}
        filters['dangling'] = True
        return self.client.volumes.list(filters=filters)
