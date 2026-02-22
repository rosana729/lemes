from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.core.config import get_settings
from app.core.database import Base, engine, get_db
from app.core.whatsapp import enviar_whatsapp_simulado
from app.core.security import obtener_hash_contraseña
from app.models.models import Usuario, Paciente
from app.routes import api, api_v2
from pathlib import Path
from sqlalchemy.orm import Session

settings = get_settings()

# Modelo para enviar mensajes
class MensajeWhatsApp(BaseModel):
    numero: str
    mensaje: str
    fecha_cita: str = None
    hora_cita: str = None
    especialidad: str = None

# Crear tablas
Base.metadata.create_all(bind=engine)

# Crear aplicación
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ════════════════════════════════════════════
# CREAR DATOS DE EJEMPLO
# ════════════════════════════════════════════

@app.on_event("startup")
def crear_datos_ejemplo():
    """Crea usuarios y pacientes de ejemplo"""
    db = next(get_db())
    
    # Verificar si ya existen datos
    if db.query(Usuario).count() > 0:
        return
    
    # Crear usuarios
    usuarios = [
        Usuario(
            nombre="Dr. Carlos Rodríguez",
            email="doctor@clinica.com",
            contraseña=obtener_hash_contraseña("123456"),
            rol="doctor",
            especialidad="Medicina General y Familiar",
            telefono="+54 9 3756505366",
            activo=True
        ),
        Usuario(
            nombre="Catalina García",
            email="secretaria@clinica.com",
            contraseña=obtener_hash_contraseña("123456"),
            rol="secretaria",
            telefono="+54 9 3812345678",
            activo=True
        ),
        Usuario(
            nombre="Admin Sistema",
            email="admin@clinica.com",
            contraseña=obtener_hash_contraseña("123456"),
            rol="admin",
            telefono="+54 9 3555555555",
            activo=True
        ),
    ]
    
    for usuario in usuarios:
        db.add(usuario)
    
    db.commit()
    
    # Crear pacientes de ejemplo
    pacientes = [
        Paciente(
            nombre="Juan", apellido="Martínez",
            documento="1234567-8",
            telefono="+54 9 3756505366",
            fecha_nacimiento="2019-05-15",
            edad=5, genero="M",
            email="juan@example.com",
            ciudad="La Plata",
            alergias="Penicilina"
        ),
        Paciente(
            nombre="María", apellido="López",
            documento="9876543-2",
            telefono="+54 9 3812345678",
            fecha_nacimiento="2021-03-20",
            edad=3, genero="F",
            email="maria@example.com",
            ciudad="La Plata",
            alergias="Ninguna"
        ),
        Paciente(
            nombre="Carlos", apellido="Ruiz",
            documento="5555555-5",
            telefono="+54 9 3654321098",
            fecha_nacimiento="2022-07-10",
            edad=2, genero="M",
            email="carlos@example.com",
            ciudad="La Plata",
            alergias="Aspirina"
        ),
        Paciente(
            nombre="Sofia", apellido="Herrera",
            documento="4444444-4",
            telefono="+54 9 3555555555",
            fecha_nacimiento="2020-11-25",
            edad=4, genero="F",
            email="sofia@example.com",
            ciudad="La Plata",
            alergias="Ninguna"
        ),
        Paciente(
            nombre="Daniel", apellido="Vargas",
            documento="3333333-3",
            telefono="+54 9 3666666666",
            fecha_nacimiento="2018-01-30",
            edad=6, genero="M",
            email="daniel@example.com",
            ciudad="La Plata",
            alergias="Ninguna"
        ),
        Paciente(
            nombre="Andrea", apellido="García",
            documento="2222222-2",
            telefono="+54 9 3777777777",
            fecha_nacimiento="2023-09-05",
            edad=1, genero="F",
            email="andrea@example.com",
            ciudad="La Plata",
            alergias="Antibióticos"
        ),
    ]
    
    for paciente in pacientes:
        db.add(paciente)
    
    db.commit()
    print("✅ Datos de ejemplo creados correctamente")


# ════════════════════════════════════════════
# HEALTH CHECK
# ════════════════════════════════════════════

@app.get("/", tags=["health"])
def root():
    """Servir el index HTML principal"""
    index_path = Path(__file__).parent / "index.html"
    if index_path.exists():
        return FileResponse(index_path, media_type="text/html")
    return {"error": "Index no encontrado"}


@app.get("/health", tags=["health"])
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.api_title,
        "version": settings.api_version
    }




# ════════════════════════════════════════════
# FRONTEND
# ════════════════════════════════════════════

