-- ════════════════════════════════════════════════════════════════════════════
-- 🏥 CLÍNICA PEDIÁTRICA - ESQUEMA COMPLETO PARA SUPABASE
-- ════════════════════════════════════════════════════════════════════════════
-- Ejecuta este script en Supabase > SQL Editor
-- ════════════════════════════════════════════════════════════════════════════

-- ════════════════════════════════════════════════════════════════════════════
-- 1️⃣ TABLA: USUARIOS (Doctores, Secretarias, Admins)
-- ════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    contraseña VARCHAR(255) NOT NULL,
    rol VARCHAR(20) DEFAULT 'doctor' CHECK (rol IN ('doctor', 'secretaria', 'admin')),
    especialidad VARCHAR(100),
    telefono VARCHAR(20),
    activo BOOLEAN DEFAULT true,
    creado_en TIMESTAMP WITH TIME ZONE DEFAULT now(),
    actualizado_en TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Índices para usuarios
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_usuarios_rol ON usuarios(rol);

-- ════════════════════════════════════════════════════════════════════════════
-- 2️⃣ TABLA: SESIONES DE USUARIOS
-- ════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS sesiones (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    token VARCHAR(500) NOT NULL UNIQUE,
    ip_address VARCHAR(45),
    user_agent TEXT,
    activa BOOLEAN DEFAULT true,
    fecha_login TIMESTAMP WITH TIME ZONE DEFAULT now(),
    fecha_logout TIMESTAMP WITH TIME ZONE,
    fecha_expiracion TIMESTAMP WITH TIME ZONE DEFAULT (now() + INTERVAL '7 days'),
    creado_en TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Índices para sesiones
CREATE INDEX idx_sesiones_usuario_id ON sesiones(usuario_id);
CREATE INDEX idx_sesiones_token ON sesiones(token);
CREATE INDEX idx_sesiones_activa ON sesiones(activa);

-- ════════════════════════════════════════════════════════════════════════════
-- 3️⃣ TABLA: PACIENTES
-- ════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS pacientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    documento VARCHAR(20) UNIQUE NOT NULL,
    fecha_nacimiento VARCHAR(10),
    edad INTEGER,
    genero VARCHAR(10),
    telefono VARCHAR(20) NOT NULL,
    email VARCHAR(100),
    direccion VARCHAR(200),
    ciudad VARCHAR(100),
    alergias TEXT,
    antecedentes_medicos TEXT,
    creado_en TIMESTAMP WITH TIME ZONE DEFAULT now(),
    actualizado_en TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Índices para pacientes
CREATE INDEX idx_pacientes_documento ON pacientes(documento);
CREATE INDEX idx_pacientes_email ON pacientes(email);
CREATE INDEX idx_pacientes_apellido ON pacientes(apellido);

-- ════════════════════════════════════════════════════════════════════════════
-- 4️⃣ TABLA: CITAS
-- ════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS citas (
    id SERIAL PRIMARY KEY,
    paciente_id INTEGER NOT NULL REFERENCES pacientes(id) ON DELETE CASCADE,
    doctor_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE SET NULL,
    fecha VARCHAR(10) NOT NULL,
    hora VARCHAR(5) NOT NULL,
    especialidad VARCHAR(100) NOT NULL,
    motivo TEXT,
    estado VARCHAR(20) DEFAULT 'programada' CHECK (estado IN ('programada', 'realizada', 'cancelada')),
    notas TEXT,
    creado_en TIMESTAMP WITH TIME ZONE DEFAULT now(),
    actualizado_en TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Índices para citas
CREATE INDEX idx_citas_paciente_id ON citas(paciente_id);
CREATE INDEX idx_citas_doctor_id ON citas(doctor_id);
CREATE INDEX idx_citas_fecha ON citas(fecha);
CREATE INDEX idx_citas_estado ON citas(estado);

-- ════════════════════════════════════════════════════════════════════════════
-- 5️⃣ TABLA: HISTORIAS CLÍNICAS
-- ════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS historias_clinicas (
    id SERIAL PRIMARY KEY,
    paciente_id INTEGER NOT NULL REFERENCES pacientes(id) ON DELETE CASCADE,
    doctor_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE SET NULL,
    
    -- Signos Vitales
    presion_arterial VARCHAR(20),
    frecuencia_cardiaca INTEGER,
    temperatura FLOAT,
    saturacion_o2 INTEGER,
    peso FLOAT,
    talla FLOAT,
    imc FLOAT,
    
    -- Anamnesis
    motivo_consulta TEXT,
    enfermedad_actual TEXT,
    sintomas_principales TEXT,
    
    -- Antecedentes
    antecedentes_personales TEXT,
    antecedentes_familiares TEXT,
    medicacion_actual TEXT,
    alergias_medicamentos TEXT,
    habitos TEXT,
    
    -- Examen Físico
    examen_general TEXT,
    sistema_cardiovascular TEXT,
    sistema_respiratorio TEXT,
    abdomen TEXT,
    neurologia TEXT,
    
    -- Estudios Complementarios
    laboratorio TEXT,
    imagenes TEXT,
    otros_estudios TEXT,
    
    -- Diagnóstico
    diagnostico_principal TEXT,
    diagnosticos_secundarios TEXT,
    codigos_cie10 TEXT,
    
    -- Impresión Diagnóstica
    impresion TEXT,
    plan_accion TEXT,
    
    -- Tratamiento
    medicamentos_prescriptos TEXT,
    indicaciones TEXT,
    proxima_cita VARCHAR(10),
    
    creado_en TIMESTAMP WITH TIME ZONE DEFAULT now(),
    actualizado_en TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Índices para historias clínicas
CREATE INDEX idx_historias_paciente_id ON historias_clinicas(paciente_id);
CREATE INDEX idx_historias_doctor_id ON historias_clinicas(doctor_id);

-- ════════════════════════════════════════════════════════════════════════════
-- 6️⃣ TABLA: DOCUMENTOS (Archivos adjuntos)
-- ════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS documentos (
    id SERIAL PRIMARY KEY,
    paciente_id INTEGER NOT NULL REFERENCES pacientes(id) ON DELETE CASCADE,
    historia_clinica_id INTEGER REFERENCES historias_clinicas(id) ON DELETE SET NULL,
    
    nombre VARCHAR(200) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    tamaño INTEGER,
    ruta VARCHAR(300) NOT NULL,
    descripcion TEXT,
    
    creado_en TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Índices para documentos
CREATE INDEX idx_documentos_paciente_id ON documentos(paciente_id);
CREATE INDEX idx_documentos_historia_id ON documentos(historia_clinica_id);

-- ════════════════════════════════════════════════════════════════════════════
-- 📊 INSERTAR DATOS DE PRUEBA
-- ════════════════════════════════════════════════════════════════════════════

-- ════════════════════════════════════════════════════════════════════════════
-- DATOS DE PRUEBA: USUARIOS
-- ════════════════════════════════════════════════════════════════════════════

INSERT INTO usuarios (nombre, email, contraseña, rol, especialidad, telefono, activo) VALUES
('Dr. Carlos García López', 'doctor@clinica.com', '$2b$12$abcdefghijklmnopqrstuvwxyz123456', 'doctor', 'Pediatría', '555-0001', true),
('Dra. María González Rodríguez', 'doctor2@clinica.com', '$2b$12$abcdefghijklmnopqrstuvwxyz123456', 'doctor', 'Pediatría y Neonatología', '555-0002', true),
('Lic. Ana Martínez López', 'secretaria@clinica.com', '$2b$12$abcdefghijklmnopqrstuvwxyz123456', 'secretaria', NULL, '555-0003', true),
('Admin Clínica', 'admin@clinica.com', '$2b$12$abcdefghijklmnopqrstuvwxyz123456', 'admin', NULL, '555-0004', true),
('Dr. Pedro Ramírez Silva', 'doctor3@clinica.com', '$2b$12$abcdefghijklmnopqrstuvwxyz123456', 'doctor', 'Cardiología Pediátrica', '555-0005', true);

-- ════════════════════════════════════════════════════════════════════════════
-- DATOS DE PRUEBA: SESIONES
-- ════════════════════════════════════════════════════════════════════════════

INSERT INTO sesiones (usuario_id, token, ip_address, user_agent, activa, fecha_expiracion) VALUES
(1, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjogMSwgInJvbCI6ICJkb2N0b3IifQ.signature1', '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', true, now() + INTERVAL '7 days'),
(2, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjogMiwgInJvbCI6ICJkb2N0b3IifQ.signature2', '192.168.1.101', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)', true, now() + INTERVAL '7 days'),
(3, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjogMywgInJvbCI6ICJzZWNyZXRhcmlhIn0.signature3', '192.168.1.102', 'Mozilla/5.0 (X11; Linux x86_64)', true, now() + INTERVAL '7 days');

-- ════════════════════════════════════════════════════════════════════════════
-- DATOS DE PRUEBA: PACIENTES
-- ════════════════════════════════════════════════════════════════════════════

INSERT INTO pacientes (nombre, apellido, documento, fecha_nacimiento, edad, genero, telefono, email, direccion, ciudad, alergias, antecedentes_medicos) VALUES
('Juan', 'Pérez García', '12345678', '2020-05-15', 4, 'Masculino', '555-1001', 'juan.perez@email.com', 'Calle Principal 123', 'Buenos Aires', 'Penicilina', 'Asma leve'),
('María', 'López Rodríguez', '87654321', '2019-03-22', 5, 'Femenino', '555-1002', 'maria.lopez@email.com', 'Avenida Central 456', 'Buenos Aires', 'Ninguna', 'Alergia estacional'),
('Carlos', 'Martínez Silva', '11223344', '2021-07-10', 3, 'Masculino', '555-1003', 'carlos.martinez@email.com', 'Calle Norte 789', 'Córdoba', 'Ninguna', 'Ninguno'),
('Sofía', 'González Fernández', '55667788', '2018-11-03', 6, 'Femenino', '555-1004', 'sofia.gonzalez@email.com', 'Avenida Sur 321', 'Rosario', 'Lactosa', 'Gastritis'),
('Diego', 'Ramírez Castro', '99001122', '2022-01-20', 2, 'Masculino', '555-1005', 'diego.ramirez@email.com', 'Calle Este 654', 'La Plata', 'Ninguna', 'Ninguno');

-- ════════════════════════════════════════════════════════════════════════════
-- DATOS DE PRUEBA: CITAS
-- ════════════════════════════════════════════════════════════════════════════

INSERT INTO citas (paciente_id, doctor_id, fecha, hora, especialidad, motivo, estado, notas) VALUES
(1, 1, '2026-02-25', '10:30', 'Pediatría', 'Revisión anual', 'programada', 'Traer carné de vacunación'),
(2, 1, '2026-02-25', '11:00', 'Pediatría', 'Tos persistente', 'programada', 'Control de síntomas'),
(3, 2, '2026-02-26', '09:00', 'Pediatría y Neonatología', 'Evaluación del crecimiento', 'programada', NULL),
(4, 2, '2026-02-26', '14:30', 'Pediatría y Neonatología', 'Alergia', 'programada', 'Traer muestras de alimentos'),
(1, 1, '2026-02-20', '15:00', 'Pediatría', 'Resfriado', 'realizada', 'Se prescribió paracetamol');

-- ════════════════════════════════════════════════════════════════════════════
-- DATOS DE PRUEBA: HISTORIAS CLÍNICAS
-- ════════════════════════════════════════════════════════════════════════════

INSERT INTO historias_clinicas (
    paciente_id, doctor_id,
    presion_arterial, frecuencia_cardiaca, temperatura, saturacion_o2, peso, talla, imc,
    motivo_consulta, enfermedad_actual, sintomas_principales,
    antecedentes_personales, antecedentes_familiares, medicacion_actual, alergias_medicamentos, habitos,
    examen_general, sistema_cardiovascular, sistema_respiratorio, abdomen, neurologia,
    laboratorio, imagenes, otros_estudios,
    diagnostico_principal, diagnosticos_secundarios, codigos_cie10,
    impresion, plan_accion,
    medicamentos_prescriptos, indicaciones, proxima_cita
) VALUES
(
    1, 1,
    '110/70', 95, 36.8, 99, 18.5, 105, 16.8,
    'Revisión anual de salud', 'Paciente en buen estado general', 'Ninguno',
    'Nacimiento: normal. Desarrollo: normal', 'Padre con diabetes tipo 2', 'Ninguna', 'Penicilina', 'Duerme 8 horas diarias',
    'Paciente activo, coloración rosa, bien hidratado', 'Ritmo cardíaco regular', 'Murmullo vesicular bilateral', 'Blando, depresible', 'Alerta, reactivo',
    'Hemograma: normal', 'Radiografía de tórax: normal', NULL,
    'Niño sano, sin patología evidente', 'Desarrollo psicomotor normal', 'Z72.0',
    'Paciente asintomático, crecimiento adecuado', 'Seguimiento en 6 meses. Continuar con vacunaciones',
    'Multivitamínico pediátrico 1 dosis diaria', 'Mantener buena nutrición, actividad física diaria', '2026-08-25'
),
(
    2, 1,
    '105/65', 88, 37.5, 98, 19.2, 108, 16.5,
    'Tos persistente', 'Tos seca por 5 días, sin fiebre', 'Tos seca, sin fiebre',
    'Antecedentes de alergia estacional', 'Madre con asma alérgico', 'Ninguna', 'Ninguna', 'Activo, juega diariamente',
    'Mucosas rosadas, sin cianosis', 'RCN regular, sin soplos', 'Estertores finos bilaterales', 'Normal', 'Normal',
    'Radiografía de tórax: congestión leve', NULL, NULL,
    'Bronquitis viral aguda', 'Alergia aéreo ambiental', 'J20.9',
    'Probable infección viral de vías aéreas superiores', 'Reposo, líquidos abundantes, monitoreo',
    'Antitusígeno 5ml cada 6 horas, paracetamol si fiebre', 'Aumentar ingesta de líquidos, evitar irritantes aéreos', '2026-03-10'
),
(
    3, 2,
    '100/60', 92, 36.6, 99, 16.8, 98, 17.5,
    'Evaluación del crecimiento', 'Crecimiento dentro de lo esperado', 'Ninguno',
    'Parto vaginal. Peso al nacer: 3.2kg. Talla: 50cm', 'Ningún antecedente relevante', 'Fórmula infantil enriquecida', 'Ninguna', 'Buen apetito',
    'Aspecto general bueno', 'Frecuencia cardíaca regular', 'Respiración tranquila', 'Normal, blando', 'Reactivo',
    NULL, NULL, 'Evaluación antropométrica: dentro de percentiles normales',
    'Crecimiento y desarrollo normal', NULL, 'Z99.9',
    'Lactante de 3 años en óptimas condiciones', 'Seguimiento nutricional mensual',
    'Vitamina D 400 UI diariamente', 'Dieta balanceada, actividad física adecuada', '2026-03-25'
);

-- ════════════════════════════════════════════════════════════════════════════
-- DATOS DE PRUEBA: DOCUMENTOS
-- ════════════════════════════════════════════════════════════════════════════

INSERT INTO documentos (paciente_id, historia_clinica_id, nombre, tipo, tamaño, ruta, descripcion) VALUES
(1, 1, 'Carné de vacunación', 'jpg', 245632, '/documentos/paciente_1/carnet_vacunacion.jpg', 'Carné de vacunación actualizado'),
(1, 1, 'Resultado análisis sangre', 'pdf', 156789, '/documentos/paciente_1/analisis_sangre_2026.pdf', 'Hemograma de enero 2026'),
(2, 2, 'Radiografía de tórax', 'jpg', 425600, '/documentos/paciente_2/radiografia_torax.jpg', 'Radiografía del 2026-02-22'),
(3, 3, 'Tabla de crecimiento', 'pdf', 98765, '/documentos/paciente_3/tabla_crecimiento.pdf', 'Gráficos de peso y talla'),
(4, NULL, 'Reporte de alergia', 'pdf', 125000, '/documentos/paciente_4/test_alergia.pdf', 'Test de alergia realizado en 2025');

-- ════════════════════════════════════════════════════════════════════════════
-- ✅ VERIFICAR QUE TODO ESTÁ CREADO
-- ════════════════════════════════════════════════════════════════════════════

-- Contar registros en cada tabla
SELECT 'USUARIOS' as tabla, COUNT(*) as total FROM usuarios
UNION ALL
SELECT 'SESIONES', COUNT(*) FROM sesiones
UNION ALL
SELECT 'PACIENTES', COUNT(*) FROM pacientes
UNION ALL
SELECT 'CITAS', COUNT(*) FROM citas
UNION ALL
SELECT 'HISTORIAS_CLINICAS', COUNT(*) FROM historias_clinicas
UNION ALL
SELECT 'DOCUMENTOS', COUNT(*) FROM documentos;

-- ════════════════════════════════════════════════════════════════════════════
-- 🔑 CREDENCIALES DE PRUEBA
-- ════════════════════════════════════════════════════════════════════════════
/*

USUARIOS DE PRUEBA (Contraseña: todas tienen hash de "123456"):

👨‍⚕️ DOCTOR 1:
Email: doctor@clinica.com
Contraseña: 123456
Rol: doctor
Especialidad: Pediatría

👩‍⚕️ DOCTOR 2:
Email: doctor2@clinica.com
Contraseña: 123456
Rol: doctor
Especialidad: Pediatría y Neonatología

👩‍💼 SECRETARIA:
Email: secretaria@clinica.com
Contraseña: 123456
Rol: secretaria

🔐 ADMIN:
Email: admin@clinica.com
Contraseña: 123456
Rol: admin

👨‍⚕️ DOCTOR 3:
Email: doctor3@clinica.com
Contraseña: 123456
Rol: doctor
Especialidad: Cardiología Pediátrica

═════════════════════════════════════════════════════════════════════════════

PACIENTES:
1. Juan Pérez García (4 años)
2. María López Rodríguez (5 años)
3. Carlos Martínez Silva (3 años)
4. Sofía González Fernández (6 años)
5. Diego Ramírez Castro (2 años)

═════════════════════════════════════════════════════════════════════════════
*/

-- ════════════════════════════════════════════════════════════════════════════
-- 📋 NOTAS IMPORTANTES
-- ════════════════════════════════════════════════════════════════════════════
/*

1. Las contraseñas están hasheadas con bcrypt (hash de "123456")
   En producción, DEBE usar contraseñas reales y más seguras.

2. Los tokens de sesión son ejemplos. El servidor debe generar tokens JWT reales.

3. Las tablas tienen "ON DELETE CASCADE" para mantener integridad referencial.

4. Se crearon índices en columnas frecuentemente consultadas para mejor performance.

5. Todos los timestamps usan TIMESTAMP WITH TIME ZONE para mejor manejo horario.

6. La tabla sesiones permite rastrear usuario logins/logouts.

7. Los documentos pueden estar ligados a historias clínicas o solo a pacientes.

═════════════════════════════════════════════════════════════════════════════
*/
