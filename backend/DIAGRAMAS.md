# 🎨 Diagramas Visuales de la Arquitectura

## 1️⃣ Vista General: Capas

```
╔════════════════════════════════════════════════════════════════╗
║                    NAVEGADOR (Frontend)                        ║
║                   docs/login.html                              ║
║              fetch() → JSON response                            ║
╚════════════════════════════════════════════════════════════════╝
                           ↓ HTTP
                           ↓ JSON
╔════════════════════════════════════════════════════════════════╗
║                  SERVIDOR (Symfony PHP)                        ║
║                                                                ║
║  ┌─────────────────────────────────────────────────────────┐  ║
║  │ 1. Controller Layer                                     │  ║
║  │    AuthController.php                                   │  ║
║  │    PacienteController.php                               │  ║
║  │    CitaController.php                                   │  ║
║  └─────────────────────────────────────────────────────────┘  ║
║                           ↓                                     ║
║  ┌─────────────────────────────────────────────────────────┐  ║
║  │ 2. Service Layer                                        │  ║
║  │    AuthService.php                                      │  ║
║  │    PacienteService.php                                  │  ║
║  │    CitaService.php                                      │  ║
║  └─────────────────────────────────────────────────────────┘  ║
║                           ↓                                     ║
║  ┌─────────────────────────────────────────────────────────┐  ║
║  │ 3. Data Access Layer (Doctrine)                         │  ║
║  │    EntityManager                                        │  ║
║  │    Repositories                                         │  ║
║  └─────────────────────────────────────────────────────────┘  ║
║                           ↓                                     ║
║  ┌─────────────────────────────────────────────────────────┐  ║
║  │ 4. Utility Layer                                        │  ║
║  │    JwtUtil.php                                          │  ║
║  │    ResponseUtil.php                                     │  ║
║  └─────────────────────────────────────────────────────────┘  ║
║                           ↓                                     ║
╚════════════════════════════════════════════════════════════════╝
                           ↑ JSON
                           ↑ Status Code
╔════════════════════════════════════════════════════════════════╗
║              BASE DE DATOS (Supabase PostgreSQL)               ║
║         ikqwnmcowwakkxjwevbr.supabase.co                       ║
║                                                                ║
║  ┌─────────┐ ┌──────────┐ ┌──────────┐ ┌─────────────────┐   ║
║  │ usuarios│ │pacientes │ │  citas   │ │historias_clinic│   ║
║  └─────────┘ └──────────┘ └──────────┘ └─────────────────┘   ║
╚════════════════════════════════════════════════════════════════╝
```

---

## 2️⃣ Flujo: Login

```
┌─────────────────────────────┐
│ Usuario ingresa credenciales│
│ email: doctor@clinica.com   │
│ contraseña: 123456          │
└──────────────┬──────────────┘
               │
               ↓ fetch() POST
┌─────────────────────────────┐
│ Client: POST /api/auth/login│
│ Content-Type: application/json
└──────────────┬──────────────┘
               │
               ↓ HTTP Request
╔═════════════════════════════════════════════════════╗
║ 1. AUTHCONTROLLER::LOGIN()                          ║
║    Recibe: Request {email, contraseña}              ║
║    ├─ json_decode()                                 ║
║    ├─ $this->authService->login($email, $password) ║
║    └─> Retorna: $usuario (array)                   ║
╠═════════════════════════════════════════════════════╣
║ 2. AUTHSERVICE::LOGIN()                             ║
║    ├─ findOneBy(['email' => $email])  → BD          ║
║    ├─ $usuario->isActivo()                          ║
║    ├─ verificarContraseña($pass)                    ║
║    ├─ JwtUtil::encode({id, email})                  ║
║    └─> Retorna: {access_token, usuario}            ║
╠═════════════════════════════════════════════════════╣
║ 3. JWTUTIL::ENCODE()                                ║
║    ├─ JWT::encode(payload, secret, HS256)          ║
║    └─> Retorna: token (string)                      ║
╠═════════════════════════════════════════════════════╣
║ 4. RESPONSEUTIL::SUCCESS()                          ║
║    ├─ Crear JSON con status: 200                    ║
║    ├─ Agregar CORS headers                          ║
║    └─> Retorna: JsonResponse                        ║
╚═════════════════════════════════════════════════════╝
               ↑ JSON Response
               │
┌──────────────┴──────────────┐
│ 200 OK                       │
│ {                            │
│   status: 200,               │
│   data: {                    │
│     access_token: "eyJ...",  │
│     usuario: {...}           │
│   }                          │
│ }                            │
└──────────────┬──────────────┘
               │
               ↓ localStorage.setItem()
┌──────────────┴──────────────┐
│ Cliente almacena:            │
│ - token en localStorage      │
│ - usuario en localStorage    │
│ - Redirigir a /dashboard.html
└──────────────────────────────┘
```

