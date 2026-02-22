# 🚀 GUÍA COMPLETA: De Cero a Producción

Tu proyecto **Clínica Pediátrica** está listo. Aquí está TODO lo que necesitas hacer:

---

## 📋 RESUMEN DE ARCHIVOS

```
✅ schema_supabase.sql        → Script SQL (6 tablas + datos)
✅ SETUP_DATABASE.md          → Cómo ejecutar en Supabase
✅ SUPABASE_AUTH.md           → Autenticación con JWT
✅ QUICK_SETUP_SUPABASE.md    → Setup rápido (3 pasos)
✅ docs/login.html            → Login funcional
✅ docs/dashboard.html        → Dashboard de usuario
✅ docs/index.html            → Página principal
✅ main.py                    → API FastAPI
```

---

## 🎯 PASO 1: CREAR BASE DE DATOS EN SUPABASE (10 min)

### 1️⃣ Ir a Supabase SQL Editor

```
https://supabase.com/dashboard → Lemes → SQL Editor → New Query
```

### 2️⃣ Copiar Script SQL

Abre: [schema_supabase.sql](schema_supabase.sql)

```
- Selecciona TODO (Ctrl+A)
- Copia (Ctrl+C)
- En Supabase SQL Editor, pega (Ctrl+V)
- Click en "▶ Run"
```

### 3️⃣ Verificar Tablas

En Supabase > Table Editor, vas a ver:

```
usuarios     ─ 5 filas
sesiones     ─ 3 filas
pacientes    ─ 5 filas
citas        ─ 5 filas
historias_clinicas ─ 3 filas
documentos   ─ 5 filas
```

**Credenciales de Prueba:**

```
doctor@clinica.com / 123456 (doctor)
secretaria@clinica.com / 123456 (secretaria)
admin@clinica.com / 123456 (admin)
```

---

## 🔐 PASO 2: CONFIGURAR AUTENTICACIÓN (5 min)

### 1️⃣ Obtener Credenciales Supabase

En: **Settings > API**

```
SUPABASE_URL = https://...supabase.co
SUPABASE_KEY = eyJhbGc...
```

### 2️⃣ Actualizar Código

**docs/login.html** (línea ~219):

```javascript
const SUPABASE_URL = 'https://abc123.supabase.co';
const SUPABASE_KEY = 'tu-clave-publica';
```

**docs/dashboard.html** (línea ~323):

```javascript
const SUPABASE_URL = 'https://abc123.supabase.co';
const SUPABASE_KEY = 'tu-clave-publica';
```

### 3️⃣ Hacer Push

```bash
git add docs/
git commit -m "Update Supabase credentials"
git push origin master
```

---

## 🌐 PASO 3: HABILITAR GITHUB PAGES (2 min)

### 1️⃣ Ir a Settings

```
https://github.com/rosana729/lemes/settings/pages
```

### 2️⃣ Configurar Build

```
Source:     Deploy from a branch
Branch:     master
Folder:     /docs
```

### 3️⃣ Guardar

Click **Save** → Espera 1-2 minutos

**Tu sitio estará en:**
```
https://rosana729.github.io/lemes
```

---

## 🧪 PASO 4: PROBAR APP (5 min)

### 1️⃣ Ejecutar API Localmente

```bash
cd c:\xampp\htdocs\Lemes
python main.py
```

Debe mostrar:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 2️⃣ Probar Login Online

```
https://rosana729.github.io/lemes/login.html

Email: doctor@clinica.com
Contraseña: 123456
```

Deberías ver:
```
✅ Login exitoso. Redirigiendo...
→ Dashboard
```

### 3️⃣ Ver Dashboard

```
https://rosana729.github.io/lemes/dashboard.html

Verás:
- Tu nombre y email
- Estadísticas
- Botones para probar API
```

---

## 📊 PASO 5: CONECTAR API (10 min)

### 1️⃣ Actualizar DATABASE_URL en main.py

En: `app/core/config.py`

```python
DATABASE_URL = "postgresql://[user]:[password]@[host]/[database]"
```

Obtenerlo en **Supabase > Settings > Database > Connection Info**

### 2️⃣ Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 3️⃣ Probar API

```bash
python main.py
```

Luego abre:
```
http://localhost:8000/docs
```

Deberías ver el Swagger UI con todos los endpoints.

---

## 🎬 PASO 6: CREAR GIF (OPCIONAL - 15 min)

Para que tu proyecto sea más atractivo en GitHub:

### 1️⃣ Descargar ScreenToGif

```
https://www.screentogif.com/
```

### 2️⃣ Grabar API en Acción

```
1. Ejecuta: python main.py
2. Abre: http://localhost:8000/docs
3. Graba 15 segundos demostrando endpoints
4. Guarda como: docs/demo.gif
```

