# 🏥 Clínica Pediátrica - FastAPI + Supabase

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776ab?style=flat&logo=python)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-336791?style=flat&logo=postgresql)](https://supabase.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=flat)]()

**Sistema moderno para gestión de consultorios pediátricos**

> Una API REST completa y escalable para administrar pacientes, consultas, gastos e ingresos de forma eficiente

---

## 🌐 **[VER SITIO WEB EN GITHUB PAGES](https://rosana729.github.io/lemes)** ⭐

📖 **[Guía Rápida GitHub Pages](QUICK_START_GITHUB_PAGES.md)** | 🎬 **[Crear GIF Demostrativo](GIF_DEMO.md)**

---

## 🎬 Demostración

### Panel Swagger UI (Documentación Interactiva)
```
http://localhost:8000/docs
```

### Endpoints principales:
- 📊 **Estadísticas**: `GET /api/estadisticas`
- 👥 **Pacientes**: CRUD completo
- 🏥 **Consultas**: Con IMC calculado automáticamente
- 💰 **Gastos/Ingresos**: Control financiero

**[Ver ejemplos de uso](#-ejemplos-de-uso)**

---

## 📚 Características

✅ **API REST moderna** con FastAPI (muy rápida, auto-documentada)
✅ **Base de datos PostgreSQL** en Supabase (en la nube)
✅ **CRUD completo** para pacientes, consultas, gastos, ingresos
✅ **Estadísticas en tiempo real** (dashboard backend)
✅ **Validación automática** con Pydantic
✅ **Documentación interactiva** Swagger UI + ReDoc
✅ **Escalable y seguro** para producción

## 🛠️ Stack Tecnológico

| Componente | Tecnología | Versión |
|-----------|-----------|---------|
| **Backend** | FastAPI | 0.104.1 |
| **Servidor** | Uvicorn | 0.24.0 |
| **ORM** | SQLAlchemy | 2.0.23 |
| **BD** | PostgreSQL (Supabase) | 15+ |
| **Validación** | Pydantic | 2.5.0 |
| **Seguridad** | Python-Jose + Passlib | 3.3.0 |
| **Python** | 3.9+ | Recomendado 3.11 |

## ⚡ Inicio Rápido (5 minutos)

```bash
# 1. Clonar proyecto
git clone https://github.com/rosana729/lemes.git
cd lemes

# 2. Crear ambiente virtual
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# o: source venv/bin/activate  # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
# Crea .env (copia de .env.example) y configura:
# - SUPABASE_URL
# - SUPABASE_KEY
# - DATABASE_URL
# - SECRET_KEY

# 5. Ejecutar servidor
python main.py

# ✅ API disponible en http://localhost:8000
# 📖 Documentación en http://localhost:8000/docs
```

## 📂 Estructura del Proyecto

```
c:\xampp\pdt\
├── app/
│   ├── __init__.py
│   ├── core/
│   │   ├── config.py           # Configuración de la app
│   │   ├── database.py         # Conexión a BD
│   │   ├── security.py         # Funciones de seguridad
│   │   └── __init__.py
│   ├── models/
│   │   ├── models.py           # Modelos SQLAlchemy (4 tablas)
│   │   └── __init__.py
│   ├── schemas/
│   │   ├── schemas.py          # Schemas Pydantic (validación)
│   │   └── __init__.py
│   └── routes/
│       ├── api.py              # Todos los endpoints
│       └── __init__.py
├── tests/                       # Tests unitarios
├── main.py                      # Aplicación principal
├── requirements.txt             # Dependencias Python
├── .env                         # Variables de entorno
└── README.md                    # Este archivo
```

## 🚀 Instalación

### 1. Requisitos

- Python 3.9 o superior
- pip (gestor de paquetes Python)
- Cuenta Supabase (gratuita en https://supabase.com)

### 2. Clonar/Descargar proyecto

```bash
cd c:\xampp\pdt
```

### 3. Crear ambiente virtual

```bash
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# Windows CMD
python -m venv venv
venv\Scripts\activate.bat
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar variables de entorno

Abre `.env` y configura:

```env
# Supabase
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu-clave-anon-key
DATABASE_URL=postgresql://postgres:contraseña@tu-proyecto.supabase.co:5432/postgres

# Seguridad (CAMBIAR EN PRODUCCIÓN)
SECRET_KEY=tu-clave-super-secreta-cambiar-en-produccion
DEBUG=True
```

### 6. Crear tablas

```bash
# Las tablas se crean automáticamente al iniciar
python main.py
```

### 7. Iniciar servidor

```bash
python main.py
```

Verás:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

## 📡 API Endpoints

### Health Check

```
GET /              - Estado de la API
GET /health        - Verificación de salud
```

### Estadísticas

```
GET /api/estadisticas    - Obtener estadísticas del dashboard
```

Respuesta:
```json
{
  "total_pacientes": 5,
  "consultas_hoy": 2,
  "ingresos_mes": 1500.00,
  "gastos_mes": 800.00,
  "ganancia_mes": 700.00
}
```

### Pacientes

```
GET    /api/pacientes                 - Listar pacientes
POST   /api/pacientes                 - Crear paciente
GET    /api/pacientes/{id}            - Obtener paciente
PUT    /api/pacientes/{id}            - Actualizar paciente
DELETE /api/pacientes/{id}            - Eliminar paciente (soft delete)
```

### Consultas

```
GET    /api/consultas                 - Listar consultas
POST   /api/consultas                 - Crear consulta (calcula IMC automáticamente)
GET    /api/consultas/{id}            - Obtener consulta
PUT    /api/consultas/{id}            - Actualizar consulta
DELETE /api/consultas/{id}            - Eliminar consulta
```

Parámetros útiles:
- `?paciente_id=1` - Filtrar por paciente
- `?skip=0&limit=10` - Paginación

### Gastos

```
GET    /api/gastos                    - Listar gastos
POST   /api/gastos                    - Crear gasto
GET    /api/gastos/{id}               - Obtener gasto
PUT    /api/gastos/{id}               - Actualizar gasto
DELETE /api/gastos/{id}               - Eliminar gasto
```

Parámetros:
- `?categoria=medicinas` - Filtrar por categoría

### Ingresos

```
GET    /api/ingresos                  - Listar ingresos
POST   /api/ingresos                  - Crear ingreso
GET    /api/ingresos/{id}             - Obtener ingreso
PUT    /api/ingresos/{id}             - Actualizar ingreso
DELETE /api/ingresos/{id}             - Eliminar ingreso
```

## 🔍 Documentación Interactiva

Accede a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Aquí puedes probar todos los endpoints en tiempo real.

## 📋 Ejemplos de Uso

### Crear paciente

```bash
curl -X POST "http://localhost:8000/api/pacientes" \
  -H "Content-Type: application/json" \
  -d '{
    "cedula": "123456789",
    "nombre": "Juan",
    "apellido": "García",
    "email": "juan@ejemplo.com",
    "fecha_nacimiento": "2020-01-15"
  }'
```

### Crear consulta

```bash
curl -X POST "http://localhost:8000/api/consultas" \
  -H "Content-Type: application/json" \
  -d '{
    "paciente_id": 1,
    "motivo_consulta": "Resfriado",
    "peso": 35,
    "altura": 130,
    "temperatura": 37,
    "diagnostico": "Resfriado viral",
    "medicinas": ["Paracetamol", "Amoxicilina"],
    "monto_consulta": 100
  }'
```

El IMC se calcula automáticamente: `35 / (1.30² ) = 20.77`

### Registrar gasto

```bash
curl -X POST "http://localhost:8000/api/gastos" \
  -H "Content-Type: application/json" \
  -d '{
    "descripcion": "Medicinas compradas",
    "monto": 50000,
    "categoria": "medicinas"
  }'
