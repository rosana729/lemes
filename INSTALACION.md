# 🚀 INSTALACIÓN - Clínica Pediátrica FastAPI

## 📋 Requisitos Previos

- ✅ Python 3.9 o superior instalado
- ✅ Conexión a internet
- ✅ Cuenta Supabase (gratuita)
- ✅ Editor de código (VS Code, PyCharm, etc)

## ⏱️ Tiempo estimado: 15 minutos

---

## PASO 1: Descargar Python (si no lo tienes)

### Windows

1. Ve a https://www.python.org/downloads/
2. Descarga "Python 3.11.x" (última versión)
3. Ejecuta el instalador
4. **IMPORTANTE**: Marca "Add Python to PATH"
5. Haz clic en "Install Now"

Verifica:
```powershell
python --version
pip --version
```

---

## PASO 2: Crear ambiente virtual

En PowerShell (como administrador):

```powershell
cd c:\xampp\pdt

# Crear ambiente
python -m venv venv

# Activar
.\venv\Scripts\Activate.ps1
```

Verás algo como: `(venv) PS C:\xampp\pdt>`

Si da error de permisos:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## PASO 3: Instalar dependencias

```powershell
pip install -r requirements.txt
```

Esperado: "Successfully installed 15 packages" (puede tardar 2-3 minutos)

---

## PASO 4: Crear cuenta Supabase

1. Abre https://supabase.com
2. Haz clic en "Sign Up"
3. Regístrate con GitHub o email
4. Crea un nuevo proyecto:
   - Nombre: `clinica-pediatrica`
   - Región: La más cercana a ti
   - Contraseña: Copia esto 👇

---

## PASO 5: Obtener credenciales Supabase

En el panel de Supabase:

1. **Settings > API**
   - Copia `Project URL` → SUPABASE_URL
   - Copia `anon public` key → SUPABASE_KEY

2. **Settings > Database**
   - Usuario: `postgres` (por defecto)
   - Contraseña: La que ingresaste
   - Port: `5432`

---

## PASO 6: Editar archivo .env

Abre `c:\xampp\pdt\.env` y configura:

```env
# Supabase
SUPABASE_URL=https://abc123xyz.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIs...
DATABASE_URL=postgresql://postgres:TuContraseña@abc123xyz.supabase.co:5432/postgres

# Seguridad (cambiar en producción)
SECRET_KEY=mi-clave-super-secreta-cambiar-luego
DEBUG=True
```

**Ejemplo completo:**

```env
SUPABASE_URL=https://bwxyzabc.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
DATABASE_URL=postgresql://postgres:MyPassword123@bwxyzabc.supabase.co:5432/postgres

API_TITLE=Clínica Pediátrica API
API_VERSION=1.0.0
DEBUG=True

SECRET_KEY=clinica-pediatrica-secreta-2024
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000", "http://127.0.0.1:3000"]
LOG_LEVEL=INFO
```

---

## PASO 7: Probar conexión a BD

```powershell
# Asegúrate de estar en c:\xampp\pdt con venv activado

python -c "from app.core.database import engine; print('✓ Conexión OK' if engine else '✗ Error')"
```

Esperado: `✓ Conexión OK`

Si falla, verifica:
- DATABASE_URL es correcto
- Supabase está online
- Contraseña tiene caracteres especiales (usa comillas)

---

## PASO 8: Iniciar servidor

```powershell
python main.py
```

Esperado:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

---

## PASO 9: Verificar que funciona

### Opción A: Browser

Abre en navegador: **http://localhost:8000**

Verás:
```json
{
  "status": "healthy",
  "service": "Clínica Pediátrica API",
  "version": "1.0.0"
}
```

### Opción B: Documentación Swagger

Abre: **http://localhost:8000/docs**

- Ves todos los endpoints
- Puedes probarlos directamente
- Auto-documentado ✨

### Opción C: Usando curl

```powershell
# En otra terminal PowerShell
curl http://localhost:8000/health

# Resultado
{"status":"ok"}
```

---

## PASO 10: Crear primer paciente

### Opción A: Swagger UI (recomendado)

1. Abre http://localhost:8000/docs
2. Expande "POST /api/pacientes"
3. Haz clic en "Try it out"
4. Completa:

```json
{
  "cedula": "123456789",
  "nombre": "Juan",
  "apellido": "García",
  "email": "juan@example.com",
  "fecha_nacimiento": "2020-01-15",
  "genero": "M",
  "telefono": "1234567890"
}
```

5. Haz clic en "Execute"

Resultado:
```json
{
  "id": 1,
  "cedula": "123456789",
  "nombre": "Juan",
  "apellido": "García",
  "nombre_completo": "Juan García",
  "edad": 6,
  ...
}
```

### Opción B: PowerShell

```powershell
$headers = @{"Content-Type" = "application/json"}

$body = @{
    cedula = "123456789"
    nombre = "Juan"
    apellido = "García"
    email = "juan@example.com"
    fecha_nacimiento = "2020-01-15"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/api/pacientes" `
    -Method POST `
    -Headers $headers `
    -Body $body
```

---

## ✅ Checklist de Instalación

- [ ] Python 3.9+ instalado
- [ ] Ambiente virtual activado (venv)
- [ ] Dependencias instaladas (pip install -r requirements.txt)
- [ ] Cuenta Supabase creada
- [ ] .env configurado con credenciales
- [ ] Servidor iniciado (python main.py)
- [ ] http://localhost:8000/health responde
- [ ] http://localhost:8000/docs abre Swagger
- [ ] Puedo crear un paciente

## 🎯 Próximos Pasos

1. ✅ Crear varios pacientes
2. ✅ Crear consultas médicas
3. ✅ Registrar gastos
4. ✅ Registrar ingresos
5. ✅ Ver estadísticas: GET /api/estadisticas

## 🔧 Comandos Útiles

```powershell
# Activar ambiente
.\venv\Scripts\Activate.ps1

# Desactivar ambiente
deactivate

# Instalar nuevo paquete
pip install nombre-paquete

# Listar paquetes instalados
pip list

# Ejecutar servidor
python main.py

# Ejecutar tests
pytest tests/

# Detener servidor
Ctrl + C
```

## 🐛 Problemas Comunes

### Error: "ModuleNotFoundError: No module named 'fastapi'"

**Solución:**
```powershell
pip install -r requirements.txt
```

### Error: "Connection refused" (Supabase)

**Solución:**
- Verifica DATABASE_URL en .env
- Verifica que Supabase está online (dashboard)
- Prueba credenciales manualmente

### Error: "Uvicorn not found"

**Solución:**
```powershell
pip install uvicorn
python main.py
```

### Error: "Port 8000 already in use"

**Solución:**
```powershell
# Cambiar puerto en main.py
# Línea final: port=8001 (o cualquier otro)
```

### El ambiente virtual no activa

**Solución:**
```powershell
# Permitir scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Luego activar
.\venv\Scripts\Activate.ps1
```

---

## 📞 Soporte

Si hay problema:

1. Revisa "Problemas Comunes" arriba
2. Lee README.md
3. Verifica .env está bien configurado
4. Prueba: `python main.py` en `c:\xampp\pdt`

---

## 🎉 ¡Felicidades!

Tu API está lista para usar. Ahora puedes:

- Crear un frontend (Vue.js, React, etc)
- Desplegar a producción
- Agregar más funcionalidades
- Integrar con otros servicios

---

**Tiempo total estimado: 15 minutos**

Última actualización: Febrero 2026
