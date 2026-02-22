from fastapi import APIRouter

# Las rutas antiguas se han movido a api_v2.py
# Este archivo se mantiene por compatibilidad

router = APIRouter(prefix="/api", tags=["api"])
