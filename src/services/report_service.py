import json
from datetime import datetime
from typing import Dict, Any

class ReportService:
    @staticmethod
    def generate_json(data: Dict[str, Any], path: str):
        report = {
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        with open(path, 'w') as f:
            json.dump(report, f, indent=4)

    @staticmethod
    def _format_size(bytes_size: float) -> str:
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_size < 1024:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024
        return f"{bytes_size:.2f} PB"

    @staticmethod
    def generate_markdown(data: Dict[str, Any], path: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lines = [
            "# Docker Cleanup Pro Report",
            f"**Date:** {timestamp}",
            "",
            "## Docker Detailed Usage",
            "| Resource Type | Count | Size |",
            "| :--- | :---: | :---: |"
        ]
        
        docker = data.get('docker_detailed', {})
        for key in ['containers', 'images', 'volumes']:
            res = docker.get(key, {})
            lines.append(f"| {key.capitalize()} | {res.get('count', 0)} | {ReportService._format_size(res.get('size', 0))} |")
        
        lines.append(f"| Build Cache | - | {ReportService._format_size(docker.get('build_cache', {}).get('size', 0))} |")
        lines.append("")
        
        system = data.get('system_disk', {})
        lines.append("## System Disk Usage")
        lines.append(f"- **Total:** {system.get('total_gb')} GB")
        lines.append(f"- **Used:** {system.get('used_gb')} GB ({system.get('percent_used')}%)")
        lines.append(f"- **Free:** {system.get('free_gb')} GB")
        lines.append("")
        
        relation = data.get('relation', {})
        lines.append("## Docker vs System Relation")
        lines.append(f"- **Docker Total Size:** {ReportService._format_size(relation.get('docker_total_bytes', 0))}")
        lines.append(f"- **Impact:** Docker represents **{relation.get('docker_ratio_percent', 0)}%** of used disk space.")
            
        with open(path, 'w') as f:
            f.write("\n".join(lines))
