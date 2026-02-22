from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class RolEnum(str, enum.Enum):
    doctor = "doctor"
    secretaria = "secretaria"
    admin = "admin"

class EstadoCitaEnum(str, enum.Enum):
    programada = "programada"
    realizada = "realizada"
    cancelada = "cancelada"

# ════════════════════════════════════════════
# MODELO: USUARIO (Doctor, Secretaria, Admin)
# ════════════════════════════════════════════
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    contraseña = Column(String(255), nullable=False)
    rol = Column(Enum(RolEnum), default=RolEnum.doctor, nullable=False)
    especialidad = Column(String(100), nullable=True)
    telefono = Column(String(20), nullable=True)
    activo = Column(Boolean, default=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    citas = relationship("Cita", back_populates="doctor")


# ════════════════════════════════════════════
# MODELO: PACIENTE
# ════════════════════════════════════════════
class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    documento = Column(String(20), unique=True, index=True, nullable=False)
    fecha_nacimiento = Column(String(10), nullable=True)
    edad = Column(Integer, nullable=True)
    genero = Column(String(10), nullable=True)
    telefono = Column(String(20), nullable=False)
    email = Column(String(100), nullable=True)
    direccion = Column(String(200), nullable=True)
    ciudad = Column(String(100), nullable=True)
    alergias = Column(Text, nullable=True)
    antecedentes_medicos = Column(Text, nullable=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    actualizado_en = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    historias_clinicas = relationship("HistoriaClinica", back_populates="paciente", cascade="all, delete-orphan")
    citas = relationship("Cita", back_populates="paciente", cascade="all, delete-orphan")
    documentos = relationship("Documento", back_populates="paciente", cascade="all, delete-orphan")


# ════════════════════════════════════════════
# MODELO: HISTORIA CLÍNICA
# ════════════════════════════════════════════
class HistoriaClinica(Base):
    __tablename__ = "historias_clinicas"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False, index=True)
    doctor_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)
    
    # Signos Vitales
    presion_arterial = Column(String(20), nullable=True)
    frecuencia_cardiaca = Column(Integer, nullable=True)
    temperatura = Column(Float, nullable=True)
    saturacion_o2 = Column(Integer, nullable=True)
    peso = Column(Float, nullable=True)
    talla = Column(Float, nullable=True)
    imc = Column(Float, nullable=True)
    
    # Anamnesis
    motivo_consulta = Column(Text, nullable=True)
    enfermedad_actual = Column(Text, nullable=True)
    sintomas_principales = Column(Text, nullable=True)
    
    # Antecedentes
    antecedentes_personales = Column(Text, nullable=True)
    antecedentes_familiares = Column(Text, nullable=True)
    medicacion_actual = Column(Text, nullable=True)
    alergias_medicamentos = Column(Text, nullable=True)
    habitos = Column(Text, nullable=True)
    
    # Examen Físico
    examen_general = Column(Text, nullable=True)
    sistema_cardiovascular = Column(Text, nullable=True)
    sistema_respiratorio = Column(Text, nullable=True)
    abdomen = Column(Text, nullable=True)
    neurologia = Column(Text, nullable=True)
    
    # Estudios Complementarios
    laboratorio = Column(Text, nullable=True)
    imagenes = Column(Text, nullable=True)
    otros_estudios = Column(Text, nullable=True)
    
    # Diagnóstico
    diagnostico_principal = Column(Text, nullable=True)
    diagnosticos_secundarios = Column(Text, nullable=True)
    codigos_cie10 = Column(Text, nullable=True)
    
    # Impresión Diagnóstica
    impresion = Column(Text, nullable=True)
    plan_accion = Column(Text, nullable=True)
    
    # Tratamiento
    medicamentos_prescriptos = Column(Text, nullable=True)
    indicaciones = Column(Text, nullable=True)
    proxima_cita = Column(String(10), nullable=True)
    
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    actualizado_en = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    paciente = relationship("Paciente", back_populates="historias_clinicas")
    doctor = relationship("Usuario")


# ════════════════════════════════════════════
# MODELO: CITA
# ════════════════════════════════════════════
class Cita(Base):
    __tablename__ = "citas"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False, index=True)
    doctor_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)
    
    fecha = Column(String(10), nullable=False)
    hora = Column(String(5), nullable=False)
    especialidad = Column(String(100), nullable=False)
    motivo = Column(Text, nullable=True)
    estado = Column(Enum(EstadoCitaEnum), default=EstadoCitaEnum.programada)
    notas = Column(Text, nullable=True)
    
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    actualizado_en = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    paciente = relationship("Paciente", back_populates="citas")
    doctor = relationship("Usuario", back_populates="citas")


# ════════════════════════════════════════════
# MODELO: DOCUMENTO/ADJUNTO
# ════════════════════════════════════════════
class Documento(Base):
    __tablename__ = "documentos"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False, index=True)
    historia_clinica_id = Column(Integer, ForeignKey("historias_clinicas.id"), nullable=True)
    
    nombre = Column(String(200), nullable=False)
    tipo = Column(String(50), nullable=False)
    tamaño = Column(Integer, nullable=True)
    ruta = Column(String(300), nullable=False)
    descripcion = Column(Text, nullable=True)
    
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    paciente = relationship("Paciente", back_populates="documentos")
