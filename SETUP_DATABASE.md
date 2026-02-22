# 📊 Cómo Crear la Base de Datos en Supabase

Tu proyecto tiene un **script SQL completo** listo para Supabase. Sigue estos pasos:

---

## ⚡ Paso 1: Ir a Supabase SQL Editor

1. Ve a: https://supabase.com/dashboard
2. Selecciona tu proyecto **"Lemes"**
3. En el menú lateral, busca **"SQL Editor"** (o ve directamente)

---

## ⚡ Paso 2: Crear Nueva Query

1. Click en **"New query"** o **"+"**
2. Se abrirá un editor SQL en blanco

---

## ⚡ Paso 3: Copiar el Script

El archivo `schema_supabase.sql` contiene **TODO**:

✅ 6 tablas
✅ Índices optimizados
✅ Datos de prueba
✅ Credenciales de ejemplo

---

## ⚡ Paso 4: Ejecutar el Script

### Opción A: Copiar Todo de una Vez (Recomendado)

1. Abre: [schema_supabase.sql](schema_supabase.sql)
2. Selecciona todo (Ctrl+A)
3. Copia (Ctrl+C)
4. En Supabase SQL Editor, pega (Ctrl+V)
5. Click en **"▶ Run"** (botón verde)

### Opción B: Ejecutar Sección por Sección

Si hay problemas, ejecuta cada sección por separado:

```sql
-- Sección 1: Crear tabla USUARIOS
CREATE TABLE IF NOT EXISTS usuarios (...)

-- Sección 2: Crear tabla SESIONES
CREATE TABLE IF NOT EXISTS sesiones (...)

-- Y así sucesivamente...
```

---

## ✅ Verificar que Funcionó

Después de ejecutar, deberías ver:

```
✓ Created table usuarios
✓ Created index idx_usuarios_email
✓ Inserted 5 rows into usuarios
✓ Created table sesiones
✓ Inserted 3 rows into sesiones
✓ Created table pacientes
✓ Inserted 5 rows into pacientes
✓ Created table citas
✓ Inserted 5 rows into citas
✓ Created table historias_clinicas
✓ Inserted 3 rows into historias_clinicas
✓ Created table documentos
✓ Inserted 5 rows into documentos
```

---

## 🔍 Ver las Tablas Creadas

En Supabase > "Table Editor", vas a ver:

```
📊 Database → public →
├── usuarios (5 filas)
├── sesiones (3 filas)
├── pacientes (5 filas)
├── citas (5 filas)
├── historias_clinicas (3 filas)
└── documentos (5 filas)
```

---

## 🧪 Probar con Datos de Prueba

### Usr 1: Doctor Pediatra

```
Email: doctor@clinica.com
Contraseña: 123456
Rol: doctor
```

### Usr 2: Secretaria

```
Email: secretaria@clinica.com
Contraseña: 123456
Rol: secretaria
```

### Usr 3: Admin

```
Email: admin@clinica.com
Contraseña: 123456
Rol: admin
```

---

## 📊 Estructura de Datos

```
USUARIOS (5)
├── Id 1: Dr. Carlos García López (doctor)
├── Id 2: Dra. María González (doctor)
├── Id 3: Ana Martínez (secretaria)
├── Id 4: Admin Clínica (admin)
└── Id 5: Dr. Pedro Ramírez (doctor)

SESIONES (3)
├── Sesión Doctor 1
├── Sesión Doctor 2
└── Sesión Secretaria

PACIENTES (5)
├── Juan Pérez García (4 años)
├── María López Rodríguez (5 años)
├── Carlos Martínez Silva (3 años)
├── Sofía González Fernández (6 años)
└── Diego Ramírez Castro (2 años)

CITAS (5)
├── Cita para Juan - 2026-02-25 10:30
├── Cita para María - 2026-02-25 11:00
├── Cita para Carlos - 2026-02-26 09:00
├── Cita para Sofía - 2026-02-26 14:30
└── Cita anterior para Juan - 2026-02-20 (realizada)

HISTORIAS CLÍNICAS (3)
├── Historia de Juan (revisión anual)
├── Historia de María (tos persistente)
└── Historia de Carlos (evaluación crecimiento)

DOCUMENTOS (5)
├── Carné de vacunación de Juan
├── Análisis de sangre de Juan
├── Radiografía de tórax de María
├── Tabla de crecimiento de Carlos
└── Reporte de alergia de Sofía
```

