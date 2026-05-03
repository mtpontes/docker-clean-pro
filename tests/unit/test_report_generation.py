import os
import json
import pytest
from src.services.report_service import ReportService

def test_generate_json(tmp_path):
    report_file = tmp_path / "test_report.json"
    data = {"docker_detailed": {"containers": {"count": 1, "size": 100}}}
    
    ReportService.generate_json(data, str(report_file))
    
    assert os.path.exists(report_file)
    with open(report_file, 'r') as f:
        content = json.load(f)
        assert content["data"] == data
        assert "timestamp" in content

def test_generate_markdown(tmp_path):
    report_file = tmp_path / "test_report.md"
    data = {
        "docker_detailed": {
            "containers": {"count": 5, "size": 1024},
            "images": {"count": 10, "size": 1024 * 1024},
            "volumes": {"count": 2, "size": 0},
            "build_cache": {"size": 500}
        },
        "system_disk": {
            "total_gb": 100,
            "used_gb": 50,
            "free_gb": 50,
            "percent_used": 50
        },
        "relation": {
            "docker_total_bytes": 1050000,
            "docker_ratio_percent": 2.1
        }
    }
    
    ReportService.generate_markdown(data, str(report_file))
    
    assert os.path.exists(report_file)
    with open(report_file, 'r') as f:
        content = f.read()
        assert "# Docker Cleanup Pro Report" in content
        assert "| Containers | 5 | 1.00 KB |" in content
        assert "| Images | 10 | 1.00 MB |" in content
        assert "Docker represents **2.1%** of used disk space." in content
