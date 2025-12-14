import docker
from fastapi import FastAPI, HTTPException

app = FastAPI(title="DevOps Dashboard")
client = docker.from_env() # Tizimdagi Docker bilan ulanadi

@app.get("/containers")
def list_containers():
    """Barcha aktiv konteynerlarni ro'yxatini qaytaradi"""
    try:
        containers = client.containers.list(all=True)
        return [
            {
                "id": c.short_id,
                "name": c.name,
                "status": c.status,
                "image": c.image.tags[0] if c.image.tags else "unknown"
            }
            for c in containers
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))