# 🔐 Configurar Login con Supabase

Tu sitio web en GitHub Pages ahora tiene un **login funcional** conectado a Supabase. Aquí está cómo configurarlo.

---

## ⚡ Paso 1: Obtener Credenciales de Supabase

### En Supabase Dashboard:

1. Ve a: https://supabase.com/dashboard
2. Selecciona tu proyecto "clinica-pediatrica"
3. Ve a **Settings > API**
4. Copia:
   - **Project URL** → `SUPABASE_URL`
   - **anon public** → `SUPABASE_KEY`

### Formato:
```
SUPABASE_URL=https://abc123xyz.supabase.co
SUPABASE_KEY=eyJhbGc...tu-clave-publica...
```

---

## ⚡ Paso 2: Agregar las Credenciales al Código

Edit `docs/login.html` (línea 219):

```javascript
// ANTES:
const SUPABASE_URL = 'https://your-project.supabase.co';
const SUPABASE_KEY = 'your-anon-key';

// DESPUÉS:
const SUPABASE_URL = 'https://abc123xyz.supabase.co';
const SUPABASE_KEY = 'eyJhbGc...tu-clave...';
```

También en `docs/dashboard.html` (línea 323):

```javascript
// ANTES:
const SUPABASE_URL = 'https://your-project.supabase.co';
const SUPABASE_KEY = 'your-anon-key';

// DESPUÉS:
const SUPABASE_URL = 'https://abc123xyz.supabase.co';
const SUPABASE_KEY = 'eyJhbGc...tu-clave...';
```

---

## ⚡ Paso 3: Crear Usuarios en Supabase

### Opción A: En Supabase Dashboard (Fácil)

1. Ve a **Authentication > Users**
2. Click en **"Add user"**
3. Completa:
   ```
   Email: doctor@clinica.com
   Password: 123456
   ```
4. Repite para:
   - secretaria@clinica.com / 123456
   - admin@clinica.com / 123456

### Opción B: Programáticamente (Avanzado)

```python
# En main.py o un script Python
import requests

SUPABASE_URL = "https://tu-proyecto.supabase.co"
SUPABASE_KEY = "tu-service-key"  # Service key, NO anon key

# Crear usuario
response = requests.post(
    f"{SUPABASE_URL}/auth/v1/admin/users",
    headers={
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "email": "doctor@clinica.com",
        "password": "123456",
        "email_confirm": True
    }
)

print(response.json())
```

---

## ✅ Paso 4: Probar el Login

1. Ve a: `https://rosana729.github.io/lemes/login.html`
2. Usa credenciales:
   - Email: `doctor@clinica.com`
   - Contraseña: `123456`
3. Deberías ver el **Dashboard** ✅

---

## 📋 Configuración de Supabase Auth

### RLS (Row Level Security)

Por seguridad, habilita RLS en Supabase:

1. Ve a **Database > Policies**
2. Para la tabla `usuarios`, crea política:

```sql
-- Que cada usuario solo vea sus propios datos
CREATE POLICY "Users can view own data"
  ON usuarios FOR SELECT
  USING (auth.uid() = id);
```

### CORS para GitHub Pages

En Supabase, permite CORS:

1. Ve a **Settings > API > CORS**
2. Agrega:
   ```
   https://rosana729.github.io
   ```

---

## 🔄 Flow de Autenticación

```
1. Usuario va a login.html
   ↓
2. Ingresa email + contraseña
   ↓
3. Supabase valida credenciales
   ↓
4. Recibe JWT token
   ↓
5. Guarda en localStorage
   ↓
6. Redirige a dashboard.html
   ↓
7. Dashboard muestra datos personalizados
```

---

## 🛡️ Seguridad

### Tokens JWT están guardados en localStorage:
```javascript
// Automático en login.html
localStorage.setItem('token', data.session.access_token);
```

### Para enviar a la API:
```javascript
const token = localStorage.getItem('token');

fetch('http://localhost:8000/api/pacientes', {
    headers: {
        'Authorization': `Bearer ${token}`
    }
})
```

### En FastAPI (main.py):
```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthCredentials

security = HTTPBearer()

@app.get("/api/pacientes")
def get_pacientes(credentials: HTTPAuthCredentials = Depends(security)):
    token = credentials.credentials
    # Validar token con Supabase
    # ...
```

---

## 🔗 URLs Importantes

| Página | URL |
|--------|-----|
| **Login** | https://rosana729.github.io/lemes/login.html |
| **Dashboard** | https://rosana729.github.io/lemes/dashboard.html |
| **Inicio** | https://rosana729.github.io/lemes |
| **Supabase Dashboard** | https://supabase.com/dashboard |
| **Supabase Auth Docs** | https://supabase.com/docs/guides/auth |

---

## ❌ Solución de Problemas

### "Login fallido"
- ✅ Verifica que las credenciales sean correctas
- ✅ Verifica que el usuario exista en Supabase
- ✅ Verifica que SUPABASE_URL y SUPABASE_KEY son correctas

### "Conexión rechazada a API"
- ✅ El servidor FastAPI debe estar ejecutándose: `python main.py`
- ✅ Debe estar en http://localhost:8000
- ✅ Agrega CORS en FastAPI si es necesario

### "El dashboard no muestra datos"
- ✅ Verifica que el servidor está ejecutándose
- ✅ Verifica que hay datos en la base de datos
- ✅ Abre Console (F12) para ver errores

---

## 📱 Próximas Mejoras

Con Supabase autentica, puedes agregar:

- 🔔 **Real-time Notifications** (cambios en tiempo real)
- 🎯 **Role-based Access** (roles: doctor, secretaria, admin)
- 📱 **Aplicación Móvil** (Supabase + React Native)
- 📊 **Reportes** (datos personalizados por usuario)
- 🔐 **OAuth** (login con Google, GitHub, etc)

---

## 🚀 Resumen Rápido

```bash
# 1. Obtener credenciales de Supabase
# Settings > API

# 2. Actualizar docs/login.html y docs/dashboard.html
# Línea ~220: SUPABASE_URL y SUPABASE_KEY

# 3. Crear usuarios en Supabase
# Authentication > Users > Add user

# 4. Hacer push
git add docs/
git commit -m "Add Supabase authentication to login pages"
git push origin master

# 5. Probar en https://rosana729.github.io/lemes/login.html
```

---

¿Necesitas ayuda con algún paso? 💬
