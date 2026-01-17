from fastapi import FastAPI
from fastapi.testclient import TestClient
import httpx

def test_minimal():
    app = FastAPI()
    @app.get("/")
    def read_root():
        return {"msg": "Hello World"}
    
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"msg": "Hello World"}

def test_httpx_version():
    print(f"HTTPX version in test: {httpx.__version__}")