---

## 3️⃣ Estructura: Directorios

```
backend/
│
├── src/
│   ├── Controller/               ← Endpoints HTTP
│   │   ├── AuthController.php        (POST /api/auth/login)
│   │   ├── PacienteController.php    (CRUD /api/pacientes)
│   │   ├── CitaController.php        (CRUD /api/citas)
│   │   ├── HealthController.php      (GET /api/health, /api/estadisticas)
│   │   └── ApiController.php         (Rutas antiguas)
│   │
│   ├── Service/                  ← Lógica de Negocios
│   │   ├── AuthService.php
│   │   │   ├── login($email, $password)
│   │   │   ├── verificarContraseña($pass, $hash)
│   │   │   ├── formatearUsuario($usuario)
│   │   │   └── verificarToken($token)
│   │   │
│   │   ├── PacienteService.php
│   │   │   ├── listarTodos()
│   │   │   ├── obtenerPorId($id)
│   │   │   ├── buscarPorDocumento($doc)
│   │   │   ├── crear($datos)
│   │   │   ├── actualizar($id, $datos)
│   │   │   ├── eliminar($id)
│   │   │   └── formatear($paciente)
│   │   │
│   │   └── CitaService.php
│   │       ├── listarTodas()
│   │       ├── obtenerPorId($id)
│   │       ├── listarPorPaciente($id)
│   │       ├── listarPorDoctor($id)
│   │       ├── crear($datos)
│   │       ├── actualizar($id, $datos)
│   │       ├── eliminar($id)
│   │       └── formatear($cita)
│   │
│   ├── Entity/                   ← Modelos de BD
│   │   ├── Usuario.php
│   │   │   ├── #id (PK)
│   │   │   ├── nombre
│   │   │   ├── email (UNIQUE)
│   │   │   ├── contraseña
│   │   │   ├── rol (doctor|secretaria|admin)
│   │   │   └── activo (bool)
│   │   │
│   │   ├── Paciente.php
│   │   │   ├── #id (PK)
│   │   │   ├── nombre
│   │   │   ├── documento (UNIQUE)
│   │   │   ├── edad
│   │   │   ├── email
│   │   │   ├── alergias
│   │   │   └── antecedentes_medicos
│   │   │
│   │   └── Cita.php
│   │       ├── #id (PK)
│   │       ├── paciente_id (FK → Paciente)
│   │       ├── doctor_id (FK → Usuario)
│   │       ├── fecha
│   │       ├── hora
│   │       ├── especialidad
│   │       ├── estado (confirmada|completada|cancelada)
│   │       └── motivo
│   │
│   ├── Util/                    ← Helpers Reutilizables
│   │   ├── JwtUtil.php
│   │   │   ├── encode(payload): string
│   │   │   ├── decode(token): array
│   │   │   └── extraerDelHeader(request): string
│   │   │
│   │   └── ResponseUtil.php
│   │       ├── success(data, status=200)
│   │       ├── error(message, status=400)
│   │       └── paginated(data, page, limit)
│   │
│   ├── Repository/               ← Auto-generado por Doctrine
│   │
│   └── Kernel.php               ← Núcleo Symfony
│
├── config/
│   ├── services.yaml            ← Inyección de dependencias
│   └── routes/
│       └── (Rutas automáticas)
│
├── public/
│   └── index.php                ← Punto de entrada
│
├── .env                         ← Variables de entorno
├── .env.example                 ← Plantilla
├── composer.json                ← Dependencias PHP
├── composer.lock                ← Versiones instaladas
│
├── ESTRUCTURA.md                ← Este documento (estructura)
├── CLIENTE_SERVIDOR.md          ← Flujo cliente-servidor
├── TESTING.md                   ← Cómo probar
├── ARQUITECTURA.md              ← Buenas prácticas
├── README.md                    ← Setup inicial
└── DIAGRAMAS.md                 ← Diagramas visuales
```

