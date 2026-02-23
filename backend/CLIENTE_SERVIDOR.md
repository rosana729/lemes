# 🔄 Flujo: Cliente ↔ Servidor

## 🌐 Diagrama General

```
┌─────────────────────────────────────────────────────────────────┐
│                        NAVEGADOR (Frontend)                      │
│                                                                   │
│  docs/login.html → fetch POST /api/auth/login → JSON response   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓ HTTP
                              ↓ JSON
┌─────────────────────────────────────────────────────────────────┐
│                        SERVIDOR PHP/Symfony                      │
│                                                                   │
│  1. AuthController recibe POST /api/auth/login                  │
│  2. Extrae email, contraseña del JSON                           │
│  3. Llama AuthService::login(email, contraseña)                 │
│  4. Service valida en BD                                        │
│  5. Service genera JWT token                                    │
│  6. Controller retorna {access_token, usuario}                  │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↑ JSON
                              ↑ 200 OK
```

---

## 👤 Ejemplo 1: Login

### REQUEST (Cliente)
```javascript
// docs/login.html
fetch('http://localhost:8000/api/auth/login', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        email: 'doctor@clinica.com',
        contraseña: '123456'
    })
})
```

### PROCESAMIENTO (Servidor)

#### 1️⃣ Controller
```php
// backend/src/Controller/AuthController.php
#[Route('/api/auth/login', methods: ['POST'])]
public function login(Request $request): JsonResponse
{
    $data = json_decode($request->getContent(), true);
    
    // Validar que existan email y contraseña
    if (!isset($data['email'], $data['contraseña'])) {
        return ResponseUtil::error('Email y contraseña requeridos', 400);
    }
    
    try {
        $usuario = $this->authService->login(
            $data['email'], 
            $data['contraseña']
        );
        return ResponseUtil::success($usuario);
    } catch (\Exception $e) {
        return ResponseUtil::error($e->getMessage(), 401);
    }
}
```

#### 2️⃣ Service
```php
// backend/src/Service/AuthService.php
public function login(string $email, string $contraseña): array
{
    // Buscar usuario en BD
    $usuario = $this->em->getRepository(Usuario::class)
        ->findOneBy(['email' => $email]);
    
    if (!$usuario) {
        throw new \Exception('Usuario no encontrado');
    }
    
    if (!$usuario->isActivo()) {
        throw new \Exception('Usuario inactivo');
    }
    
    // Verificar contraseña
    if (!$this->verificarContraseña($contraseña, $usuario->getContraseña())) {
        throw new \Exception('Contraseña incorrecta');
    }
    
    // Generar JWT
    $token = JwtUtil::encode([
        'id' => $usuario->getId(),
        'email' => $usuario->getEmail(),
        'rol' => $usuario->getRol()
    ]);
    
    // Retornar usuario + token
    return [
        'access_token' => $token,
        'usuario' => $this->formatearUsuario($usuario)
    ];
}
```

#### 3️⃣ Entidad (Modelo)
```php
// backend/src/Entity/Usuario.php
#[ORM\Table(name: 'usuarios')]
class Usuario
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;
    
    #[ORM\Column(length: 255)]
    private string $email;
    
    #[ORM\Column(length: 255)]
    private string $contraseña;
    
    #[ORM\Column]
    private bool $activo = true;
    
    // Getters/Setters...
}
```

#### 4️⃣ Utilidad (Helper)
```php
// backend/src/Util/JwtUtil.php
public static function encode(array $payload): string
{
    return JWT::encode(
        $payload,
        $_ENV['JWT_SECRET'],
        'HS256'
    );
}

public static function decode(string $token): mixed
{
    return JWT::decode(
        $token,
        new Key($_ENV['JWT_SECRET'], 'HS256')
    );
}
```

### RESPONSE (Servidor → Cliente)
```json
{
    "status": 200,
    "message": "Success",
    "data": {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "usuario": {
            "id": 1,
            "nombre": "Dr. Juan",
            "email": "doctor@clinica.com",
            "rol": "doctor",
            "especialidad": "Pediatría"
        }
    }
}
```

### ALMACENAMIENTO (Cliente)
```javascript
// docs/script.js
const usuario = respuesta.data.usuario;
const token = respuesta.data.access_token;

localStorage.setItem('usuario', JSON.stringify(usuario));
localStorage.setItem('token', token);

// Redirigir a dashboard
location.href = '/Lemes/dashboard.html';
```

---

## 👶 Ejemplo 2: Crear Paciente

### REQUEST (Cliente)
```javascript
// docs/dashboard.html
const token = localStorage.getItem('token');

fetch('http://localhost:8000/api/pacientes', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
    },
    body: JSON.stringify({
        nombre: 'Juan',
        apellido: 'Pérez',
        documento: '12345678',
        edad: 5,
        telefono: '1234567890',
        email: 'juan@mail.com',
        alergias: 'Ninguna',
        antecedentes_medicos: 'Ninguno'
    })
})
```

### PROCESAMIENTO (Servidor)

#### 1️⃣ Controller
```php
// backend/src/Controller/PacienteController.php
#[Route('/api/pacientes', methods: ['POST'])]
public function crear(Request $request): JsonResponse
{
    try {
        $data = json_decode($request->getContent(), true);
        
        $paciente = $this->pacienteService->crear($data);
        
        return ResponseUtil::success(
            $this->pacienteService->formatear($paciente),
            201  // Created
        );
    } catch (\Exception $e) {
        return ResponseUtil::error($e->getMessage(), 400);
    }
}
```

