import psutil
from fastapi import APIRouter

router = APIRouter()

@router.get("isalive")
def is_alive():
    return {"status": "alive"}

@router.get("system_status")
def get_system_status():
    return {
        "status": "alive",
        "cpu_usage": psutil.cpu_percent(),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent
    }