---

## 4️⃣ Stack Tecnológico

```
┌─────────────────────────────────────────────────┐
│           FRONTEND (HTML/CSS/JS)                │
│  docs/index.html                                │
│  docs/login.html                                │
│  docs/dashboard.html                            │
│  docs/style.css                                 │
│  docs/script.js                                 │
│  docs/config.js                                 │
└────────────────┬────────────────────────────────┘
                 │
                 │ fetch() HTTP
                 │ JSON
                 ↓
┌─────────────────────────────────────────────────┐
│         BACKEND (Symfony 7 + PHP 8.2)           │
│                                                 │
│  Controllers → Services → Repositories → BD    │
│                   ↓                              │
│         Doctrine ORM (Entity Management)        │
│                   ↓                              │
│      Firebase\JWT (JWT Token Generation)       │
│                   ↓                              │
│         PDO + Doctrine DBAL (SQL Driver)       │
└────────────────┬────────────────────────────────┘
                 │
                 │ PDO Connection
                 │ SQL Queries
                 ↓
┌─────────────────────────────────────────────────┐
│     DATABASE (PostgreSQL on Supabase)           │
│  Host: ikqwnmcowwakkxjwevbr.supabase.co        │
│  Port: 5432                                     │
│  Database: postgres                             │
│  Credentials: postgres:Sismas50mas              │
│                                                 │
│  Tables:                                        │
│  - usuarios (doctors, secretaries, admins)     │
│  - pacientes (children)                         │
│  - citas (appointments)                         │
│  - historias_clinicas (medical records)        │
│  - documentos (attachments)                     │
│  - sesiones (legacy)                            │
└─────────────────────────────────────────────────┘
```

---

## 5️⃣ Flujo: Crear Paciente

