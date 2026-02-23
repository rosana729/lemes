# 🏗️ Arquitectura: Malas vs Buenas Prácticas

## ❌ MAL: Todo en un archivo (Spaghetti Code)

```php
<?php
// ❌ MALO: api_viejo.php (todo mezclado)

$email = $_POST['email'] ?? '';
$contraseña = $_POST['contraseña'] ?? '';

try {
    // Conectar BD
    $pdo = new PDO('postgresql://...');
    
    // Validar usuario (mezclado con lógica de BD)
    $stmt = $pdo->prepare('SELECT * FROM usuarios WHERE email = ?');
    $stmt->execute([$email]);
    $usuario = $stmt->fetch();
    
    if (!$usuario) {
        die(json_encode(['error' => 'Usuario no encontrado']));
    }
    
    // Validar contraseña (sin separación)
    if (!password_verify($contraseña, $usuario['contraseña'])) {
        die(json_encode(['error' => 'Contraseña incorrecta']));
    }
    
    // Generar JWT (sin utilidad reutilizable)
    $token = \Firebase\JWT\JWT::encode([
        'id' => $usuario['id'],
        'email' => $usuario['email']
    ], $_ENV['JWT_SECRET'], 'HS256');
    
    // Formatear respuesta (sin utilidad)
    echo json_encode([
        'status' => 200,
        'token' => $token,
        'usuario' => [
            'id' => $usuario['id'],
            'nombre' => $usuario['nombre'],
            'email' => $usuario['email']
        ]
    ]);
    
} catch (Exception $e) {
    // Manejo de errores genérico
    die(json_encode(['error' => $e->getMessage()]));
}

// Mismo archivo maneja: Validación, BD, JWT, Respuesta, Errores
// Resultado: Código repetido, difícil de mantener, difícil de testear
```

**Problemas:**
- ❌ Lógica de validación mezclada con BD
- ❌ JWT encoding sin reutilización
- ❌ Formato de respuesta inconsistente
- ❌ Si cambia contraseña → cambiar en 50 lugares
- ❌ Imposible testear sin BD real
- ❌ Difícil encontrar bugs

---

## ✅ BIEN: Separación de responsabilidades

```
AuthController.php          ← Recibe HTTP, valida input, llama service
    ↓
AuthService.php             ← Lógica: login, validación
    ↓
JwtUtil.php                 ← Generar/verificar tokens (reutilizable)
    ↓
ResponseUtil.php            ← Formatear JSON (reutilizable)
    ↓
Database (via Doctrine)     ← Acceso a datos
```

### 1️⃣ Controller: HTTP

```php
// ✅ BIEN: AuthController.php

#[Route('/api/auth/login', methods: ['POST'])]
public function login(Request $request): JsonResponse
{
    try {
        $data = json_decode($request->getContent(), true);
        
        $usuario = $this->authService->login(
            $data['email'], 
            $data['contraseña']
        );
        
        return ResponseUtil::success($usuario);
    } catch (Exception $e) {
        return ResponseUtil::error($e->getMessage(), 401);
    }
}

// Responsabilidad: Solo manejo de HTTP
// - Recibir request
// - Parsear datos
// - Delegar a service
// - Devolver respuesta
```

### 2️⃣ Service: Lógica

```php
// ✅ BIEN: AuthService.php

public function login(string $email, string $contraseña): array
{
    // Buscar usuario
    $usuario = $this->em->getRepository(Usuario::class)
        ->findOneBy(['email' => $email]);
    
    if (!$usuario) {
        throw new Exception('Usuario no encontrado');
    }
    
    // Validar activo
    if (!$usuario->isActivo()) {
        throw new Exception('Usuario inactivo');
    }
    
    // Validar contraseña
    if (!$this->verificarContraseña($contraseña, $usuario->getContraseña())) {
        throw new Exception('Contraseña incorrecta');
    }
    
    // Generar token (delegado a JwtUtil)
    $token = JwtUtil::encode([
        'id' => $usuario->getId(),
        'email' => $usuario->getEmail()
    ]);
    
    // Formatear respuesta (delegado a Service)
    return [
        'access_token' => $token,
        'usuario' => $this->formatearUsuario($usuario)
    ];
}

// Responsabilidad: Solo lógica
// - Validar datos
// - Buscar en BD
// - Llamar utilidades
// - Retornar datos limpios
```

