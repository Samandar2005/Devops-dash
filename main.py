import docker
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi import WebSocket
import asyncio

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
    

class ContainerRequest(BaseModel):
    image: str
    port: int

@app.post("/containers/run")
def run_container(req: ContainerRequest):
    """Yangi konteyner ko'tarish (Masalan: nginx)"""
    try:
        container = client.containers.run(
            req.image,
            detach=True,
            ports={'80/tcp': req.port} # Ichki 80 portni tashqi portga ulash
        )
        return {"message": "Konteyner ishga tushdi", "id": container.short_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/containers/{container_id}/stop")
def stop_container(container_id: str):
    """Konteynerni to'xtatish"""
    try:
        container = client.containers.get(container_id)
        container.stop()
        return {"message": f"Konteyner {container_id} to'xtatildi"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/containers/{container_id}/logs")
async def websocket_endpoint(websocket: WebSocket, container_id: str):
    await websocket.accept()
    try:
        container = client.containers.get(container_id)
        # Loglarni stream qilish (jonli oqim)
        for line in container.logs(stream=True, tail=10):
            await websocket.send_text(line.decode("utf-8"))
            await asyncio.sleep(0.1) # Kichik pauza
    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")
        await websocket.close()


@app.get("/containers/{container_id}/stats")
def get_stats(container_id: str):
    try:
        container = client.containers.get(container_id)
        stats = container.stats(stream=False)
        # Bu yerda Docker stats JSON qaytaradi, uni frontendda parslash kerak
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

