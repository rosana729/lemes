from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Usuario, Paciente, HistoriaClinica, Cita, Documento
from app.schemas.schemas import (
    UsuarioLogin, UsuarioCreate, UsuarioResponse, TokenResponse,
    PacienteCreate, PacienteResponse, PacienteUpdate,
    HistoriaClinicaCreate, HistoriaClinicaResponse, HistoriaClinicaUpdate,
    CitaCreate, CitaResponse, CitaUpdate
)
from app.core.security import (
    verificar_contraseña, obtener_hash_contraseña, 
    crear_token_acceso, verificar_token
)

router = APIRouter(prefix="/api", tags=["api"])

# ════════════════════════════════════════════
# LOGIN
# ════════════════════════════════════════════

@router.post("/login", response_model=TokenResponse)
def login(credenciales: UsuarioLogin, db: Session = Depends(get_db)):
    """Login - Retorna token JWT"""
    usuario = db.query(Usuario).filter(Usuario.email == credenciales.email).first()
    
    if not usuario or not verificar_contraseña(credenciales.contraseña, usuario.contraseña):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos"
        )
    
    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    
    # Crear token
    token = crear_token_acceso({
        "email": usuario.email,
        "rol": usuario.rol,
        "id": usuario.id
    })
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": usuario
    }


# ════════════════════════════════════════════
# PACIENTES
# ════════════════════════════════════════════

@router.post("/pacientes", response_model=PacienteResponse)
def crear_paciente(paciente: PacienteCreate, db: Session = Depends(get_db)):
    """Crear nuevo paciente"""
    # Verificar si el documento ya existe
    existe = db.query(Paciente).filter(Paciente.documento == paciente.documento).first()
    if existe:
        raise HTTPException(status_code=400, detail="Documento ya registrado")
    
    nuevo_paciente = Paciente(**paciente.dict())
    db.add(nuevo_paciente)
    db.commit()
    db.refresh(nuevo_paciente)
    return nuevo_paciente


@router.get("/pacientes", response_model=list[PacienteResponse])
def listar_pacientes(db: Session = Depends(get_db)):
    """Listar todos los pacientes"""
    return db.query(Paciente).all()


@router.get("/pacientes/{paciente_id}", response_model=PacienteResponse)
def obtener_paciente(paciente_id: int, db: Session = Depends(get_db)):
    """Obtener paciente por ID"""
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return paciente


@router.put("/pacientes/{paciente_id}", response_model=PacienteResponse)
def actualizar_paciente(paciente_id: int, paciente_update: PacienteUpdate, db: Session = Depends(get_db)):
    """Actualizar paciente"""
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    datos = paciente_update.dict(exclude_unset=True)
    for campo, valor in datos.items():
        setattr(paciente, campo, valor)
    
    db.commit()
    db.refresh(paciente)
    return paciente


@router.delete("/pacientes/{paciente_id}")
def eliminar_paciente(paciente_id: int, db: Session = Depends(get_db)):
    """Eliminar paciente"""
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    db.delete(paciente)
    db.commit()
    return {"mensaje": "Paciente eliminado correctamente"}


# ════════════════════════════════════════════
# HISTORIAS CLÍNICAS
# ════════════════════════════════════════════

@router.post("/historias-clinicas", response_model=HistoriaClinicaResponse)
def crear_historia_clinica(historia: HistoriaClinicaCreate, db: Session = Depends(get_db)):
    """Crear nueva historia clínica"""
    nueva_historia = HistoriaClinica(**historia.dict())
    db.add(nueva_historia)
    db.commit()
    db.refresh(nueva_historia)
    return nueva_historia


@router.get("/historias-clinicas/paciente/{paciente_id}", response_model=list[HistoriaClinicaResponse])
def obtener_historias_paciente(paciente_id: int, db: Session = Depends(get_db)):
    """Obtener historias clínicas de un paciente"""
    return db.query(HistoriaClinica).filter(HistoriaClinica.paciente_id == paciente_id).all()


@router.get("/historias-clinicas/{historia_id}", response_model=HistoriaClinicaResponse)
def obtener_historia(historia_id: int, db: Session = Depends(get_db)):
    """Obtener una historia clínica"""
    historia = db.query(HistoriaClinica).filter(HistoriaClinica.id == historia_id).first()
    if not historia:
        raise HTTPException(status_code=404, detail="Historia clínica no encontrada")
    return historia


@router.put("/historias-clinicas/{historia_id}", response_model=HistoriaClinicaResponse)
def actualizar_historia(historia_id: int, historia_update: HistoriaClinicaUpdate, db: Session = Depends(get_db)):
    """Actualizar historia clínica"""
    historia = db.query(HistoriaClinica).filter(HistoriaClinica.id == historia_id).first()
    if not historia:
        raise HTTPException(status_code=404, detail="Historia clínica no encontrada")
    
    datos = historia_update.dict(exclude_unset=True)
    for campo, valor in datos.items():
        setattr(historia, campo, valor)
    
    db.commit()
    db.refresh(historia)
    return historia


# ════════════════════════════════════════════
# CITAS
# ════════════════════════════════════════════

@router.post("/citas", response_model=CitaResponse)
def crear_cita(cita: CitaCreate, db: Session = Depends(get_db)):
    """Crear nueva cita"""
    nueva_cita = Cita(**cita.dict())
    db.add(nueva_cita)
    db.commit()
    db.refresh(nueva_cita)
    return nueva_cita


@router.get("/citas/doctor/{doctor_id}", response_model=list[CitaResponse])
def obtener_citas_doctor(doctor_id: int, db: Session = Depends(get_db)):
    """Obtener citas de un doctor"""
    return db.query(Cita).filter(Cita.doctor_id == doctor_id).all()


@router.get("/citas/paciente/{paciente_id}", response_model=list[CitaResponse])
def obtener_citas_paciente(paciente_id: int, db: Session = Depends(get_db)):
    """Obtener citas de un paciente"""
    return db.query(Cita).filter(Cita.paciente_id == paciente_id).all()


@router.put("/citas/{cita_id}", response_model=CitaResponse)
def actualizar_cita(cita_id: int, cita_update: CitaUpdate, db: Session = Depends(get_db)):
    """Actualizar cita"""
    cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    
    datos = cita_update.dict(exclude_unset=True)
    for campo, valor in datos.items():
        setattr(cita, campo, valor)
    
    db.commit()
    db.refresh(cita)
    return cita


@router.delete("/citas/{cita_id}")
def eliminar_cita(cita_id: int, db: Session = Depends(get_db)):
    """Eliminar cita"""
    cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    
    db.delete(cita)
    db.commit()
    return {"mensaje": "Cita eliminada correctamente"}


# ════════════════════════════════════════════
# ESTADÍSTICAS
# ════════════════════════════════════════════

@router.get("/estadisticas")
def obtener_estadisticas(db: Session = Depends(get_db)):
    """Obtener estadísticas generales"""
    total_pacientes = db.query(Paciente).count()
    total_citas = db.query(Cita).count()
    total_doctores = db.query(Usuario).filter(Usuario.rol == "doctor").count()
    
    return {
        "total_pacientes": total_pacientes,
        "total_citas": total_citas,
        "total_doctores": total_doctores
    }


@router.get("/usuarios", response_model=list[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    """Listar todos los usuarios"""
    return db.query(Usuario).all()
