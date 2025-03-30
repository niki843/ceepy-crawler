from fastapi import APIRouter

from app.services.health_service import HealthService

router = APIRouter()

@router.get("isalive")
def is_alive():
    return {"status": HealthService.calculate_system_status()}

@router.get("system_status")
def get_system_status():
    return HealthService.get_system_stats()