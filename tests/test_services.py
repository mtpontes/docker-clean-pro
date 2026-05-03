import pytest
from unittest.mock import MagicMock, patch
from src.services.docker_service import DockerService
from src.services.system_service import SystemService

@patch('docker.from_env')
def test_docker_service_usage(mock_from_env):
    mock_client = MagicMock()
    mock_from_env.return_value = mock_client
    
    # Mock return value for client.df()
    mock_client.df.return_value = {
        'Containers': [{'Size': 100}, {'Size': 200}],
        'Images': [{'Size': 1000}, {'Size': 2000}],
        'Volumes': [{'UsageData': {'Size': 500}}],
        'BuildCache': [{'Size': 50}]
    }
    
    service = DockerService()
    usage = service.get_detailed_usage()
    
    assert usage['containers']['count'] == 2
    assert usage['containers']['size'] == 300
    assert usage['images']['count'] == 2
    assert usage['images']['size'] == 3000
    assert usage['volumes']['count'] == 1
    assert usage['volumes']['size'] == 500
    assert usage['build_cache']['size'] == 50

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
