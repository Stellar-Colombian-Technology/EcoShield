from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class CoordinatesRequest(BaseModel):
    lat: float = Field(..., ge=-90, le=90, description="Latitud entre -90 y 90")
    lon: float = Field(..., ge=-180, le=180, description="Longitud entre -180 y 180")
    radius: Optional[float] = Field(default=5.0, ge=0.1, le=50.0, description="Radio en km para el análisis")

class AirQualityData(BaseModel):
    coordinates: Dict[str, float]
    timestamp: datetime
    no2_density: Optional[float] = Field(None, description="Densidad de NO2 en mol/m²")
    co_density: Optional[float] = Field(None, description="Densidad de CO en mol/m²")
    o3_density: Optional[float] = Field(None, description="Densidad de O3 en mol/m²")
    so2_density: Optional[float] = Field(None, description="Densidad de SO2 en mol/m²")
    ch4_density: Optional[float] = Field(None, description="Densidad de CH4 en mol/m²")
    hcho_density: Optional[float] = Field(None, description="Densidad de HCHO en mol/m²")
    air_quality_index: Optional[int] = Field(None, ge=0, le=500, description="Índice de calidad del aire (0-500)")
    air_quality_category: Optional[str] = Field(None, description="Categoría de calidad del aire")
    health_recommendations: Optional[str] = Field(None, description="Recomendaciones de salud")
    data_source: str = Field(default="Sentinel-5P", description="Fuente de los datos")
    analysis_radius_km: float = Field(..., description="Radio de análisis en kilómetros")

class AirQualityResponse(BaseModel):
    success: bool
    message: str
    data: Optional[AirQualityData] = None
    error: Optional[str] = None

class GenerateReportRequest(BaseModel):
    air_quality_data: AirQualityData
    report_title: Optional[str] = Field(default="Reporte de Calidad del Aire", description="Título del reporte")
    include_charts: Optional[bool] = Field(default=True, description="Incluir gráficos en el reporte")

class ReportResponse(BaseModel):
    success: bool
    message: str
    filename: Optional[str] = None
    error: Optional[str] = None