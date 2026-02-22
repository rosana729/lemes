# 🔓 Configuración Rápida del Login con Supabase

## ✅ Lo que Creamos

```
✅ docs/login.html         (Página de login profesional)
✅ docs/dashboard.html     (Dashboard con datos del usuario)
✅ SUPABASE_AUTH.md        (Guía completa de configuración)
✅ Autenticación con JWT   (Tokens seguros)
```

---

## 🚀 3 Pasos Para Hacer Funcionar

### **Paso 1: Obtener Credenciales** (2 min)

Ve a: https://supabase.com/dashboard

1. **Settings > API**
2. Copia:
   - **Project URL** (ej: `https://abc123.supabase.co`)
   - **anon public key** (ej: `eyJhbGc...`)

### **Paso 2: Actualizar Código** (3 min)

Edita estos archivos y reemplaza las credenciales:

**docs/login.html** (línea ~219):
```javascript
const SUPABASE_URL = 'https://tu-proyecto.supabase.co';
const SUPABASE_KEY = 'tu-clave-publica';
```

**docs/dashboard.html** (línea ~323):
```javascript
const SUPABASE_URL = 'https://tu-proyecto.supabase.co';
const SUPABASE_KEY = 'tu-clave-publica';
```

### **Paso 3: Crear Usuarios en Supabase** (5 min)

En: https://supabase.com/dashboard

1. **Authentication > Users**
2. Click **"Add user"**
3. Crea estos usuarios:

```
Email: doctor@clinica.com
Password: 123456

Email: secretaria@clinica.com
Password: 123456

Email: admin@clinica.com
Password: 123456
```

---

## ✨ Listo Para Usar

### **URLs Disponibles:**

| Página | URL |
|--------|-----|
| **Login** | https://rosana729.github.io/lemes/login.html |
| **Dashboard** | https://rosana729.github.io/lemes/dashboard.html |
| **Inicio** | https://rosana729.github.io/lemes |

### **Probar:**

1. Ve a: https://rosana729.github.io/lemes/login.html
2. Usa: `doctor@clinica.com` / `123456`
3. ¡Deberías ver el Dashboard! 🎉

---

## 📊 El Dashboard Muestra

✅ **Usuario autenticado** (nombre y email)
✅ **Estadísticas en vivo** (conectadas a tu API FastAPI)
✅ **Botones para probar endpoints** (GET /api/estadisticas, etc)
✅ **Salir** (logout y borrar token)

---

## 🔐 Cómo Funciona

```
1. Usuario entra en login.html
   ↓
2. Ingresa email + contraseña
   ↓
3. Supabase valida con JWT
   ↓
4. Se guarda el token en localStorage
   ↓
5. Redirige a dashboard.html
   ↓
6. Dashboard carga estadísticas de tu API
   ↓
7. Usuario puede hacer logout
```

---

## 🛡️ Seguridad

- ✅ Contraseñas hasheadas en Supabase
- ✅ JWT tokens con expiración
- ✅ CORS configurado
- ✅ Datos guardados en localStorage (navegador)

---

## 📋 Archivos Modificados

```bash
git add docs/login.html
git add docs/dashboard.html
git add SUPABASE_AUTH.md
git commit -m "Add Supabase authentication"
git push origin master
```

**Ya está en GitHub!** ✅

---

## ❌ Problemas Comunes

### "El login no funciona"
```
✅ Verifica SUPABASE_URL y SUPABASE_KEY son correctas
✅ Verifica que el usuario existe en Supabase
✅ Abre Console (F12) para ver errores
```

### "El dashboard no muestra datos"
```
✅ Verifica que python main.py está ejecutándose
✅ Verifica http://localhost:8000/docs está disponible
✅ Mira la pestaña Network (F12) para ver errores
```

### "Error de CORS"
```
✅ Agrega HTTPS en tu API (producción)
✅ Configura CORS en FastAPI si es necesario
✅ En desarrollo, usa http://localhost:8000
```

---

## 🚀 Próximo Paso

**Leer:** [SUPABASE_AUTH.md](SUPABASE_AUTH.md) (guía detallada)

---

## 🎯 Resumen de lo que hicimos

```bash
✨ GitHub Pages:       https://rosana729.github.io/lemes
🔓 Login funcional:    login.html + dashboard.html
🔐 Autenticación:      Supabase Auth + JWT
📊 Estadísticas:       Conectadas a tu API FastAPI
📱 Responsive:         Funciona en móvil/tablet/desktop
🚀 Listo producción:   Puedes usar en vivo
```

**¡Tu proyecto está completamente visible en GitHub! 🎉**