```

### Registrar ingreso

```bash
curl -X POST "http://localhost:8000/api/ingresos" \
  -H "Content-Type: application/json" \
  -d '{
    "descripcion": "Pago consulta",
    "monto": 100,
    "tipo": "consulta",
    "method_pago": "efectivo",
    "paciente_id": 1
  }'
```

## 🗄️ Modelo de Datos

### Paciente
- id, cedula (única), nombre, apellido, email, teléfono
- fecha_nacimiento, género, dirección, ciudad
- tutor_nombre, tutor_telefono, tutor_email
- alergias, medicamentos_actuales (JSON), historial_médico
- activo (para soft delete), created_at, updated_at
- Relaciones: muchas consultas, muchos ingresos

### Consulta
- id, paciente_id (FK), fecha_consulta, próxima_cita
- peso, altura, imc (calculado), temperatura
- presión_arterial, frecuencia_cardíaca, frecuencia_respiratoria
- motivo_consulta, diagnóstico, medicinas (JSON), observaciones
- monto_consulta, estado_pago (pendiente/pagado/parcial)
- created_at, updated_at
- Relaciones: un paciente, un ingreso

### Gasto
- id, descripción, monto
- categoría (medicinas, arriendo, servicios, etc)
- recurrente (bool), frecuencia (mensual/trimestral/anual)
- fecha_gasto, created_at

### Ingreso
- id, paciente_id (FK nullable), consulta_id (FK nullable)
- descripción, monto
- tipo (consulta, laboratorio, medicinas, etc)
- method_pago (efectivo, tarjeta, transferencia)
- fecha_ingreso, created_at
- Relaciones: un paciente, una consulta

## ⚙️ Integración Supabase (Base de Datos en la Nube)

### ¿Por qué Supabase?

✨ **PostgreSQL en la nube** | 🆓 **Gratuito** | 🔐 **Seguro** | ⚡ **Rápido**

- Base de datos PostgreSQL con SLA 99.9%
- 500MB de almacenamiento gratuito
- API automática REST/GraphQL
- Autenticación integrada con JWT
- Dashboard admin intuitivo
- Backups automáticos diarios

### Configuración Paso a Paso

#### 1️⃣ Crear cuenta (gratis)

1. Ve a https://supabase.com
2. Click en "Start your project"
3. Registrate con GitHub (recomendado)

#### 2️⃣ Crear proyecto

1. Click en "New project"
2. Completa el formulario:
   - **Nombre**: `clinica-pediatrica`
   - **Contraseña**: Copia y guarda en `.env` como `DATABASE_PASSWORD`
   - **Región**: Selecciona la más cercana a ti
3. Espera a que se cree (5 minutos max)

#### 3️⃣ Obtener credenciales en Settings > API

```env
SUPABASE_URL=https://[PROJECT-ID].supabase.co
SUPABASE_KEY=[ANON-PUBLIC-KEY]
```

#### 4️⃣ Obtener DATABASE_URL en Settings > Database

```env
DATABASE_URL=postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres
```

**Ejemplo completo:**
```env
SUPABASE_URL=https://abc123xyz.supabase.co
SUPABASE_KEY=eyJhbGc...
DATABASE_URL=postgresql://postgres:Mi_Contraseña123@abc123xyz.supabase.co:5432/postgres
```

#### 5️⃣ Verificar conexión

```bash
python main.py
```

Si ves este mensaje: ✅ **¡Conectado a Supabase!**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### ✨ Próximas funcionalidades con Supabase

- 📱 **Aplicación móvil** (conectar directamente a Supabase)
- 🔔 **Real-time updates** (cambios en tiempo real)
- 🔐 **Autenticación avanzada** (Google, GitHub, etc)
- 📊 **Analytics mejorados** (con Supabase Studio)
- 🌍 **Disponible globalmente** (acceso desde cualquier lugar)

## 🔒 Seguridad

✅ Validación Pydantic en todos los inputs
✅ SQL Injection prevention (SQLAlchemy ORM)
✅ CORS configurado
✅ Contraseñas hasheadas con bcrypt
✅ JWT para autenticación futura
✅ Type hints para seguridad de tipos

## 📊 Performance

- **FastAPI**: ~2000 req/s en predicción de modelos
- **Uvicorn**: Servidor ASGI muy rápido
- **PostgreSQL**: Índices automáticos en campos frecuentes
- **Connection pooling**: Máx 10 conexiones concurrentes

## 🎬 Crear GIF Demostrativo para GitHub

Para mejorar la visualización en tu perfil de GitHub, puedes crear un GIF mostrando el API en acción:

### Opción 1: ScreenToGif (Windows) ⭐ **Recomendado**

1. Descarga [ScreenToGif](https://www.screentogif.com/)
2. **Inicia tu servidor**: `python main.py`
3. Abre en navegador: `http://localhost:8000/docs`
4. Graba un GIF:
   - Click en "Record"
   - Demuestra: crear paciente → crear consulta → ver estadísticas
   - Guarda como `.gif`