### 3️⃣ Utility: Reutilizable

```php
// ✅ BIEN: JwtUtil.php

class JwtUtil
{
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
        return JWT::decode($token, ...);
    }
}

// Responsabilidad: Solo JWT
// Reutilizable en:
// - AuthService
// - AuthController
// - Middleware
// - Tests
```

### 4️⃣ Response Utility: Consistencia

```php
// ✅ BIEN: ResponseUtil.php

class ResponseUtil
{
    public static function success($data, int $status = 200): JsonResponse
    {
        return new JsonResponse([
            'status' => $status,
            'message' => 'Success',
            'data' => $data,
            'headers' => ['Access-Control-Allow-Origin' => '*']
        ]);
    }
    
    public static function error(string $message, int $status = 400): JsonResponse
    {
        return new JsonResponse([
            'status' => $status,
            'message' => 'Error',
            'error' => $message,
            'headers' => ['Access-Control-Allow-Origin' => '*']
        ], $status);
    }
}

// Responsabilidad: Formato JSON consistente
// Reutilizable en: Todos los controllers
```

---

## 📊 Comparación: Arquitectura

### ❌ MONOLÍTICA (Vieja)

```
api_viejo.php (1000+ líneas)
├─ Validación
├─ BD
├─ Lógica
├─ JWT
├─ Respuesta
├─ Errores
└─ TODO MEZCLADO
```

**Problemas:**
- Archivo gigante → imposible leer
- Cambio en una cosa = efectos secundarios
- Código duplicado
- Imposible testear
- Imposible reutilizar

### ✅ MODULAR (Nueva)

```
Controller          (Capa HTTP)
    ↓
Service             (Lógica)
    ↓
Repository/Entity   (Datos)
    ↓
Util                (Helpers)
```

**Ventajas:**
- Cada clase hace UNA cosa
- Cambios sin efectos secundarios
- Código reutilizable
- Fácil testear
- Fácil encontrar bugs

---

## 🎯 Principios Implementados

### 1. Single Responsibility Principle

```php
// ✅ CORRECTO
class AuthService          // Solo lógica de login
class JwtUtil              // Solo tokens
class ResponseUtil         // Solo formato JSON

// ❌ INCORRECTO
class AuthService          // Login + BD + JWT + Respuesta + Errores
```

### 2. Don't Repeat Yourself (DRY)

```php
// ✅ CORRECTO (Reutilizable)
public function formatearUsuario(Usuario $u): array
{
    return [
        'id' => $u->getId(),
        'nombre' => $u->getNombre(),
        ...
    ];
}

// Se usa en: AuthService, UsuarioController, etc.

// ❌ INCORRECTO (Repetido)
// AuthService.php
return ['id' => $u->getId(), 'nombre' => $u->getNombre(), ...];

// UsuarioController.php
return ['id' => $u->getId(), 'nombre' => $u->getNombre(), ...];

// CitaController.php
return ['id' => $u->getId(), 'nombre' => $u->getNombre(), ...];
```

### 3. Dependency Injection

```php
// ✅ CORRECTO (Inyectado)
class AuthController
{
    public function __construct(
        private AuthService $authService
    ) {}
    
    public function login(Request $request): JsonResponse
    {
        // AuthService ya disponible
        $usuario = $this->authService->login(...);
    }
}

// ❌ INCORRECTO (Acoplado)
class AuthController
{
    public function login(Request $request): JsonResponse
    {
        // Crear adentro = acoplamiento
        $authService = new AuthService();
        $usuario = $authService->login(...);
    }
}
```

### 4. Separation of Concerns

