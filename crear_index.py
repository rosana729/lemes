#!/usr/bin/env python3
# -*- coding: utf-8 -*-

html_content = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏥 Clínica Pediátrica</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .login-container { display: flex; align-items: center; justify-content: center; min-height: 100vh; }
        .login-container.hidden { display: none; }
        .login-box { background: white; padding: 40px; border-radius: 15px; width: 100%; max-width: 400px; box-shadow: 0 10px 40px rgba(0,0,0,0.3); }
        .login-box h1 { color: #667eea; margin-bottom: 30px; text-align: center; }
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; margin-bottom: 5px; color: #333; font-weight: 600; }
        .form-group input, .form-group select { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 6px; }
        .btn { width: 100%; padding: 12px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 6px; font-size: 1em; font-weight: 600; cursor: pointer; }
        .btn:hover { transform: scale(1.02); }
        .demo-creds { margin-top: 20px; padding-top: 20px; border-top: 1px solid #e0e0e0; font-size: 0.85em; color: #666; }
        .header { display: none; background: white; padding: 20px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        .header.active { display: flex; justify-content: space-between; align-items: center; }
        .header h1 { color: #667eea; }
        .user-info { text-align: right; }
        .user-info .email { font-weight: 600; color: #333; }
        .user-info .rol { color: #667eea; font-size: 0.9em; }
        .logout-btn { background: #f44; color: white; padding: 8px 16px; border: none; border-radius: 6px; cursor: pointer; margin-left: 15px; }
        .main-content { display: none; }
        .main-content.active { display: block; }
        .dashboard { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px; }
        .card { background: white; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        .card .number { font-size: 2.5em; font-weight: bold; color: #667eea; }
        .card .label { color: #666; font-size: 0.9em; margin-top: 5px; }
        .tabs { display: flex; gap: 10px; margin-bottom: 20px; border-bottom: 2px solid #e0e0e0; }
        .tab-btn { background: transparent; border: none; color: #667eea; padding: 10px 20px; cursor: pointer; font-weight: 600; border-bottom: 3px solid transparent; }
        .tab-btn.active { border-bottom-color: #667eea; }
        .section { background: white; padding: 25px; border-radius: 12px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); margin-bottom: 20px; display: none; }
        .section.active { display: block; }
        .section h2 { color: #667eea; margin-bottom: 20px; border-bottom: 2px solid #667eea; padding-bottom: 10px; }
        .form-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; }
        textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 6px; font-family: inherit; min-height: 80px; resize: vertical; }
        table { width: 100%; border-collapse: collapse; }
        th { background: #f5f5f5; padding: 12px; text-align: left; font-weight: bold; border-bottom: 2px solid #ddd; }
        td { padding: 12px; border-bottom: 1px solid #e0e0e0; }
        tr:hover { background: #f9f9f9; }
        .empty { text-align: center; padding: 30px; color: #999; }
    </style>
</head>
<body>
    <div id="loginContainer" class="login-container">
        <div class="login-box">
            <h1>🏥 Clínica Pediátrica</h1>
            <form onsubmit="handleLogin(event)">
                <div class="form-group">
                    <label>Email:</label>
                    <input type="email" id="email" placeholder="doctor@clinica.com" required>
                </div>
                <div class="form-group">
                    <label>Contraseña:</label>
                    <input type="password" id="password" placeholder="123456" required>
                </div>
                <button type="submit" class="btn">Iniciar Sesión</button>
            </form>
            <div class="demo-creds">
                <strong>Prueba con:</strong><br>
                👨‍⚕️ doctor@clinica.com / 123456<br>
                👩‍💼 secretaria@clinica.com / 123456<br>
                👤 admin@clinica.com / 123456
            </div>
        </div>
    </div>
    <div class="container">
        <div id="header" class="header">
            <h1>🏥 Clínica Pediátrica</h1>
            <div style="display: flex; align-items: center;">
                <div class="user-info">
                    <div class="email" id="usuarioEmail"></div>
                    <div class="rol" id="usuarioRol"></div>
                </div>
                <button class="logout-btn" onclick="handleLogout()">Cerrar Sesión</button>
            </div>
        </div>
        <div id="mainContent" class="main-content">
            <div class="dashboard">
                <div class="card"><div style="font-size: 2.5em;">👶</div><div class="number" id="totalPacientes">0</div><div class="label">Pacientes</div></div>
                <div class="card"><div style="font-size: 2.5em;">📋</div><div class="number" id="totalCitas">0</div><div class="label">Citas</div></div>
                <div class="card"><div style="font-size: 2.5em;">👨‍⚕️</div><div class="number" id="totalDoctores">0</div><div class="label">Doctores</div></div>
            </div>
            <div class="tabs">
                <button class="tab-btn active" onclick="switchTab(event, 'pacientes')">👶 Pacientes</button>
                <button class="tab-btn" onclick="switchTab(event, 'historias')">📄 Historias</button>
                <button class="tab-btn" onclick="switchTab(event, 'citas')">📅 Citas</button>
            </div>
            <div id="pacientes" class="section active">
                <h2>Gestión de Pacientes</h2>
                <div class="form-row">
                    <div class="form-group"><label>Nombre:</label><input type="text" id="pacNombre" placeholder="Nombre"></div>
                    <div class="form-group"><label>Apellido:</label><input type="text" id="pacApellido" placeholder="Apellido"></div>
                </div>
                <div class="form-row">
                    <div class="form-group"><label>Documento:</label><input type="text" id="pacDocumento" placeholder="1234567-8"></div>
                    <div class="form-group"><label>Teléfono:</label><input type="text" id="pacTelefono"></div>
                </div>
                <button class="btn" onclick="crearPaciente()" style="width: auto; padding: 10px 30px;">Guardar Paciente</button>
                <hr style="margin: 20px 0; border: none; border-top: 1px solid #e0e0e0;">
                <h3 style="margin-bottom: 15px;">Pacientes Registrados:</h3>
                <div id="listaPacientes" class="empty">Cargando...</div>
            </div>
            <div id="historias" class="section">
                <h2>Historias Clínicas</h2>
                <div class="form-group"><label>Selecciona Paciente:</label><select id="histPaciente" onchange="cargarHistoriasDelPaciente()"><option value="">-- Selecciona un paciente --</option></select></div>
                <div id="formularioHistoria" style="display: none;">
                    <h3 style="color: #667eea; margin-top: 20px; margin-bottom: 15px;">Registro de Consulta</h3>
                    <div class="form-group"><label>Motivo de Consulta:</label><textarea id="histMotivo" placeholder="¿Por qué viene el paciente?"></textarea></div>
                    <div class="form-group"><label>Diagnóstico:</label><textarea id="histDiagnostico" placeholder="Diagnóstico"></textarea></div>
                    <button class="btn" onclick="crearHistoria()" style="width: auto; padding: 10px 30px;">Guardar Historia</button>
                </div>
                <hr style="margin: 20px 0; border: none; border-top: 1px solid #e0e0e0;">
                <div id="listaHistorias" class="empty">Selecciona un paciente</div>
            </div>
            <div id="citas" class="section">
                <h2>Gestión de Citas</h2>
                <div class="form-row">
                    <div class="form-group"><label>Paciente:</label><select id="citaPaciente"><option value="">-- Selecciona paciente --</option></select></div>
                    <div class="form-group"><label>Doctor:</label><select id="citaDoctor"><option value="">-- Selecciona doctor --</option></select></div>
                </div>
                <div class="form-row">
                    <div class="form-group"><label>Fecha:</label><input type="date" id="citaFecha"></div>
                    <div class="form-group"><label>Hora:</label><input type="time" id="citaHora"></div>
                </div>
                <button class="btn" onclick="crearCita()" style="width: auto; padding: 10px 30px;">Programar Cita</button>
                <hr style="margin: 20px 0; border: none; border-top: 1px solid #e0e0e0;">
                <h3 style="margin-bottom: 15px;">Citas Programadas:</h3>
                <div id="listaCitas" class="empty">Cargando...</div>
            </div>
        </div>
    </div>
    <script src="/api.js"></script>
    <script>
        const api = new ClinicaAPI();
        async function handleLogin(e) {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const result = await api.login(email, password);
            if (result.success) {
                document.getElementById('loginContainer').classList.add('hidden');
                document.getElementById('header').classList.add('active');
                document.getElementById('mainContent').classList.add('active');
                document.getElementById('usuarioEmail').textContent = result.usuario.email;
                document.getElementById('usuarioRol').textContent = result.usuario.rol;
                cargarDatos();
                cargarSelects();
            } else {
                alert('Credenciales inválidas: ' + (result.error || 'Error'));
            }
        }
        function handleLogout() {
            api.logout();
            document.getElementById('loginContainer').classList.remove('hidden');
            document.getElementById('header').classList.remove('active');
            document.getElementById('mainContent').classList.remove('active');
        }
        function switchTab(e, tab) {
            document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.getElementById(tab).classList.add('active');
            e.target.classList.add('active');
        }
        async function cargarDatos() {
            const stats = await api.obtenerEstadisticas();
            if (stats && !stats.error) {
                document.getElementById('totalPacientes').textContent = stats.total_pacientes || 0;
                document.getElementById('totalCitas').textContent = stats.total_citas || 0;
                document.getElementById('totalDoctores').textContent = stats.total_doctores || 0;
            }
            await cargarPacientes();
            await cargarCitas();
        }
        async function cargarSelects() {
            const pacientes = await api.obtenerPacientes();
            if (pacientes && !pacientes.error) {
                const sel1 = document.getElementById('histPaciente');
                const sel2 = document.getElementById('citaPaciente');
                sel1.innerHTML = '<option value="">-- Selecciona un paciente --</option>';
                sel2.innerHTML = '<option value="">-- Selecciona un paciente --</option>';
                pacientes.forEach(p => {
                    sel1.innerHTML += '<option value="' + p.id + '">' + p.nombre + ' ' + p.apellido + '</option>';
                    sel2.innerHTML += '<option value="' + p.id + '">' + p.nombre + ' ' + p.apellido + '</option>';
                });
            }
            const usuarios = await api.obtenerUsuarios();
            if (usuarios) {
                const docSel = document.getElementById('citaDoctor');
                docSel.innerHTML = '<option value="">-- Selecciona doctor --</option>';
                usuarios.filter(u => u.rol === 'doctor').forEach(u => {
                    docSel.innerHTML += '<option value="' + u.id + '">' + u.nombre + '</option>';
                });
            }
        }
        async function cargarPacientes() {
            const pacientes = await api.obtenerPacientes();
            const lista = document.getElementById('listaPacientes');
            if (!pacientes || pacientes.error || pacientes.length === 0) {
                lista.innerHTML = '<div class="empty">No hay pacientes</div>';
                return;
            }
            let html = '<table><tr><th>Nombre</th><th>Documento</th><th>Teléfono</th></tr>';
            pacientes.forEach(p => {
                html += '<tr><td>' + p.nombre + ' ' + p.apellido + '</td><td>' + p.documento + '</td><td>' + (p.telefono || '-') + '</td></tr>';
            });
            html += '</table>';
            lista.innerHTML = html;
        }
        async function crearPaciente() {
            const datos = {
                nombre: document.getElementById('pacNombre').value,
                apellido: document.getElementById('pacApellido').value,
                documento: document.getElementById('pacDocumento').value,
                telefono: document.getElementById('pacTelefono').value,
                email: '',
                edad: null,
                genero: '',
                alergias: '',
                antecedentes_medicos: '',
                fecha_nacimiento: null
            };
            const result = await api.crearPaciente(datos);
            if (result.error) {
                alert('Error: ' + result.error);
            } else {
                document.getElementById('pacNombre').value = '';
                document.getElementById('pacApellido').value = '';
                document.getElementById('pacDocumento').value = '';
                document.getElementById('pacTelefono').value = '';
                cargarPacientes();
                cargarSelects();
                alert('Paciente creado correctamente');
            }
        }
        async function cargarHistoriasDelPaciente() {
            const pacienteId = document.getElementById('histPaciente').value;
            if (!pacienteId) {
                document.getElementById('formularioHistoria').style.display = 'none';
                document.getElementById('listaHistorias').innerHTML = '<div class="empty">Selecciona un paciente</div>';
                return;
            }
            document.getElementById('formularioHistoria').style.display = 'block';
            const historias = await api.obtenerHistoriasPaciente(pacienteId);
            const lista = document.getElementById('listaHistorias');
            if (!historias || historias.error || historias.length === 0) {
                lista.innerHTML = '<div class="empty">No hay historias</div>';
                return;
            }
            let html = '<table><tr><th>Fecha</th><th>Motivo</th></tr>';
            historias.forEach(h => {
                html += '<tr><td>' + new Date(h.creado_en).toLocaleDateString() + '</td><td>' + (h.motivo_consulta || '-') + '</td></tr>';
            });
            html += '</table>';
            lista.innerHTML = html;
        }
        async function crearHistoria() {
            const pacienteId = document.getElementById('histPaciente').value;
            const datos = {
                paciente_id: parseInt(pacienteId),
                doctor_id: api.usuario.id,
                motivo_consulta: document.getElementById('histMotivo').value,
                diagnostico_principal: document.getElementById('histDiagnostico').value,
                presion_arterial: null,
                frecuencia_cardiaca: null,
                temperatura: null,
                saturacion_o2: null,
                enfermedad_actual: '',
                antecedentes_personales: '',
                antecedentes_familiares: '',
                medicacion_actual: '',
                alergias_medicamentos: '',
                laboratorio: '',
                imagenes: '',
                diagnosticos_secundarios: '',
                impresion: '',
                plan_accion: '',
                medicamentos_prescriptos: '',
                indicaciones: ''
            };
            const result = await api.crearHistoria(datos);
            if (result.error) {
                alert('Error: ' + result.error);
            } else {
                document.getElementById('histMotivo').value = '';
                document.getElementById('histDiagnostico').value = '';
                cargarHistoriasDelPaciente();
                alert('Historia creada correctamente');
            }
        }
        async function cargarCitas() {
            const citas = await api.obtenerCitasDoctor(api.usuario.id);
            const lista = document.getElementById('listaCitas');
            if (!citas || citas.length === 0) {
                lista.innerHTML = '<div class="empty">No hay citas</div>';
                return;
            }
            let html = '<table><tr><th>Paciente</th><th>Fecha</th><th>Hora</th><th>Estado</th></tr>';
            citas.forEach(c => {
                html += '<tr><td>Pac. ' + c.paciente_id + '</td><td>' + c.fecha + '</td><td>' + c.hora + '</td><td>' + c.estado + '</td></tr>';
            });
            html += '</table>';
            lista.innerHTML = html;
        }
        async function crearCita() {
            const datos = {
                paciente_id: parseInt(document.getElementById('citaPaciente').value),
                doctor_id: parseInt(document.getElementById('citaDoctor').value),
                fecha: document.getElementById('citaFecha').value,
                hora: document.getElementById('citaHora').value,
                especialidad: '',
                motivo: '',
                estado: 'programada'
            };
            const result = await api.crearCita(datos);
            if (result.error) {
                alert('Error: ' + result.error);
            } else {
                document.getElementById('citaPaciente').value = '';
                document.getElementById('citaDoctor').value = '';
                document.getElementById('citaFecha').value = '';
                document.getElementById('citaHora').value = '';
                cargarCitas();
                alert('Cita programada correctamente');
            }
        }
    </script>
</body>
</html>'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✅ Archivo index.html creado correctamente")
