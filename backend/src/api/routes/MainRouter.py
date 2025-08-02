from fastapi import APIRouter
from api.routes.AirQualityRouter import air_quality_router

main_router = APIRouter(prefix="/api/v1")

main_router.include_router(air_quality_router)
