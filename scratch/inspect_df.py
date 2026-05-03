import docker
import json

client = docker.from_env()
usage = client.df()

# Helper to make it serializable for inspection
def serialize(obj):
    if isinstance(obj, list):
        return [serialize(i) for i in obj]
    if isinstance(obj, dict):
        return {k: serialize(v) for k, v in obj.items()}
    # Some items in df() might be objects, let's just show their type/repr if not dict/list
    if hasattr(obj, '__dict__'):
        return serialize(obj.__dict__)
    return str(obj)

print(json.dumps(serialize(usage), indent=2))