```
┌─────────────────────────────────────────────────┐
│ FRONTEND: dashboard.html                        │
│ Click: "Agregar Paciente"                       │
│ Llenar form:                                    │
│  - nombre: "Maria"                              │
│  - apellido: "Lopez"                            │
│  - documento: "11111111"                        │
│  - edad: 4                                      │
└────────────────┬────────────────────────────────┘
                 │
                 │ JSON.stringify({...})
                 │
                 ↓
┌─────────────────────────────────────────────────┐
│ fetch POST /api/pacientes                       │
│ Body: {                                         │
│   "nombre": "Maria",                            │
│   "apellido": "Lopez",                          │
│   "documento": "11111111",                      │
│   "edad": 4                                     │
│ }                                               │
└────────────────┬────────────────────────────────┘
                 │
                 ↓ HTTP POST
╔═════════════════════════════════════════════════╗
║ 1. SYMPHONY ROUTER                              ║
║    URL: /api/pacientes                          ║
║    Method: POST                                 ║
║    → PacienteController::crear()                ║
╠═════════════════════════════════════════════════╣
║ 2. PACIENTECONTROLLER::CREAR()                  ║
║    $data = json_decode($request)                ║
║    $paciente = $this->service->crear($data)    ║
║    if (error) return ResponseUtil::error()     ║
║    return ResponseUtil::success($paciente, 201)║
╠═════════════════════════════════════════════════╣
║ 3. PACIENTESERVICE::CREAR()                     ║
║    ├─ Validar documento único                   ║
║    │  if (findOneBy(['documento'])) throw      ║
║    │                                            ║
║    ├─ Crear entidad Paciente                    ║
║    │  $p = new Paciente()                       ║
║    │  $p->setNombre("Maria")                    ║
║    │  ...etc                                    ║
║    │                                            ║
║    ├─ Persistir en BD                           ║
║    │  $this->em->persist($p)                    ║
║    │  $this->em->flush()                        ║
║    │                                            ║
║    └─ Retornar paciente                         ║
║       return $p                                 ║
╠═════════════════════════════════════════════════╣
║ 4. DOCTRINE ORM                                 ║
║    ├─ INSERT INTO pacientes (...)               ║
║    ├─ VALUES (...)                              ║
║    └─ RETURNING id → 6                          ║
╠═════════════════════════════════════════════════╣
║ 5. PACIENTESERVICE::FORMATEAR()                 ║
║    return [                                     ║
║      'id' => 6,                                 ║
║      'nombre' => 'Maria',                       ║
║      'documento' => '11111111',                 ║
║      ...                                        ║
║    ]                                            ║
╠═════════════════════════════════════════════════╣
║ 6. RESPONSEUTIL::SUCCESS()                      ║
║    return JsonResponse([                        ║
║      'status' => 201,                           ║
║      'message' => 'Success',                    ║
║      'data' => {...}                            ║
║    ], 201)                                      ║
╚═════════════════════════════════════════════════╝
                 ↑ JSON
                 │
┌────────────────┴────────────────────────────────┐
│ 201 Created                                     │
│ {                                               │
│   "status": 201,                                │
│   "message": "Success",                         │
│   "data": {                                     │
│     "id": 6,                                    │
│     "nombre": "Maria",                          │
│     "apellido": "Lopez",                        │
│     "documento": "11111111",                    │
│     "edad": 4,                                  │
│     "creado_en": "2024-01-15 10:30:45"         │
│   }                                             │
│ }                                               │
└────────────────┬────────────────────────────────┘
                 │
                 ↓ JSON.parse()
┌────────────────┴────────────────────────────────┐
│ FRONTEND: Almacenar paciente                    │
│ - Agregar a tabla                               │
│ - Mostrar mensaje "Paciente creado"             │
│ - Actualizar lista                              │
│ - Limpiar formulario                            │
└─────────────────────────────────────────────────┘
```

---

## 6️⃣ Manejo de Errores

```
┌──────────────────────────────┐
│ POST /api/pacientes          │
│ Documento: "98765432"        │
│ (Ya existe)                  │
└──────────────┬───────────────┘
               │
         ↓ PacienteService
         
         ├─ findOneBy(['documento'])
         │  = Paciente existente
         │
         └─ throw new Exception(
               'Documento ya existe'
            )
            
         ↑ PacienteController
         
         ├─ catch (Exception $e)
         │
         └─ ResponseUtil::error(
               'Documento ya existe',
               400
            )

┌──────────────────────────────┐
│ 400 Bad Request              │
│ {                            │
│   "status": 400,             │
│   "message": "Error",        │
│   "error": "Documento        │
│            ya existe"        │
│ }                            │
└──────────────┬───────────────┘
               │
         ↓ Cliente (JS)
         
         catch (error) {
           alert('Documento ya existe');
         }
```

---

## 7️⃣ Ciclo Completo: Login → Dashboard → Crear Paciente