```
HTTP Layer          ← Controllers (reciben requests)
    ↓
Business Logic      ← Services (validan, procesan)
    ↓
Data Access         ← Repositories (buscan en BD)
    ↓
Response Layer      ← Utils (formatean JSON)
```

---

## 📈 Escalabilidad

### Con Arquitectura Modular

```
Agregar nueva funcionalidad es fácil:

1. Crear UsuarioController
2. Crear UsuarioService
3. Usar Entity Usuario existente
4. Usar ResponseUtil existente
5. ¡Listo! Endpoint funcional

100 líneas de código vs. 1000 líneas en archivo monolítico
```

### Ejemplo: Agregar endpoint "listar doctores"

```php
// 1. Service
// UsuarioService.php
public function listarDoctores(): array
{
    $doctores = $this->em->getRepository(Usuario::class)
        ->findBy(['rol' => 'doctor']);
    return array_map(fn($u) => $this->formatear($u), $doctores);
}

// 2. Controller
// UsuarioController.php
#[Route('/usuarios/doctores', methods: ['GET'])]
public function listarDoctores(): JsonResponse
{
    $doctores = $this->usuarioService->listarDoctores();
    return ResponseUtil::success($doctores);
}

// ¡Listo! Endpoint /api/usuarios/doctores funcional
// Sin duplicar código
// Sin efectos secundarios
```

---

## 🧪 Testing

### Con Arquitectura Modular

```php
// ✅ FÁCIL de testear
public function testLogin()
{
    $authService = new AuthService($entityManager);
    $usuario = $authService->login('test@mail.com', 'password');
    
    $this->assertEquals('test@mail.com', $usuario['email']);
}

// No necesita servidor, BD real, etc.
```

### Sin Arquitectura Modular

```php
// ❌ DIFÍCIL de testear
$_POST['email'] = 'test@mail.com';  // Simular POST
// Ejecutar api_viejo.php              // ¿Cómo?
// Necesita BD real, conexión, etc.  // Complicado
```

---

## 🔄 Flow Completo

```
┌──────────────────────────────────────────────────┐
│ 1. CLIENT: POST /api/auth/login                  │
│    {email, contraseña}                           │
└──────────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────────┐
│ 2. SYMFONY ROUTER                                │
│    Encontrar AuthController::login()             │
└──────────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────────┐
│ 3. CONTROLLER: AuthController::login()           │
│    - Parsear JSON                                │
│    - Validar campos                              │
│    - Llamar authService.login()                  │
└──────────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────────┐
│ 4. SERVICE: AuthService::login()                 │
│    - Buscar usuario en BD                        │
│    - Validar contraseña                          │
│    - Llamar JwtUtil.encode()                     │
│    - Formatear usuario                           │
└──────────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────────┐
│ 5. UTIL: JwtUtil::encode()                       │
│    - Generar token JWT                           │
│    - Retornar token                              │
└──────────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────────┐
│ 6. SERVICE: Retorna array                        │
│    [access_token, usuario]                       │
└──────────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────────┐
│ 7. CONTROLLER: Retorna response                  │
│    Llama ResponseUtil.success()                  │
└──────────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────────┐
│ 8. UTIL: ResponseUtil::success()                 │
│    - Crear JSON                                  │
│    - Agregar headers                             │
│    - Status 200                                  │
└──────────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────────┐
│ 9. CLIENT: Recibe JSON                           │
│    {status, data: {token, usuario}}              │
│    Guardar token en localStorage                 │
│    Redirigir a dashboard                         │
└──────────────────────────────────────────────────┘
```

---

## 💡 Conclusión

```
ANTES:                          DESPUÉS:
1000 líneas en 1 archivo   →   100 líneas en 10 pequeños

❌ Caótico                  →   ✅ Organizado
❌ Repetitivo              →   ✅ DRY
❌ Acoplado                →   ✅ Desacoplado  
❌ Imposible testear       →   ✅ Fácil testear
❌ Imposible escalar       →   ✅ Escalable

Código que le encantará mantener 🚀
```

