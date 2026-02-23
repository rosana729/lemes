# 🏥 Clínica Pediátrica - Backend Symfony

Backend API para el sistema de gestión de clínica pediátrica construido con **Symfony 7** + **PostgreSQL (Supabase)**.

## ⚡ Setup Rápido

### 1. Instalar dependencias con Composer

```bash
cd backend
composer install
```

### 2. Configurar base de datos

El archivo `.env` ya tiene la conexión a Supabase. Solo verifica:

```bash
DATABASE_URL=postgresql://postgres:Sismas50mas@db.ikqwnmcowwakkxjwevbr.supabase.co:5432/postgres?serverVersion=15
```

### 3. Ejecutar migraciones (crear tablas)

```bash
php bin/console doctrine:migrations:migrate
```

O crear tablas manualmente en Supabase ejecutando `../schema_supabase.sql`

### 4. Iniciar servidor

```bash
# Opción A: Servidor Symfony
php bin/console server:run -vvv

# Opción B: PHP built-in server
php -S localhost:8000 -t public
```

Server corriendo en: **http://localhost:8000**

---

## 📡 Endpoints API

### Autenticación

```
POST /api/login
Content-Type: application/json

{
  "email": "doctor@clinica.com",
  "contraseña": "123456"
}

Respuesta:
{
  "success": true,
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "usuario": {
    "id": 1,
    "email": "doctor@clinica.com",
    "nombre": "Dr. Carlos García",
    "rol": "doctor"
  }
}
```

### Pacientes

```
GET  /api/pacientes      → Listar todos
POST /api/pacientes      → Crear nuevo
GET  /api/pacientes/{id} → Obtener uno
PUT  /api/pacientes/{id} → Actualizar
```

### Citas

```
GET  /api/citas          → Listar todas
POST /api/citas          → Crear nueva
GET  /api/citas/{id}     → Obtener una
PUT  /api/citas/{id}     → Actualizar
```

### Estadísticas (Dashboard)

```
GET /api/estadisticas    → Datos para el dashboard
```

### Health Check

```
GET /api/health          → Estado del servidor
```

---

## 🔐 Credenciales de prueba

```
doctor@clinica.com / 123456
secretaria@clinica.com / 123456
admin@clinica.com / 123456
```

---

## 📁 Estructura

```
backend/
├── src/
│   ├── Controller/       ← Endpoints API
│   ├── Entity/           ← Modelos (Usuario, Paciente, Cita)
│   ├── Service/          ← Lógica negocios
│   └── Kernel.php        ← Núcleo Symfony
├── config/
│   └── services.yaml     ← Configuración servicios
├── public/
│   └── index.php         ← Punto entrada
├── .env                  ← Variables entorno
└── composer.json         ← Dependencias
```

---

## 🚀 Desplegar en Railway

1. Sube el `backend/` a GitHub
2. Conecta repo en [Railway](https://railway.app)
3. Configura variable  `DATABASE_URL` en Railway
4. Deploy automático ✅

---

## 🔗 Conectar con Frontend

En `docs/config.js` del frontend:

```javascript
const API_URL = 'http://localhost:8000';  // desarrollo
// const API_URL = 'https://api.lemes.railway.app'; // producción
```

---

## 📧 Soporte

¿Preguntas? Revisa los comentarios en el código 👍
