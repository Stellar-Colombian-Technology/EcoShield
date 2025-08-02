from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import Response

from api.dto.AirQuality.AirQualityDto import (
    CoordinatesRequest, 
    AirQualityResponse, 
    GenerateReportRequest, 
    ReportResponse
)
from api.controller.AirQualityController import AirQualityController

air_quality_router = APIRouter(
    prefix="/air-quality",
    tags=["Air Quality"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"}
    }
)

air_quality_controller = AirQualityController()

@air_quality_router.post(
    "/summary", 
    response_model=AirQualityResponse,
    summary="Obtener resumen de calidad del aire",
    description="""
    Obtiene un resumen detallado de la calidad del aire basado en coordenadas geográficas.
    
    **Parámetros:**
    - **lat**: Latitud (entre -90 y 90)
    - **lon**: Longitud (entre -180 y 180)  
    - **radius**: Radio de análisis en km (opcional, por defecto 5km)
    
    **Retorna:**
    - Datos de concentración de contaminantes (NO2, CO, O3, SO2, CH4, HCHO)
    - Índice de calidad del aire (AQI)
    - Categoría de calidad del aire
    - Recomendaciones de salud
    """
)
async def get_air_quality_summary(coordinates: CoordinatesRequest) -> AirQualityResponse:
    """
    Endpoint para obtener resumen de calidad del aire basado en coordenadas
    """
    return await air_quality_controller.get_air_quality_summary(coordinates)

@air_quality_router.post(
    "/report",
    summary="Generar reporte PDF de calidad del aire",
    description="""
    Genera un reporte PDF detallado con los datos de calidad del aire.
    
    **Parámetros:**
    - **air_quality_data**: Datos obtenidos del endpoint /summary
    - **report_title**: Título personalizado para el reporte (opcional)
    - **include_charts**: Incluir gráficos en el reporte (opcional, por defecto true)
    
    **Retorna:**
    - Archivo PDF para descarga con el reporte completo
    """
)
async def generate_air_quality_report(request: GenerateReportRequest) -> Response:
    """
    Endpoint para generar y descargar reporte PDF de calidad del aire
    """
    return await air_quality_controller.generate_air_quality_report(request)

@air_quality_router.post(
    "/report/info",
    response_model=ReportResponse,
    summary="Validar datos para reporte",
    description="""
    Valida los datos de calidad del aire y retorna información del reporte que se generaría.
    Útil para validar antes de generar el PDF real.
    """
)
async def get_report_info(request: GenerateReportRequest) -> ReportResponse:
    """
    Endpoint para validar datos y obtener información del reporte sin generarlo
    """
    return await air_quality_controller.get_air_quality_report_info(request)