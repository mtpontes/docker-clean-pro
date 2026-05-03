import pytest
from unittest.mock import MagicMock, patch
from src.services.docker_service import DockerService
from src.services.system_service import SystemService

@patch('docker.from_env')
def test_docker_service_counts(mock_from_env):
    mock_client = MagicMock()
    mock_from_env.return_value = mock_client
    
    mock_client.containers.list.return_value = [1, 2, 3]
    mock_client.images.list.return_value = [1, 2]
    mock_client.volumes.list.return_value = [1]
    mock_client.networks.list.return_value = [1, 2, 3, 4]
    
    service = DockerService()
    counts = service.get_resource_counts()
    
    assert counts['containers'] == 3
    assert counts['images'] == 2
    assert counts['volumes'] == 1
    assert counts['networks'] == 4

@patch('psutil.disk_usage')
def test_system_service_usage(mock_disk_usage):
    mock_usage = MagicMock()
    mock_usage.total = 100 * (1024**3)
    mock_usage.used = 40 * (1024**3)
    mock_usage.free = 60 * (1024**3)
    mock_usage.percent = 40.0
    mock_disk_usage.return_value = mock_usage
    
    usage = SystemService.get_disk_usage("C:/")
    
    assert usage['total_gb'] == 100.0
    assert usage['used_gb'] == 40.0
    assert usage['percent_used'] == 40.0