@app.get("/frontend", tags=["frontend"])
def get_frontend():
    """Servir el frontend HTML de la clínica"""
    frontend_path = Path(__file__).parent / "frontend.html"
    if frontend_path.exists():
        return FileResponse(frontend_path, media_type="text/html")
    return {"error": "Frontend no encontrado"}


@app.get("/index", tags=["frontend"])
def get_index():
    """Servir el index HTML"""
    index_path = Path(__file__).parent / "frontend.html"
    if index_path.exists():
        return FileResponse(index_path, media_type="text/html")
    return {"error": "Index no encontrado"}


@app.get("/clinica", tags=["frontend"])
def get_clinica_completa():
    """Servir la clínica completa con roles de usuario"""
    clinica_path = Path(__file__).parent / "clinica_completa.html"
    if clinica_path.exists():
        return FileResponse(clinica_path, media_type="text/html")
    return {"error": "Clínica no encontrada"}


@app.get("/admin", tags=["frontend"])
def get_admin():
    """Servir el panel administrativo con login"""
    admin_path = Path(__file__).parent / "admin.html"
    if admin_path.exists():
        return FileResponse(admin_path, media_type="text/html")
    return {"error": "Admin no encontrado"}


@app.get("/sistema", tags=["frontend"])
def get_sistema():
    """Servir el sistema con recordatorios"""
    sistema_path = Path(__file__).parent / "sistema.html"
    if sistema_path.exists():
        return FileResponse(sistema_path, media_type="text/html")
    return {"error": "Sistema no encontrado"}


@app.get("/historia-clinica", tags=["frontend"])
def get_historia_clinica():
    """Servir la vista profesional de historia clínica"""
    historia_path = Path(__file__).parent / "historia_clinica_profesional.html"
    if historia_path.exists():
        return FileResponse(historia_path, media_type="text/html")
    return {"error": "Historia clínica no encontrada"}


@app.get("/api.js", tags=["frontend"])
def get_api_js():
    """Servir el cliente API JavaScript"""
    api_js_path = Path(__file__).parent / "api.js"
    if api_js_path.exists():
        return FileResponse(api_js_path, media_type="application/javascript")
    return {"error": "API JS no encontrado"}


# ════════════════════════════════════════════
# INCLUIR RUTAS
# ════════════════════════════════════════════

app.include_router(api.router)
app.include_router(api_v2.router)


# ════════════════════════════════════════════
# WHATSAPP - CITAS Y RECORDATORIOS
# ════════════════════════════════════════════

@app.post("/api/whatsapp/enviar-cita", tags=["whatsapp"])
def enviar_cita_whatsapp(datos: MensajeWhatsApp):
    """
    Envía confirmación de cita a WhatsApp
    
    Detecta automáticamente el país por el código telefónico:
    - +54 = Argentina
    - +591 = Bolivia
    - +56 = Chile
    - +57 = Colombia
    - etc.
    """
    try:
        numero = datos.numero.replace(" ", "").replace("-", "")
        
        # Detectar país
        paises = {
            "54": "🇦🇷 Argentina",
            "591": "🇧🇴 Bolivia",
            "56": "🇨🇱 Chile",
            "57": "🇨🇴 Colombia",
            "55": "🇧🇷 Brasil",
            "58": "🇻🇪 Venezuela",
            "51": "🇵🇪 Perú",
            "595": "🇵🇾 Paraguay",
            "598": "🇺🇾 Uruguay",
        }
        
        # Extraer código de país
        codigo = numero[1:3] if numero.startswith("+") else numero[:2]
        pais = paises.get(codigo, "País desconocido")
        
        # Crear mensaje con datos de cita
        mensaje = f"""¡Hola! 👋

Confirmación de cita en Clínica Pediátrica

📅 FECHA: {datos.fecha_cita}
⏰ HORA: {datos.hora_cita}
🏥 ESPECIALIDAD: {datos.especialidad}
🌍 PAÍS: {pais}

Por favor, confirma tu asistencia.
¡Te esperamos! 🏥❤️"""
        
        # Enviar mensaje
        resultado = enviar_whatsapp_simulado(numero, mensaje)
        
        return {
            "success": True,
            "mensaje": "Cita enviada automáticamente a WhatsApp",
            "numero": numero,
            "pais": pais,
            "resultado": resultado
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al enviar: {str(e)}")


# ════════════════════════════════════════════
# MANEJADORES DE ERRORES
# ════════════════════════════════════════════

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Manejador genérico de errores"""
    return JSONResponse(
        status_code=500,
        content={"detail": f"Error interno del servidor: {str(exc)}"},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
