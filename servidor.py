#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏥 CLÍNICA PEDIÁTRICA - Servidor API Completo
Versión: 1.0.0
"""

import json
import sqlite3
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from datetime import datetime
from pathlib import Path

# Base de datos SQLite
DB_PATH = "clinica.db"

class ClinicaHandler(BaseHTTPRequestHandler):
    """Manejador de requests HTTP para la clínica"""
    
    def do_GET(self):
        """Manejo de GET requests"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)
        
        try:
            # Servir archivos HTML
            if path == '/index.html' or path == '/':
                try:
                    with open('index.html', 'r', encoding='utf-8') as f:
                        html = f.read()
                    self.send_html_response(html)
                    return
                except FileNotFoundError:
                    pass
            
            # Root endpoint (JSON)
            if path == '/':
                self.send_json_response({
                    "status": "healthy",
                    "service": "🏥 Clínica Pediátrica API",
                    "version": "1.0.0",
                    "message": "¡Sistema funcionando!",
                    "timestamp": datetime.now().isoformat()
                })
            
            # Health check
            elif path == '/health':
                self.send_json_response({
                    "status": "healthy",
                    "database": "sqlite3",
                    "uptime": "running"
                })
            
            # Dashboard - Estadísticas
            elif path == '/api/estadisticas':
                stats = self.get_estadisticas()
                self.send_json_response(stats)
            
            # Listar pacientes
            elif path == '/api/pacientes':
                pacientes = self.get_pacientes(query_params.get('skip', ['0'])[0])
                self.send_json_response(pacientes)
            
            # Ver paciente específico
            elif path.startswith('/api/pacientes/'):
                paciente_id = path.split('/')[-1]
                try:
                    paciente_id = int(paciente_id)
                    paciente = self.get_paciente(paciente_id)
                    if paciente:
                        self.send_json_response(paciente)
                    else:
                        self.send_error_response(404, "Paciente no encontrado")
                except:
                    self.send_error_response(400, "ID de paciente inválido")
            
            # Listar consultas
            elif path == '/api/consultas':
                consultas = self.get_consultas()
                self.send_json_response(consultas)
            
            # Listar gastos
            elif path == '/api/gastos':
                gastos = self.get_gastos()
                self.send_json_response(gastos)
            
            # Listar ingresos
            elif path == '/api/ingresos':
                ingresos = self.get_ingresos()
                self.send_json_response(ingresos)
            
            # Swagger UI básico
            elif path == '/docs':
                self.send_html_response(self.get_swagger_ui())
            
            else:
                self.send_error_response(404, "Endpoint no encontrado")
                
        except Exception as e:
            self.send_error_response(500, str(e))
    
    def do_POST(self):
        """Manejo de POST requests"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}
            
            # Crear paciente
            if path == '/api/pacientes':
                if not data.get('cedula') or not data.get('nombre'):
                    self.send_error_response(400, "Cedula y nombre requeridos")
                    return
                
                paciente = self.crear_paciente(data)
                self.send_json_response(paciente, 201)
            
            # Crear consulta
            elif path == '/api/consultas':
                if not data.get('paciente_id') or not data.get('motivo_consulta'):
                    self.send_error_response(400, "paciente_id y motivo_consulta requeridos")
                    return
                
                consulta = self.crear_consulta(data)
                self.send_json_response(consulta, 201)
            
            # Crear gasto
            elif path == '/api/gastos':
                if not data.get('descripcion') or not data.get('monto'):
                    self.send_error_response(400, "descripcion y monto requeridos")
                    return
                
                gasto = self.crear_gasto(data)
                self.send_json_response(gasto, 201)
            
            # Crear ingreso
            elif path == '/api/ingresos':
                if not data.get('descripcion') or not data.get('monto'):
                    self.send_error_response(400, "descripcion y monto requeridos")
                    return
                
                ingreso = self.crear_ingreso(data)
                self.send_json_response(ingreso, 201)
            
            else:
                self.send_error_response(404, "Endpoint no encontrado")
                
        except json.JSONDecodeError:
            self.send_error_response(400, "JSON inválido")
        except Exception as e:
            self.send_error_response(500, str(e))
    
    def do_PUT(self):
        """Manejo de PUT requests"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}
            
            # Actualizar paciente
            if path.startswith('/api/pacientes/'):
                paciente_id = int(path.split('/')[-1])
                paciente = self.actualizar_paciente(paciente_id, data)
                if paciente:
                    self.send_json_response(paciente)
                else:
                    self.send_error_response(404, "Paciente no encontrado")
            else:
                self.send_error_response(404, "Endpoint no encontrado")
                
        except Exception as e:
            self.send_error_response(500, str(e))
    
    def do_DELETE(self):
        """Manejo de DELETE requests"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        try:
            # Eliminar paciente
            if path.startswith('/api/pacientes/'):
                paciente_id = int(path.split('/')[-1])
                if self.eliminar_paciente(paciente_id):
                    self.send_json_response({"message": "Paciente eliminado"})
                else:
                    self.send_error_response(404, "Paciente no encontrado")
            else:
                self.send_error_response(404, "Endpoint no encontrado")
                
        except Exception as e:
            self.send_error_response(500, str(e))
    
    # Métodos de respuesta
    def send_json_response(self, data, status=200):
        """Envía respuesta JSON"""
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2, ensure_ascii=False).encode('utf-8'))
    
    def send_html_response(self, html, status=200):
        """Envía respuesta HTML"""
        self.send_response(status)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def send_error_response(self, status, message):
        """Envía respuesta de error"""
        self.send_json_response({
            "error": True,
            "status": status,
            "message": message
        }, status)
    
    # Métodos de base de datos
    def init_db(self):
        """Inicializa la base de datos"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Tabla pacientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pacientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cedula VARCHAR(50) UNIQUE NOT NULL,
                nombre VARCHAR(100) NOT NULL,
                apellido VARCHAR(100) NOT NULL,
                email VARCHAR(100),
                telefono VARCHAR(20),
                fecha_nacimiento DATE,
                direccion TEXT,
                alergias TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla consultas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS consultas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER NOT NULL,
                fecha_consulta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                motivo_consulta TEXT NOT NULL,
                diagnostico TEXT,
                peso REAL,
                altura REAL,
                temperatura REAL,
                presion_arterial VARCHAR(20),
                monto_consulta REAL DEFAULT 0,
                estado_pago VARCHAR(20) DEFAULT 'pendiente',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
            )
        ''')
        
        # Tabla gastos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS gastos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descripcion VARCHAR(255) NOT NULL,
                monto REAL NOT NULL,
                categoria VARCHAR(100),
                fecha_gasto TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla ingresos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ingresos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descripcion VARCHAR(255) NOT NULL,
                monto REAL NOT NULL,
                tipo VARCHAR(100),
                paciente_id INTEGER,
                consulta_id INTEGER,
                fecha_ingreso TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
                FOREIGN KEY (consulta_id) REFERENCES consultas(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_pacientes(self, skip=0):
        """Obtiene lista de pacientes con paginación"""
        try:
            skip = int(skip)
        except:
            skip = 0
        
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM pacientes ORDER BY created_at DESC LIMIT 10 OFFSET ?', (skip * 10,))
        pacientes = [dict(row) for row in cursor.fetchall()]
        
        cursor.execute('SELECT COUNT(*) as total FROM pacientes')
        total = cursor.fetchone()['total']
        
        conn.close()
        
        return {
            "items": pacientes,
            "total": total,
            "skip": skip,
            "limit": 10
        }
    
    def get_paciente(self, paciente_id):
        """Obtiene un paciente específico"""
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM pacientes WHERE id = ?', (paciente_id,))
        paciente = cursor.fetchone()
        conn.close()
        
        return dict(paciente) if paciente else None
    
    def crear_paciente(self, data):
        """Crea un nuevo paciente"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO pacientes (cedula, nombre, apellido, email, telefono, fecha_nacimiento, direccion, alergias)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.get('cedula'),
                data.get('nombre'),
                data.get('apellido'),
                data.get('email', ''),
                data.get('telefono', ''),
                data.get('fecha_nacimiento', ''),
                data.get('direccion', ''),
                data.get('alergias', '')
            ))
            conn.commit()
            
            paciente_id = cursor.lastrowid
            conn.close()
            
            return {
                "id": paciente_id,
                "cedula": data.get('cedula'),
                "nombre": data.get('nombre'),
                "apellido": data.get('apellido'),
                "email": data.get('email'),
                "created_at": datetime.now().isoformat()
            }
        except sqlite3.IntegrityError:
            conn.close()
            return {"error": "Cédula duplicada"}
    
    def actualizar_paciente(self, paciente_id, data):
        """Actualiza un paciente"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Verificar que existe
        cursor.execute('SELECT * FROM pacientes WHERE id = ?', (paciente_id,))
        if not cursor.fetchone():
            conn.close()
            return None
        
        # Actualizar campos que se proporcionan
        updates = []
        values = []
        for key in ['nombre', 'apellido', 'email', 'telefono', 'direccion', 'alergias']:
            if key in data:
                updates.append(f"{key} = ?")
                values.append(data[key])
        
        if updates:
            values.append(paciente_id)
            query = f"UPDATE pacientes SET {', '.join(updates)}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
            cursor.execute(query, values)
            conn.commit()
        
        conn.close()
        return self.get_paciente(paciente_id)
    
    def eliminar_paciente(self, paciente_id):
        """Elimina un paciente"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM pacientes WHERE id = ?', (paciente_id,))
        conn.commit()
        
        deleted = cursor.rowcount > 0
        conn.close()
        
        return deleted
    
    def get_consultas(self):
        """Obtiene todas las consultas"""
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM consultas ORDER BY fecha_consulta DESC LIMIT 50')
        consultas = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return {"items": consultas, "total": len(consultas)}
    
    def crear_consulta(self, data):
        """Crea una nueva consulta"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO consultas (paciente_id, motivo_consulta, diagnostico, peso, altura, temperatura, presion_arterial, monto_consulta)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('paciente_id'),
            data.get('motivo_consulta'),
            data.get('diagnostico', ''),
            data.get('peso'),
            data.get('altura'),
            data.get('temperatura'),
            data.get('presion_arterial', ''),
            data.get('monto_consulta', 0)
        ))
        conn.commit()
        
        consulta_id = cursor.lastrowid
        conn.close()
        
        return {"id": consulta_id, "paciente_id": data.get('paciente_id'), "created_at": datetime.now().isoformat()}
    
    def get_gastos(self):
        """Obtiene todos los gastos"""
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM gastos ORDER BY fecha_gasto DESC LIMIT 50')
        gastos = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return {"items": gastos, "total": len(gastos)}
    
    def crear_gasto(self, data):
        """Crea un nuevo gasto"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO gastos (descripcion, monto, categoria)
            VALUES (?, ?, ?)
        ''', (
            data.get('descripcion'),
            data.get('monto'),
            data.get('categoria', 'general')
        ))
        conn.commit()
        
        gasto_id = cursor.lastrowid
        conn.close()
        
        return {"id": gasto_id, "monto": data.get('monto'), "created_at": datetime.now().isoformat()}
    
    def get_ingresos(self):
        """Obtiene todos los ingresos"""
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM ingresos ORDER BY fecha_ingreso DESC LIMIT 50')
        ingresos = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return {"items": ingresos, "total": len(ingresos)}
    
    def crear_ingreso(self, data):
        """Crea un nuevo ingreso"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO ingresos (descripcion, monto, tipo, paciente_id, consulta_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            data.get('descripcion'),
            data.get('monto'),
            data.get('tipo', 'general'),
            data.get('paciente_id'),
            data.get('consulta_id')
        ))
        conn.commit()
        
        ingreso_id = cursor.lastrowid
        conn.close()
        
        return {"id": ingreso_id, "monto": data.get('monto'), "created_at": datetime.now().isoformat()}
    
    def get_estadisticas(self):
        """Calcula estadísticas del sistema"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Total pacientes
        cursor.execute('SELECT COUNT(*) as total FROM pacientes')
        total_pacientes = cursor.fetchone()[0]
        
        # Consultas hoy
        cursor.execute('SELECT COUNT(*) as total FROM consultas WHERE DATE(fecha_consulta) = DATE("now")')
        consultas_hoy = cursor.fetchone()[0]
        
        # Ingresos del mes
        cursor.execute('SELECT SUM(monto) as total FROM ingresos WHERE strftime("%Y-%m", fecha_ingreso) = strftime("%Y-%m", "now")')
        ingresos_mes = cursor.fetchone()[0] or 0
        
        # Gastos del mes
        cursor.execute('SELECT SUM(monto) as total FROM gastos WHERE strftime("%Y-%m", fecha_gasto) = strftime("%Y-%m", "now")')
        gastos_mes = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            "total_pacientes": total_pacientes,
            "consultas_hoy": consultas_hoy,
            "ingresos_mes": round(ingresos_mes, 2),
            "gastos_mes": round(gastos_mes, 2),
            "ganancia_mes": round(ingresos_mes - gastos_mes, 2),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_swagger_ui(self):
        """Retorna HTML con Swagger UI simplificado"""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>🏥 Clínica Pediátrica - API Documentation</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
                .container { max-width: 1200px; margin: 0 auto; }
                header { background: white; padding: 30px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
                h1 { color: #667eea; margin-bottom: 10px; }
                .endpoint { background: white; padding: 20px; margin-bottom: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .method { display: inline-block; padding: 5px 10px; border-radius: 5px; font-weight: bold; color: white; margin-right: 10px; }
                .get { background: #61affe; }
                .post { background: #49cc90; }
                .put { background: #fca130; }
                .delete { background: #f93e3e; }
                .path { font-family: monospace; color: #333; font-weight: bold; }
                .description { color: #666; margin-top: 10px; }
                .try-btn { background: #667eea; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin-top: 10px; }
                .try-btn:hover { background: #764ba2; }
            </style>
        </head>
        <body>
            <div class="container">
                <header>
                    <h1>🏥 Clínica Pediátrica - API Documentation</h1>
                    <p>Versión 1.0.0 - Sistema de Gestión de Consultorios Pediátricos</p>
                </header>
                
                <div class="endpoint">
                    <span class="method get">GET</span>
                    <span class="path">/</span>
                    <p class="description">Estado de la API</p>
                    <a href="/" class="try-btn">Probar</a>
                </div>
                
                <div class="endpoint">
                    <span class="method get">GET</span>
                    <span class="path">/health</span>
                    <p class="description">Health check del servidor</p>
                    <a href="/health" class="try-btn">Probar</a>
                </div>
                
                <div class="endpoint">
                    <span class="method get">GET</span>
                    <span class="path">/api/estadisticas</span>
                    <p class="description">Obtener estadísticas del sistema (total pacientes, consultas hoy, ingresos/gastos del mes)</p>
                    <a href="/api/estadisticas" class="try-btn">Probar</a>
                </div>
                
                <div class="endpoint">
                    <span class="method get">GET</span>
                    <span class="path">/api/pacientes</span>
                    <p class="description">Listar todos los pacientes (paginado)</p>
                    <a href="/api/pacientes" class="try-btn">Probar</a>
                </div>
                
                <div class="endpoint">
                    <span class="method get">GET</span>
                    <span class="path">/api/pacientes/{id}</span>
                    <p class="description">Obtener información de un paciente específico</p>
                </div>
                
                <div class="endpoint">
                    <span class="method post">POST</span>
                    <span class="path">/api/pacientes</span>
                    <p class="description">Crear nuevo paciente</p>
                    <p style="font-size: 12px; color: #999; margin-top: 10px;">Body: { "cedula": "123456", "nombre": "Juan", "apellido": "Pérez", "email": "juan@example.com" }</p>
                </div>
                
                <div class="endpoint">
                    <span class="method put">PUT</span>
                    <span class="path">/api/pacientes/{id}</span>
                    <p class="description">Actualizar paciente</p>
                </div>
                
                <div class="endpoint">
                    <span class="method delete">DELETE</span>
                    <span class="path">/api/pacientes/{id}</span>
                    <p class="description">Eliminar paciente</p>
                </div>
                
                <div class="endpoint">
                    <span class="method get">GET</span>
                    <span class="path">/api/consultas</span>
                    <p class="description">Listar todas las consultas médicas</p>
                    <a href="/api/consultas" class="try-btn">Probar</a>
                </div>
                
                <div class="endpoint">
                    <span class="method post">POST</span>
                    <span class="path">/api/consultas</span>
                    <p class="description">Crear nueva consulta</p>
                </div>
                
                <div class="endpoint">
                    <span class="method get">GET</span>
                    <span class="path">/api/gastos</span>
                    <p class="description">Listar todos los gastos</p>
                    <a href="/api/gastos" class="try-btn">Probar</a>
                </div>
                
                <div class="endpoint">
                    <span class="method post">POST</span>
                    <span class="path">/api/gastos</span>
                    <p class="description">Registrar nuevo gasto</p>
                </div>
                
                <div class="endpoint">
                    <span class="method get">GET</span>
                    <span class="path">/api/ingresos</span>
                    <p class="description">Listar todos los ingresos</p>
                    <a href="/api/ingresos" class="try-btn">Probar</a>
                </div>
                
                <div class="endpoint">
                    <span class="method post">POST</span>
                    <span class="path">/api/ingresos</span>
                    <p class="description">Registrar nuevo ingreso</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def log_message(self, format, *args):
        """Suprime logs innecesarios"""
        pass

def main():
    """Inicia el servidor HTTP"""
    # Inicializar BD
    handler = ClinicaHandler
    handler.init_db(handler)
    
    server_address = ('127.0.0.1', 8000)
    httpd = HTTPServer(server_address, handler)
    
    print("""
╔════════════════════════════════════════════════════════╗
║  🏥 CLÍNICA PEDIÁTRICA - Servidor Completo            ║
╚════════════════════════════════════════════════════════╝

🌐 Servidor corriendo en:

   http://localhost:8000

📡 Endpoints principales:

   GET  /                    → Estado de la API
   GET  /health              → Health check
   GET  /api/estadisticas    → Dashboard de estadísticas
   GET  /api/pacientes       → Listar pacientes
   POST /api/pacientes       → Crear paciente
   GET  /api/consultas       → Listar consultas
   POST /api/consultas       → Crear consulta
   GET  /api/gastos          → Listar gastos
   POST /api/gastos          → Crear gasto
   GET  /api/ingresos        → Listar ingresos
   POST /api/ingresos        → Crear ingreso

📚 Documentación interactiva:

   http://localhost:8000/docs

🧪 Ejemplos en navegador:

   http://localhost:8000/api/estadisticas
   http://localhost:8000/api/pacientes

⏸️  Presiona Ctrl+C para detener el servidor

════════════════════════════════════════════════════════
    """)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n✓ Servidor detenido")

if __name__ == '__main__':
    main()
