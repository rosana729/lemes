# 🧪 Guía Rápida: Probar API Localmente

## ⚡ Quick Start

```bash
# 1. Instalar Composer (primera vez)
# Descargar desde: https://getcomposer.org/download/

# 2. Instalar dependencias
cd c:\xampp\htdocs\Lemes\backend
composer install

# 3. Iniciar servidor PHP
php -S localhost:8000 -t public

# El servidor estará en: http://localhost:8000
```

---

## 🔑 Test 1: Login

### Con CURL (Command Line)

```bash
curl -X POST http://localhost:8000/api/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"doctor@clinica.com\",\"contraseña\":\"123456\"}"
```

### Con Postman

```
POST http://localhost:8000/api/auth/login
Content-Type: application/json

{
    "email": "doctor@clinica.com",
    "contraseña": "123456"
}
```

### Respuesta esperada (✅ Éxito)

```json
{
    "status": 200,
    "message": "Success",
    "data": {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwi...",
        "usuario": {
            "id": 1,
            "nombre": "Dr. Juan",
            "email": "doctor@clinica.com",
            "rol": "doctor",
            "especialidad": "Pediatría",
            "activo": true
        }
    }
}
```

---

## 👶 Test 2: Listar Pacientes

```bash
# Guardar el token del login anterior
SET TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...

# Listar todos
curl -X GET http://localhost:8000/api/pacientes ^
  -H "Authorization: Bearer %TOKEN%"
```

### Respuesta esperada

```json
{
    "status": 200,
    "message": "Success",
    "data": [
        {
            "id": 1,
            "nombre": "Carlos",
            "apellido": "Rodríguez",
            "documento": "98765432",
            "edad": 7,
            "email": "carlos@mail.com",
            ...
        }
    ]
}
```

---

## ✨ Test 3: Crear Paciente

```bash
curl -X POST http://localhost:8000/api/pacientes ^
  -H "Content-Type: application/json" ^
  -H "Authorization: Bearer %TOKEN%" ^
  -d "{\"nombre\":\"Maria\",\"apellido\":\"Lopez\",\"documento\":\"11111111\",\"edad\":4,\"telefono\":\"1234567890\",\"email\":\"maria@mail.com\",\"alergias\":\"Penicilina\",\"antecedentes_medicos\":\"Asma\"}"
```

### Respuesta esperada (201 Created)

```json
{
    "status": 201,
    "message": "Success",
    "data": {
        "id": 6,
        "nombre": "Maria",
        "apellido": "Lopez",
        "documento": "11111111",
        "edad": 4,
        ...
        "creado_en": "2024-01-15 10:30:45"
    }
}
```

---

## 📋 Test 4: Obtener Paciente Específico

```bash
curl -X GET http://localhost:8000/api/pacientes/1 ^
  -H "Authorization: Bearer %TOKEN%"
```

---

## 📊 Test 5: Estadísticas

```bash
curl -X GET http://localhost:8000/api/estadisticas ^
  -H "Authorization: Bearer %TOKEN%"
```

### Respuesta esperada

```json
{
    "status": 200,
    "message": "Success",
    "data": {
        "total_pacientes": 5,
        "total_citas": 5,
        "total_usuarios": 3,
        "citas_por_estado": {
            "confirmada": 2,
            "completada": 2,
            "cancelada": 1
        },
        "pacientes_por_edad": {
            "0-5": 2,
            "6-10": 2,
            "11-15": 1
        }
    }
}
```

---

## 🏥 Test 6: Gestión de Citas

### Crear cita

```bash
curl -X POST http://localhost:8000/api/citas ^
  -H "Content-Type: application/json" ^
  -H "Authorization: Bearer %TOKEN%" ^
  -d "{\"paciente_id\":1,\"doctor_id\":1,\"fecha\":\"2024-02-15\",\"hora\":\"10:30\",\"especialidad\":\"Pediatría\",\"estado\":\"confirmada\",\"motivo\":\"Control rutinario\"}"
```

### Listar citas

```bash
curl -X GET http://localhost:8000/api/citas ^
  -H "Authorization: Bearer %TOKEN%"
```

### Obtener cita específica

```bash
curl -X GET http://localhost:8000/api/citas/1 ^
  -H "Authorization: Bearer %TOKEN%"
```

### Actualizar cita

