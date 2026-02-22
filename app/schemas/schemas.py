from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ════════════════════════════════════════════
# SCHEMAS - USUARIO
# ════════════════════════════════════════════
class UsuarioLogin(BaseModel):
    email: str
    contraseña: str


class UsuarioBase(BaseModel):
    nombre: str
    email: str
    rol: str
    especialidad: Optional[str] = None
    telefono: Optional[str] = None


class UsuarioCreate(UsuarioBase):
    contraseña: str


class UsuarioResponse(UsuarioBase):
    id: int
    activo: bool
    creado_en: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    usuario: UsuarioResponse


# ════════════════════════════════════════════
# SCHEMAS - PACIENTE
# ════════════════════════════════════════════
class PacienteBase(BaseModel):
    nombre: str
    apellido: str
    documento: str
    telefono: str
    fecha_nacimiento: Optional[str] = None
    edad: Optional[int] = None
    genero: Optional[str] = None
    email: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    alergias: Optional[str] = None
    antecedentes_medicos: Optional[str] = None


class PacienteCreate(PacienteBase):
    pass


class PacienteUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    alergias: Optional[str] = None
    antecedentes_medicos: Optional[str] = None


class PacienteResponse(PacienteBase):
    id: int
    creado_en: datetime
    actualizado_en: datetime

    class Config:
        from_attributes = True


# ════════════════════════════════════════════
# SCHEMAS - HISTORIA CLÍNICA
# ════════════════════════════════════════════
class HistoriaClinicaBase(BaseModel):
    paciente_id: int
    doctor_id: int
    presion_arterial: Optional[str] = None
    frecuencia_cardiaca: Optional[int] = None
    temperatura: Optional[float] = None
    saturacion_o2: Optional[int] = None
    peso: Optional[float] = None
    talla: Optional[float] = None
    motivo_consulta: Optional[str] = None
    enfermedad_actual: Optional[str] = None
    diagnostico_principal: Optional[str] = None
    impresion: Optional[str] = None
    medicamentos_prescriptos: Optional[str] = None


class HistoriaClinicaCreate(HistoriaClinicaBase):
    pass


class HistoriaClinicaUpdate(BaseModel):
    presion_arterial: Optional[str] = None
    frecuencia_cardiaca: Optional[int] = None
    temperatura: Optional[float] = None
    saturacion_o2: Optional[int] = None
    peso: Optional[float] = None
    talla: Optional[float] = None
    motivo_consulta: Optional[str] = None
    enfermedad_actual: Optional[str] = None
    diagnostico_principal: Optional[str] = None
    impresion: Optional[str] = None
    medicamentos_prescriptos: Optional[str] = None
    plan_accion: Optional[str] = None
    proxima_cita: Optional[str] = None


class HistoriaClinicaResponse(HistoriaClinicaBase):
    id: int
    creado_en: datetime
    actualizado_en: datetime

    class Config:
        from_attributes = True


# ════════════════════════════════════════════
# SCHEMAS - CITA
# ════════════════════════════════════════════
class CitaBase(BaseModel):
    paciente_id: int
    doctor_id: int
    fecha: str
    hora: str
    especialidad: str
    motivo: Optional[str] = None
    estado: Optional[str] = "programada"


class CitaCreate(CitaBase):
    pass


class CitaUpdate(BaseModel):
    fecha: Optional[str] = None
    hora: Optional[str] = None
    especialidad: Optional[str] = None
    motivo: Optional[str] = None
    estado: Optional[str] = None


class CitaResponse(CitaBase):
    id: int
    creado_en: datetime
    actualizado_en: datetime

    class Config:
        from_attributes = True


# ════════════════════════════════════════════
# SCHEMAS - DOCUMENTO
# ════════════════════════════════════════════
class DocumentoBase(BaseModel):
    paciente_id: int
    nombre: str
    tipo: str
    descripcion: Optional[str] = None


class DocumentoCreate(DocumentoBase):
    ruta: str
    tamaño: Optional[int] = None


class DocumentoResponse(DocumentoBase):
    id: int
    tamaño: Optional[int]
    ruta: str
    creado_en: datetime

    class Config:
        from_attributes = True
