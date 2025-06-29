from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime

# Configuración de la aplicación
app = FastAPI(
    title="Market Data API",
    description="API para datos de mercado por sectores y países",
    version="1.0.0"
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://comercio-internacional-react.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic
class MarketResponse(BaseModel):
    success: bool
    data: List[Dict[str, Any]]
    timestamp: datetime

# Datos estructurados de los sectores
sectors_data = [
    { "label": "Educación", "data": [65, 68, 64, 70, 72, 75, 77, 80], "color": "rgb(255, 99, 132)" },
    { "label": "Minería", "data": [80, 85, 72, 68, 75, 82, 88, 90], "color": "rgb(54, 162, 235)" },
    { "label": "Salud", "data": [60, 63, 75, 78, 76, 80, 82, 85], "color": "rgb(75, 192, 192)" },
    { "label": "Tecnología", "data": [85, 92, 98, 105, 110, 118, 125, 130], "color": "rgb(153, 102, 255)" },
    { "label": "Agricultura", "data": [70, 73, 68, 72, 75, 74, 77, 80], "color": "rgb(255, 159, 64)" },
    { "label": "Turismo", "data": [75, 80, 55, 40, 65, 85, 95, 100], "color": "rgb(255, 205, 86)" },
    { "label": "Manufactura", "data": [82, 85, 78, 80, 83, 86, 89, 92], "color": "rgb(201, 203, 207)" },
    { "label": "Energía Renovable", "data": [50, 55, 60, 70, 75, 80, 90, 95], "color": "rgb(255, 205, 220)" },
    { "label": "Construcción", "data": [85, 88, 92, 100, 110, 120, 130, 140], "color": "rgb(0, 255, 0)" },
    { "label": "Retail", "data": [90, 93, 95, 98, 100, 105, 110, 115], "color": "rgb(255, 140, 0)" },
    { "label": "Logística", "data": [80, 85, 90, 100, 110, 115, 120, 125], "color": "rgb(128, 0, 128)" },
    { "label": "Telecomunicaciones", "data": [100, 105, 110, 115, 120, 125, 130, 135], "color": "rgb(0, 255, 255)" },
    { "label": "Automotriz", "data": [55, 60, 65, 70, 75, 80, 85, 90], "color": "rgb(255, 99, 71)" },
    { "label": "Joyería", "data": [50, 55, 60, 65, 70, 75, 80, 85], "color": "rgb(255, 159, 64)" }
]

countries_data = [
    { "label": "India", "data": [60, 63, 75, 80, 85, 90, 95, 100], "color": "rgb(255, 99, 132)" },
    { "label": "China", "data": [70, 75, 85, 90, 95, 100, 105, 110], "color": "rgb(54, 162, 235)" },
    { "label": "Brasil", "data": [55, 58, 65, 70, 75, 80, 85, 90], "color": "rgb(75, 192, 192)" },
    { "label": "Estados Unidos", "data": [80, 85, 95, 100, 105, 110, 115, 120], "color": "rgb(153, 102, 255)" },
    { "label": "Japón", "data": [50, 55, 60, 65, 70, 75, 80, 85], "color": "rgb(255, 159, 64)" }
]

# Rutas de la API
@app.get("/")
async def root():
    """Endpoint raíz con información de la API"""
    return {
        "message": "Market Data API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "sectors": "/identificacion-mercados",
            "countries": "/comportamiento-mercado"
        }
    }

@app.get("/identificacion-mercados", response_model=MarketResponse)
async def get_market_identification():
    """Obtener datos de identificación de mercados por sectores"""
    try:
        return MarketResponse(
            success=True,
            data=sectors_data,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo datos de sectores: {str(e)}")

@app.get("/comportamiento-mercado", response_model=MarketResponse)
async def get_market_behavior():
    """Obtener datos de comportamiento de mercado por países"""
    try:
        return MarketResponse(
            success=True,
            data=countries_data,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo datos de países: {str(e)}")

@app.get("/health")
async def health_check():
    """Verificar el estado de la API"""
    return {
        "status": "healthy",
        "message": "API funcionando correctamente",
        "timestamp": datetime.now(),
        "data_loaded": {
            "sectors": len(sectors_data),
            "countries": len(countries_data)
        }
    }

# Rutas adicionales para obtener estadísticas
@app.get("/stats")
async def get_stats():
    """Obtener estadísticas generales de los datos"""
    try:
        # Calcular estadísticas de sectores
        sector_stats = {}
        for sector in sectors_data:
            sector_stats[sector["label"]] = {
                "min": min(sector["data"]),
                "max": max(sector["data"]),
                "avg": round(sum(sector["data"]) / len(sector["data"]), 2)
            }
        
        # Calcular estadísticas de países
        country_stats = {}
        for country in countries_data:
            country_stats[country["label"]] = {
                "min": min(country["data"]),
                "max": max(country["data"]),
                "avg": round(sum(country["data"]) / len(country["data"]), 2)
            }
        
        return {
            "success": True,
            "sectors": sector_stats,
            "countries": country_stats,
            "timestamp": datetime.now()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculando estadísticas: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)