#### 2️⃣ Service
```php
// backend/src/Service/PacienteService.php
public function crear(array $datos): Paciente
{
    // Validar documento único
    $existente = $this->em->getRepository(Paciente::class)
        ->findOneBy(['documento' => $datos['documento']]);
    
    if ($existente) {
        throw new \Exception('Documento ya existe');
    }
    
    // Crear entidad
    $paciente = new Paciente();
    $paciente->setNombre($datos['nombre']);
    $paciente->setApellido($datos['apellido']);
    $paciente->setDocumento($datos['documento']);
    $paciente->setEdad($datos['edad']);
    $paciente->setTelefono($datos['telefono']);
    $paciente->setEmail($datos['email']);
    $paciente->setAlergias($datos['alergias'] ?? '');
    $paciente->setAntecedentesMedicos($datos['antecedentes_medicos'] ?? '');
    $paciente->setCreadoEn(new \DateTime());
    
    // Persistir
    $this->em->persist($paciente);
    $this->em->flush();
    
    return $paciente;
}

public function formatear(Paciente $paciente): array
{
    return [
        'id' => $paciente->getId(),
        'nombre' => $paciente->getNombre(),
        'apellido' => $paciente->getApellido(),
        'documento' => $paciente->getDocumento(),
        'edad' => $paciente->getEdad(),
        'telefono' => $paciente->getTelefono(),
        'email' => $paciente->getEmail(),
        'alergias' => $paciente->getAlergias(),
        'antecedentes_medicos' => $paciente->getAntecedentesMedicos(),
        'creado_en' => $paciente->getCreadoEn()?->format('Y-m-d H:i:s')
    ];
}
```

### RESPONSE (Servidor → Cliente)
```json
{
    "status": 201,
    "message": "Success",
    "data": {
        "id": 6,
        "nombre": "Juan",
        "apellido": "Pérez",
        "documento": "12345678",
        "edad": 5,
        "telefono": "1234567890",
        "email": "juan@mail.com",
        "alergias": "Ninguna",
        "antecedentes_medicos": "Ninguno",
        "creado_en": "2024-01-15 10:30:45"
    }
}
```

---

## 📊 Flujo Completo: Listar Pacientes

```
CLIENTE                              SERVIDOR
   │                                    │
   ├─ GET /api/pacientes ──────────────>│
   │                            PacienteController
   │                                    │
   │                          ┌─────────┴──────────┐
   │                          │ 1. Recibir solicitud
   │                          │ 2. Parsear parámetros
   │                          │ 3. Validar autenticación
   │
   │                          ├─ pacienteService.listarTodos()
   │                          │    │
   │                          │    ├─ Buscar en BD
   │                          │    ├─ EntityManager::find()
   │                          │    ├─ Array de Pacientes
   │                          │    └─ Formatear cada uno
   │                          │
   │                          ├─ ResponseUtil::success()
   │                          └─ JSON con datos
   │
   │<───────── 200 JSON ───────────────┤
   │
   ├─ Procesar datos
   ├─ Mostrar en HTML
   └─ Actualizar UI
```

---

## 🔐 Flujo de Autenticación

```
1. USUARIO INGRESA CREDENCIALES
   └─> POST /api/auth/login

2. SERVER VALIDA EN BD
   ├─ ¿Existe usuario?
   ├─ ¿Contraseña correcta?
   └─ ¿Usuario activo?

3. SERVER GENERA JWT TOKEN
   └─> JwtUtil::encode({id, email, rol})

4. SERVER RETORNA TOKEN + USUARIO
   └─> localStorage.setItem('token', token)

5. CLIENTE ENVÍA REQUESTS CON TOKEN
   └─> Authorization: Bearer <token>

6. SERVER VALIDA TOKEN
   └─> JwtUtil::decode(token)
   └─> ¿Token válido? ¿No expiró?

7. SI TODO OK → PROCESA SOLICITUD
   └─> Devuelve datos

8. SI FALLA → RECHAZA
   └─> 401 Unauthorized
```

---

## ⚠️ Códigos HTTP Utilizados

| Código | Significado | Ejemplo |
|--------|------------|---------|
| **200** | OK | GET pacientes exitoso |
| **201** | Created | Paciente creado |
| **400** | Bad Request | Datos inválidos |
| **401** | Unauthorized | Token inválido/expirado |
| **404** | Not Found | Paciente no existe |
| **500** | Server Error | Error en servidor |

---

## 📝 Checklist de Prueba

- [ ] Login funciona y retorna token
- [ ] Token se almacena en localStorage
- [ ] GET /api/pacientes retorna lista
- [ ] POST /api/pacientes crea nuevo paciente
- [ ] GET /api/pacientes/{id} obtiene uno
- [ ] PUT /api/pacientes/{id} actualiza
- [ ] DELETE /api/pacientes/{id} elimina
- [ ] Validaciones funcionan (documento único, etc.)
- [ ] Headers CORS presentes
- [ ] Respuestas siempre en formato JSON

---

## 🐛 Debugging

### Ver variables en el request

```php
// AuthController.php
dd($data);  // Mostrar datos recibidos
```

### Ver SQL generado

```bash
php bin/console dbal:run-sql "SELECT * FROM usuarios WHERE email = 'doctor@clinica.com';"
```

### Probar JWT manualmente

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"doctor@clinica.com","contraseña":"123456"}'
```

---

✅ **Sistema funcionando cuando:**
1. POST /api/auth/login retorna token
2. GET /api/pacientes retorna lista con token
3. Frontend puede acceder a datos
4. Respuestas siempre en formato JSON

¡Listo! 🚀