### 3️⃣ Agregar al README

En README.md:

```markdown
![Demo API](docs/demo.gif)
```

Hacer push:

```bash
git add docs/demo.gif README.md
git commit -m "Add demo GIF"
git push origin master
```

---

## 📝 PASO 7: DOCUMENTACIÓN (10 min)

Leer en este orden:

1. **[QUICK_SETUP_SUPABASE.md](QUICK_SETUP_SUPABASE.md)** ⭐ (Empieza aquí)
2. **[SETUP_DATABASE.md](SETUP_DATABASE.md)** (Base de datos)
3. **[SUPABASE_AUTH.md](SUPABASE_AUTH.md)** (Autenticación)
4. **[GIF_DEMO.md](GIF_DEMO.md)** (GIF demostrativo)

---

## ✅ CHECKLIST FINAL

### Base de Datos
- [ ] Script SQL ejecutado en Supabase
- [ ] 6 tablas creadas
- [ ] Datos de prueba insertados
- [ ] Usuarios de prueba listos

### Autenticación
- [ ] SUPABASE_URL actualizada
- [ ] SUPABASE_KEY actualizada
- [ ] docs/login.html modificado
- [ ] docs/dashboard.html modificado

### GitHub Pages
- [ ] Settings > Pages configurado
- [ ] Branch: master
- [ ] Folder: /docs
- [ ] Sitio online

### Testing
- [ ] API ejecutándose en localhost:8000
- [ ] Login funciona
- [ ] Dashboard muestra datos
- [ ] Endpoints responden en Swagger

### Producción
- [ ] DATABASE_URL en main.py
- [ ] Dependencias instaladas
- [ ] API conectada a Supabase
- [ ] Cambiar contraseñas reales

---

## 🔗 URLS IMPORTANTES

| Sección | URL |
|---------|-----|
| **Sitio Web** | https://rosana729.github.io/lemes |
| **Login** | https://rosana729.github.io/lemes/login.html |
| **Dashboard** | https://rosana729.github.io/lemes/dashboard.html |
| **GitHub Repo** | https://github.com/rosana729/lemes |
| **Supabase** | https://supabase.com/dashboard |
| **API Local** | http://localhost:8000 |
| **API Docs** | http://localhost:8000/docs |

---

## 📊 ESTRUCTURA FINAL

```
FRONTEND (GitHub Pages)
├── index.html          (Página inicio)
├── login.html          (Login Supabase)
├── dashboard.html      (Dashboard usuario)
└── demo.gif            (GIF opcional)

BACKEND (LocalHost)
├── main.py             (API FastAPI)
├── app/models/         (SQLAlchemy models)
├── app/routes/         (Endpoints)
└── app/schemas/        (Validación Pydantic)

DATABASE (Supabase Cloud)
├── usuarios            (5 registros)
├── sesiones            (3 registros)
├── pacientes           (5 registros)
├── citas               (5 registros)
├── historias_clinicas  (3 registros)
└── documentos          (5 registros)
```

---

## ⏱️ TIEMPO TOTAL

```
Paso 1 (BD):           10 min
Paso 2 (Auth):         5 min
Paso 3 (Pages):        2 min
Paso 4 (Testing):      5 min
Paso 5 (API):          10 min
Paso 6 (GIF):          15 min (OPCIONAL)
Paso 7 (Docs):         10 min

TOTAL:                 57 min (o 42 min sin GIF)
```

---

## 🎯 OBJETIVO FINAL

Al terminar tendrás:

✨ **Sitio Web** - Visible en GitHub Pages
✨ **Login Funcional** - Con autenticación Supabase
✨ **Database Modern** - PostgreSQL en Supabase
✨ **API REST** - FastAPI con 12+ endpoints
✨ **Dashboard** - Con datos en tiempo real
✨ **Documentación** - Completa y clara
✨ **Listo Producción** - Para usar en vivo

---

## 📞 CONTACTO & SOPORTE

Si tienes problemas:

1. Abre [SETUP_DATABASE.md](SETUP_DATABASE.md) - Problemas comunes
2. Abre [SUPABASE_AUTH.md](SUPABASE_AUTH.md) - Autenticación
3. Revisar archivo `.env`
4. Avisar en GitHub Issues

---

## 🚀 ¡A EMPEZAR!

### Ahora mismo (5 min):

```bash
# 1. Copiar schema_supabase.sql
# 2. Ir a Supabase SQL Editor
# 3. Pegar y ejecutar
# 4. ¡Listo!
```

**Próximo paso:** [SETUP_DATABASE.md](SETUP_DATABASE.md)

---

**¡Tu proyecto está listo para conquista el mundo! 🌍**

Última actualización: Febrero 2026
