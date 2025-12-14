from fastapi import FastAPI

app = FastAPI(title="DevOps Dashboard")

@app.get("/")
def read_root():
    return {"message": "Tizim ishlayapti!"}