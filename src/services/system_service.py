import psutil
from typing import Dict, Any

class SystemService:
    @staticmethod
    def get_disk_usage(path: str = "/") -> Dict[str, Any]:
        """Returns disk usage for a given path."""
        # On Windows, path should be "C:/" or similar.
        import platform
        if platform.system() == "Windows" and path == "/":
            path = "C:/"
            
        usage = psutil.disk_usage(path)
        return {
            "total_gb": round(usage.total / (1024**3), 2),
            "used_gb": round(usage.used / (1024**3), 2),
            "free_gb": round(usage.free / (1024**3), 2),
            "percent_used": usage.percent
        }