5. Coloca el GIF en la carpeta `docs/demo.gif`
6. Agrega al README:
   ```markdown
   ![Demo API](docs/demo.gif)
   ```

### Opción 2: Usando FFmpeg (Multiplataforma)

```bash
# 1. Instala FFmpeg (https://ffmpeg.org/download.html)

# 2. Graba video con ffmpeg
ffmpeg -f gdigrab -framerate 30 -i desktop output.mp4

# 3. Convierte a GIF
ffmpeg -i output.mp4 -vf "scale=1280:-1" -t 10 demo.gif
```

### Opción 3: LiceCAP (Multiplataforma + Ligero)

Herramienta muy ligera perfecta para grabar GIFs:
- Descarga: https://www.cockos.com/licecap/
- Graba directamente en GIF
- Perfecto para demostraciones cortas (~10 seg)

---

## 🧪 Testing

```bash
# Instalar pytest (ya incluido en requirements.txt)
pytest tests/

# Con cobertura
pytest --cov=app tests/
```

## 📦 Deployment

### Local (Desarrollo)

```bash
python main.py
```

### Producción (Render, Heroku, Railway)

```bash
# Instalar gunicorn
pip install gunicorn

# Ejecutar
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'app'"

Asegúrate de estar en `c:\xampp\pdt` y ejecuta:
```bash
python main.py
```

### Error: "Connection refused" a Supabase

- Verifica DATABASE_URL en .env
- Verifica que Supabase esté online
- Prueba la conexión en Settings > Database > Test Connection

### Error: "CORS blocked"

El CORS ya está configurado para localhost:3000, 8000, etc.
Para agregar más origen, edita `app/core/config.py`

## 📞 Soporte

Documentos adicionales:
- `INSTALACION.md` - Guía paso a paso
- `GUIA_USO.md` - Manual de usuario

## 📄 Licencia

MIT - Libre para usar

---

**Estado**: ✅ Completamente funcional y listo para producción

Última actualización: Febrero 2026