```
START
  │
  ├─→ Usuario abre login.html
  │
  ├─→ Ingresa credenciales
  │       email: doctor@clinica.com
  │       contraseña: 123456
  │
  ├─→ fetch POST /api/auth/login
  │       └─→ AuthController → AuthService
  │       └─→ JwtUtil::encode()
  │       └─→ ResponseUtil::success()
  │       └─ 200 OK + token
  │
  ├─→ localStorage.setItem('token', token)
  │
  ├─→ Redirigir a dashboard.html
  │
  ├─→ Dashboard.html carga
  │       addEventListener('DOMContentLoaded')
  │       → fetch GET /api/estadisticas
  │           (Con Authorization header + token)
  │       → Mostrar stats
  │
  ├─→ Usuario click "Agregar Paciente"
  │
  ├─→ Modal abre
  │
  ├─→ Llenar formulario (nombre, edad, etc)
  │
  ├─→ Click "Guardar"
  │       → fetch POST /api/pacientes
  │       → Con token en Authorization
  │       → PacienteService::crear()
  │       → EntityManager::persist()
  │       → EntityManager::flush()
  │       → 201 Created
  │
  ├─→ Mostrar "Paciente creado exitosamente"
  │
  ├─→ Actualizar tabla de pacientes
  │       → fetch GET /api/pacientes
  │       → Mostrar lista actualizada
  │
  └─→ END
```

---

## 8️⃣ Base de Datos: Relaciones

```
┌──────────────────────┐
│      USUARIOS        │
│ (Doctors/Secretaries)│
├──────────────────────┤
│ #id (PK)             │
│ nombre               │
│ email (UNIQUE)       │
│ contraseña           │
│ rol                  │
│ especialidad         │
│ activo               │
└──────────────────────┘
        │
        │ 1:Many (One doctor → Many appointments)
        │
        ↓
┌──────────────────────────┐         ┌───────────────────┐
│        CITAS             │         │   PACIENTES       │
├──────────────────────────┤←────────┤───────────────────┤
│ #id (PK)                 │ FK      │ #id (PK)          │
│ paciente_id (FK) ────────┼─────────┼→ documento(UNIQUE)│
│ doctor_id (FK) ──────┐   │         │ nombre            │
│ fecha                │   │         │ edad              │
│ hora                 │   │         │ alergias          │
│ especialidad         │   │         │ email             │
│ estado               │   │         │ telefono          │
│ motivo               │   │         │ creado_en         │
└──────────────────────────┘         └───────────────────┘
                                               │
                                         1:Many
                                               │
                                               ↓
```

**Relaciones:**
- 1 Usuario (doctor) → Many Citas
- 1 Paciente → Many Citas
- 1 Usuario (especialidad) ← Many Citas

---

## 9️⃣ Tokens JWT: Estructura

```
REQUEST HEADER:
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwi...

DECODED TOKEN:
{
  "iss": "http://localhost:8000"
  "aud": null
  "iat": 1705316400
  "exp": 1705318200,          ← Expira en 30 minutos
  "id": 1,                     ← ID del usuario
  "email": "doctor@clinica.com"
  "rol": "doctor"
}

VERIFICACIÓN:
1. Extraer token del header
2. Decodificar con JWT_SECRET
3. Verificar que no expiró (exp > now)
4. Si OK → Permitir acceso
5. Si NO → Retornar 401 Unauthorized
```

---

## 🔟 Estados de Cita

```
CONFIRMADA
    │
    └─→ (Usuario va a la cita)
        │
        ↓
    COMPLETADA ← (Doctor termina)
    
o

CONFIRMADA
    │
    └─→ (Usuario no puede ir)
        │
        ↓
    CANCELADA
```

**Estados en BD:**
```sql
ALTER TABLE citas
ADD CONSTRAINT check_estado 
CHECK (estado IN ('confirmada', 'completada', 'cancelada'));
```

---

## 🎯 Flujo de Validaciones

```
POST /api/pacientes
│
├─ ¿Email y contraseña en body?
│   └─ NO → 400 Bad Request
│
├─ ¿Documento válido?
│   └─ NO → 400 Bad Request
│
├─ ¿Documento ya existe?
│   └─ SÍ → 400 Bad Request "Ya existe"
│
├─ ¿Token válido?
│   └─ NO → 401 Unauthorized
│
├─ ¿Usuario activo?
│   └─ NO → 401 Unauthorized
│
├─ ✅ Todas las validaciones OK
│
└─ CREATE Paciente
   RETURN 201 Created
```

---

✅ **Diagrama visual completo del sistema** 🎨

