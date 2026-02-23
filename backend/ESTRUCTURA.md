# 🏥 Clínica Pediátrica - Backend Symfony (Estructura Profesional)

## 📁 Estructura del Proyecto

```
backend/
├── src/
│   ├── Controller/           ← Endpoints API REST
│   │   ├── AuthController.php        (Login, autenticación)
│   │   ├── PacienteController.php    (CRUD pacientes)
│   │   ├── CitaController.php        (CRUD citas)
│   │   ├── HealthController.php      (Health check, estadísticas)
│   │   └── ApiController.php         (Endpoints antiguos)
│   │
│   ├── Entity/               ← Modelos de Base de Datos
│   │   ├── Usuario.php       (Doctor, secretaria, admin)
│   │   ├── Paciente.php      (Datos del paciente)
│   │   └── Cita.php          (Cita médica)
│   │
│   ├── Service/              ← Lógica de Negocios
│   │   ├── AuthService.php   (Maneja login, JWT)
│   │   ├── PacienteService.php (CRUD pacientes)
│   │   └── CitaService.php   (CRUD citas)
│   │
│   ├── Repository/           ← Acceso a Datos
│   │   └── (Auto-generado por Doctrine)
│   │
│   ├── Util/                 ← Utilidades y Helpers
│   │   ├── JwtUtil.php       (Codificar/decodificar JWT)
│   │   └── ResponseUtil.php  (Formatear respuestas API)
│   │
│   └── Kernel.php            ← Núcleo de Symfony
│
├── config/
│   ├── services.yaml         ← Inyección de dependencias
│   └── routes/               ← Configuración de rutas
│
├── public/
│   └── index.php             ← Punto de entrada
│
├── .env                      ← Variables de entorno
├── .env.example              ← Plantilla .env
├── composer.json             ← Dependencias PHP
└── README.md                 ← Este archivo

```

## 🎯 Separación de Responsabilidades

### **Controllers** (Solicitudes HTTP)
Reciben requests, validan inputs, llaman servicios, retornan respuestas.

**Ejemplo:**
```php
POST /api/pacientes
- Recibe JSON con datos
- Valida formato
- Llama PacienteService::crear()
- Retorna respuesta formateada
```

### **Services** (Lógica de Negocios)
Manejan la lógica, validaciones, interactúan con BD.

**Ejemplo:**
```php
PacienteService::crear()
- Valida documento único
- Crea entidad Paciente
- Persiste en BD
- Retorna datos
```

### **Entities** (Modelos de BD)
Representan tablas de base de datos.

**Ejemplo:**
```php
class Paciente
{
    #[ORM\Column]
    private string $nombre;
    
    // Getters/setters
}
```

### **Utils** (Helpers Reutilizables)
Funciones auxiliares sin lógica de negocio.

**Ejemplo:**
```php
JwtUtil::encode()   // Codificar token
JwtUtil::decode()   // Validar token
ResponseUtil::success()  // Respuesta exitosa
ResponseUtil::error()    // Respuesta error
```

---

## 📡 Endpoints API

### Autenticación
```
POST /api/auth/login
GET  /api/auth/me
```

### Pacientes
```
GET  /api/pacientes           → Listar todos
POST /api/pacientes           → Crear nuevo
GET  /api/pacientes/{id}      → Obtener uno
PUT  /api/pacientes/{id}      → Actualizar
DELETE /api/pacientes/{id}    → Eliminar
```

### Citas
```
GET    /api/citas             → Listar todas
POST   /api/citas             → Crear nueva
GET    /api/citas/{id}        → Obtener una
PUT    /api/citas/{id}        → Actualizar
DELETE /api/citas/{id}        → Eliminar
```

### Sistema
```
GET  /api/health              → Health check
GET  /api/estadisticas        → Estadísticas dashboard
```

---

## 🚀 Flujo de una Solicitud

```
1. Cliente envía POST /api/pacientes
           ↓
2. Symfony enruta a PacienteController::crear()
           ↓
3. Controller extrae datos del request
           ↓
4. Controller llama PacienteService::crear($datos)
           ↓
5. Service valida datos
           ↓
6. Service crea entidad Paciente
           ↓
7. Service persiste en BD (EntityManager)
           ↓
8. Service retorna Paciente
           ↓
9. Controller formatea con PacienteService::formatear()
           ↓
10. Controller retorna ResponseUtil::success()
           ↓
11. Symfony serializa a JSON
           ↓
12. Cliente recibe respuesta JSON
```

---

## 🔐 Buenas Prácticas Implementadas

✅ **Separación de responsabilidades** - Controllers, Services, Entities separados  
✅ **Inyección de dependencias** - Services inyectados en Controllers  
✅ **DRY (Don't Repeat Yourself)** - Lógica reutilizable en Services  
✅ **Type hints** - Todo tipado (PHP 8.2)  
✅ **Documentación** - Comments en cada clase/método  
✅ **Manejo de errores** - Try/catch con mensajes claros  
✅ **Respuestas consistentes** - ResponseUtil para todas las respuestas  
✅ **Validación de datos** - En Services antes de acceder BD  

---

##  Credenciales de Prueba

```
Email: doctor@clinica.com
Contraseña: 123456
Rol: doctor

Email: secretaria@clinica.com
Contraseña: 123456
Rol: secretaria

Email: admin@clinica.com
Contraseña: 123456
Rol: admin
```

---

## ⚙️ Configuración

<details>
<summary><strong>Variables de Entorno (.env)</strong></summary>

```
# Base de Datos Supabase
DATABASE_URL=postgresql://postgres:password@host.supabase.co:5432/postgres

# JWT
JWT_SECRET=tu-clave-jwt-super-segura

# App
APP_ENV=dev
APP_DEBUG=1
```

</details>

---

## 📚 Ejemplo: Crear un Nuevo Endpoint

### 1. Crear método en Service

```php
// src/Service/UsuarioService.php
public function listarDoctores(): array
{
    $doctores = $this->em->getRepository(Usuario::class)
        ->findBy(['rol' => 'doctor']);
    return array_map(fn($u) => $this->formatear($u), $doctores);
}
```

### 2. Crear método en Controller

```php
// src/Controller/UsuarioController.php
#[Route('/usuarios/doctores', methods: ['GET'])]
public function listarDoctores(): JsonResponse
{
    try {
        $doctores = $this->usuarioService->listarDoctores();
        return ResponseUtil::success($doctores);
    } catch (\Exception $e) {
        return ResponseUtil::error($e->getMessage(), 400);
    }
}
```

### 3. ¡Listo! Endpoint disponible

```bash
GET /api/usuarios/doctores
```

---

## 🐛 Debugging

### Ver logs de la aplicación

```bash
tail -f var/log/dev.log
```

### Ejecutar queries SQL directo

```bash
php bin/console dbal:run-sql "SELECT * FROM pacientes;"
```

---

## 🚀 Próximos pasos

1. **Instalar Composer** (si no lo hiciste)
2. **Ejecutar migraciones** para crear tablas
3. **Iniciar servidor** con `php -S localhost:8000 -t public`
4. **Probar endpoints** con Postman/curl
5. **Desplegar en Railway** cuando esté listo

---

¿Preguntas? Revisa los comentarios en el código 👍