```bash
curl -X PUT http://localhost:8000/api/citas/1 ^
  -H "Content-Type: application/json" ^
  -H "Authorization: Bearer %TOKEN%" ^
  -d "{\"estado\":\"completada\"}"
```

### Eliminar cita

```bash
curl -X DELETE http://localhost:8000/api/citas/1 ^
  -H "Authorization: Bearer %TOKEN%"
```

---

## 🧬 Test 7: Búsqueda de Paciente por Documento

```bash
curl -X GET "http://localhost:8000/api/pacientes/documento/98765432" ^
  -H "Authorization: Bearer %TOKEN%"
```

---

## 📝 Test 8: Salud del Servidor

```bash
curl -X GET http://localhost:8000/api/health
```

### Respuesta esperada

```json
{
    "status": 200,
    "message": "Server is running",
    "timestamp": "2024-01-15 10:30:45"
}
```

---

## 🔴 Errores Comunes

### Error: "Token inválido"
```
→ El token expiró (30 minutos)
→ Solución: Hacer login de nuevo
```

### Error: "Usuario no encontrado"
```
→ Email incorrecto
→ Solución: Usar email de prueba correcto
```

### Error: "Documento ya existe"
```
→ Intento crear paciente con documento duplicado
→ Solución: Usar documento único
```

### Error: "Conexión rechazada (localhost:8000)"
```
→ Servidor PHP no está corriendo
→ Solución: Ejecutar `php -S localhost:8000 -t public`
```

### Error: "CORS error"
```
→ Frontend intenta acceder desde dominio diferente
→ Solución: Verificar CORS headers en ResponseUtil
```

---

## 📱 Usuarios de Prueba

```
1. Doctor
   Email: doctor@clinica.com
   Contraseña: 123456
   Rol: doctor

2. Secretaria
   Email: secretaria@clinica.com
   Contraseña: 123456
   Rol: secretaria

3. Admin
   Email: admin@clinica.com
   Contraseña: 123456
   Rol: admin
```

---

## 🎯 Velocidad de Pruebas

### Test Rápido (5 min)
1. ✅ Login: verificar que retorna token
2. ✅ Listar pacientes: verificar que retorna lista
3. ✅ Estadísticas: verificar conteos

### Test Completo (15 min)
1. ✅ Login con diferentes usuarios
2. ✅ CRUD pacientes (crear, leer, actualizar, eliminar)
3. ✅ CRUD citas
4. ✅ Validaciones (documento único, etc)
5. ✅ Errores (token inválido, no encontrado)

### Test de Integración (30 min)
1. ✅ Toda la suite anterior
2. ✅ Probar desde frontend (login.html → dashboard.html)
3. ✅ Verificar localStorage
4. ✅ Verificar CORS headers
5. ✅ Verificar respuestas JSON
6. ✅ Probar en navegador

---

## 📊 Herramientas Recomendadas

**Para Windows:**
- **Postman Desktop** - GUI para probar APIs
- **curl** - Línea de comando (incluido en Windows)
- **PowerShell** - Terminal nativa de Windows

**Online:**
- **Thunder Client** - VS Code extension
- **REST Client** - VS Code extension
- **HTTPie Online** - Web app

---

## 💾 Guardar Responses

### En Postman
1. Hacer request
2. Click "Save" → "Save Response as Example"
3. Para comparar después

### En archivo de texto
```
==== LOGIN ====
POST /api/auth/login
Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...

==== LISTAR PACIENTES ====
GET /api/pacientes
5 pacientes retornados

==== CREAR PACIENTE ====
POST /api/pacientes
ID: 6 creado exitosamente
```

---

## ✅ Checklist Final

- [ ] Servidor PHP corriendo en localhost:8000
- [ ] POST /api/auth/login retorna token
- [ ] GET /api/pacientes retorna lista
- [ ] POST /api/pacientes crea paciente
- [ ] GET /api/pacientes/{id} obtiene uno
- [ ] PUT /api/pacientes/{id} actualiza
- [ ] DELETE /api/pacientes/{id} elimina
- [ ] GET /api/citas retorna citas
- [ ] POST /api/citas crea cita
- [ ] GET /api/estadisticas retorna stats
- [ ] GET /api/health retorna status
- [ ] Headers CORS presentes
- [ ] Errores retornan JSON correcto

---

🎉 **¡Todo funcionando = Listo para integrar con frontend!**

