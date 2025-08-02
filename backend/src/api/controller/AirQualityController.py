from fastapi import HTTPException
from fastapi.responses import Response
from datetime import datetime

from api.dto.AirQuality.AirQualityDto import (
    CoordinatesRequest, 
    AirQualityResponse, 
    GenerateReportRequest, 
    ReportResponse
)
from core.service.AirQualityService import AirQualityService
from shared.errors.ApiResponse import ApiResponse

class AirQualityController:
    def __init__(self):
        self.air_quality_service = AirQualityService()
    
    async def get_air_quality_summary(self, coordinates: CoordinatesRequest) -> AirQualityResponse:
        """
        Controlador para obtener resumen de calidad del aire basado en coordenadas
        """
        try:
            if not (-90 <= coordinates.lat <= 90):
                raise HTTPException(
                    status_code=400, 
                    detail="La latitud debe estar entre -90 y 90 grados"
                )
            
            if not (-180 <= coordinates.lon <= 180):
                raise HTTPException(
                    status_code=400, 
                    detail="La longitud debe estar entre -180 y 180 grados"
                )
            
            if coordinates.radius <= 0 or coordinates.radius > 50:
                raise HTTPException(
                    status_code=400, 
                    detail="El radio debe estar entre 0.1 y 50 km"
                )
            
            air_quality_data = await self.air_quality_service.get_air_quality_summary(coordinates)
            
            return AirQualityResponse(
                success=True,
                message="Datos de calidad del aire obtenidos exitosamente",
                data=air_quality_data
            )
            
        except HTTPException:
            raise
        except Exception as e:
            return AirQualityResponse(
                success=False,
                message="Error interno del servidor",
                error=str(e)
            )
    
    async def generate_air_quality_report(self, request: GenerateReportRequest) -> Response:
        """
        Controlador para generar reporte PDF de calidad del aire
        """
        try:
            if not request.air_quality_data:
                raise HTTPException(
                    status_code=400,
                    detail="Los datos de calidad del aire son requeridos"
                )
            
            if not request.air_quality_data.coordinates:
                raise HTTPException(
                    status_code=400,
                    detail="Las coordenadas son requeridas en los datos"
                )
            
            pdf_content = await self.air_quality_service.generate_pdf_report(
                request.air_quality_data,
                request.report_title or "Reporte de Calidad del Aire"
            )
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            lat = request.air_quality_data.coordinates.get('lat', 0)
            lon = request.air_quality_data.coordinates.get('lon', 0)
            filename = f"reporte_calidad_aire_{lat:.4f}_{lon:.4f}_{timestamp}.pdf"
            
            return Response(
                content=pdf_content,
                media_type="application/pdf",
                headers={
                    "Content-Disposition": f"attachment; filename={filename}",
                    "Content-Type": "application/pdf"
                }
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error generando el reporte PDF: {str(e)}"
            )
    
    async def get_air_quality_report_info(self, request: GenerateReportRequest) -> ReportResponse:
        """
        Controlador alternativo que retorna información del reporte sin generar el PDF
        Útil para validar antes de la generación
        """
        try:
            if not request.air_quality_data or not request.air_quality_data.coordinates:
                raise HTTPException(
                    status_code=400,
                    detail="Datos de calidad del aire incompletos"
                )
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            lat = request.air_quality_data.coordinates.get('lat', 0)
            lon = request.air_quality_data.coordinates.get('lon', 0)
            filename = f"reporte_calidad_aire_{lat:.4f}_{lon:.4f}_{timestamp}.pdf"
            
            return ReportResponse(
                success=True,
                message="Información del reporte generada exitosamente",
                filename=filename
            )
            
        except HTTPException:
            raise
        except Exception as e:
            return ReportResponse(
                success=False,
                message="Error validando datos para el reporte",
                error=str(e)
            )