---

## ⚠️ Problemas Comunes

### "Error: relation already exists"

**Solución:** Las tablas ya existen. Hay dos opciones:

```sql
-- Opción 1: Usar IF NOT EXISTS (ya está en el script)
-- Solo omitirá las tablas que ya existen

-- Opción 2: Eliminar todo primero
DROP TABLE IF EXISTS documentos CASCADE;
DROP TABLE IF EXISTS historias_clinicas CASCADE;
DROP TABLE IF EXISTS citas CASCADE;
DROP TABLE IF EXISTS pacientes CASCADE;
DROP TABLE IF EXISTS sesiones CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;

-- Luego ejecutar el script completo
```

### "Error: Unique constraint violation"

**Solución:** Ya hay datos. Ejecuta esto primero:

```sql
DELETE FROM documentos;
DELETE FROM historias_clinicas;
DELETE FROM citas;
DELETE FROM sesiones;
DELETE FROM pacientes;
DELETE FROM usuarios;

-- Luego los INSERT
```

### "Error: Foreign key constraint failed"

**Solución:** Los datos se insertaron en orden incorrecto. Ejecuta el script completo en orden.

---

## 🔒 Seguridad (IMPORTANTE)

### Cambiar Contraseñas en Producción

Las contraseñas actuales están hasheadas, pero en PRODUCCIÓN usa:

```sql
-- Generar hash bcrypt de contraseña real
-- Reemplaza los hashes por los reales
UPDATE usuarios SET contraseña = 'hash_bcrypt_real'
WHERE email = 'doctor@clinica.com';
```

### Cambiar Tokens de Sesión

Los tokens son ejemplos. El servidor debe generar tokens JWT reales:

```python
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "tu-clave-super-secreta"

token = jwt.encode(
    {
        "user_id": 1,
        "email": "doctor@clinica.com",
        "exp": datetime.utcnow() + timedelta(days=7)
    },
    SECRET_KEY,
    algorithm="HS256"
)
```

---

## 🚀 Conectar desde tu API

Una vez creadas las tablas en Supabase, actualiza tu código Python:

**main.py:**
```python
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://[user]:[password]@[host]:[port]/[database]"

engine = create_engine(DATABASE_URL)
```

**Obtener DATABASE_URL en Supabase:**

1. Ve a: Settings > Database > Connection Info
2. Format: Database URL
3. Copia y pega en tu `.env`

---

## ✅ Checklist Final

- [ ] Proyecto creado en Supabase
- [ ] SQL editor abierto
- [ ] Script copiado
- [ ] Script ejecutado
- [ ] 6 tablas creadas
- [ ] Datos de prueba insertados
- [ ] Credenciales actualizadas
- [ ] DATABASE_URL en `.env`
- [ ] API conectada

---

## 📞 Archivos Relacionados

| Archivo | Propósito |
|---------|-----------|
| [schema_supabase.sql](schema_supabase.sql) | Script SQL completo |
| [SUPABASE_AUTH.md](SUPABASE_AUTH.md) | Autenticación JWT |
| [QUICK_SETUP_SUPABASE.md](QUICK_SETUP_SUPABASE.md) | Setup rápido |

---

## 🎯 Próximo Paso

Una vez las tablas estén en Supabase:

1. **Actualiza credenciales** en `docs/login.html` y `docs/dashboard.html`
2. **Prueba el login** en https://rosana729.github.io/lemes/login.html
3. **Conecta tu API** con DATABASE_URL

¡Listo para producción! 🚀
