from typing import Dict, Any, Optional
from src.services.docker_service import DockerService

class CleanupService:
    def __init__(self, docker_service: DockerService):
        self.docker_service = docker_service

    def _parse_older_than(self, older_than: Optional[str]) -> Dict[str, Any]:
        if not older_than:
            return {}
        
        val = older_than.strip()
        # Basic conversion like the original PS script
        if val.endswith('d'):
            h = int(val[:-1]) * 24
            val = f"{h}h"
        elif val.endswith('w'):
            h = int(val[:-1]) * 168
            val = f"{h}h"
        elif val.endswith('M'):
            h = int(val[:-1]) * 720
            val = f"{h}h"
            
        return {"until": val}

    def basic_cleanup(self, older_than: Optional[str] = None) -> Dict[str, Any]:
        filters = self._parse_older_than(older_than)
        return {
            "containers": self.docker_service.prune_containers(filters),
            "networks": self.docker_service.prune_networks(filters),
            "images": self.docker_service.prune_images(filters, dangling=True)
        }

    def advanced_cleanup(self, older_than: Optional[str] = None) -> Dict[str, Any]:
        filters = self._parse_older_than(older_than)
        basic = self.basic_cleanup(older_than)
        return {
            **basic,
            "volumes": self.docker_service.prune_volumes(filters),
            "images_all": self.docker_service.prune_images(filters, dangling=False),
            "builder": self.docker_service.prune_builder(filters)
        }

    def total_cleanup(self, older_than: Optional[str] = None) -> Dict[str, Any]:
        filters = self._parse_older_than(older_than)
        return {
            "system": self.docker_service.prune_system(filters, volumes=True)
        }

    def get_preview(self, level: str, older_than: Optional[str] = None) -> Dict[str, Any]:
        filters = self._parse_older_than(older_than)
        preview = {}
        
        if level in ['basic', 'advanced']:
            preview['containers'] = self.docker_service.get_containers_to_prune(filters)
            preview['images'] = self.docker_service.get_images_to_prune(filters, dangling=True)
            preview['networks'] = [] # SDK doesn't have a direct "list unused networks" easily without custom logic
            
        if level == 'advanced':
            preview['volumes'] = self.docker_service.get_volumes_to_prune(filters)
            preview['images_all'] = self.docker_service.get_images_to_prune(filters, dangling=False)
            
        return preview
