"""
API Simple - Clínica Pediátrica
Versión Mini sin dependencias complejas
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime

# Base de datos simple en memoria
pacientes = {}
consultas = {}
gastos = {}
ingresos = {}

class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        
        # Health check
        if path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode())
        
        # Root
        elif path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "status": "healthy",
                "service": "Clínica Pediátrica API",
                "version": "1.0.0",
                "message": "¡Sistema funcionando!"
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
        
        # Estadísticas
        elif path == '/api/estadisticas':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "total_pacientes": len(pacientes),
                "consultas_hoy": len(consultas),
                "ingresos_mes": 1500.00,
                "gastos_mes": 800.00,
                "ganancia_mes": 700.00
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
        
        # Pacientes
        elif path == '/api/pacientes':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(list(pacientes.values()), indent=2).encode())
        
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "No encontrado"}).encode())
    
    def do_POST(self):
        path = self.path
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        try:
            data = json.loads(body.decode())
        except:
            data = {}
        
        # Crear paciente
        if path == '/api/pacientes':
            nuevo_id = len(pacientes) + 1
            pacientes[nuevo_id] = {
                "id": nuevo_id,
                "cedula": data.get("cedula"),
                "nombre": data.get("nombre"),
                "apellido": data.get("apellido"),
                "email": data.get("email"),
                "nombre_completo": f"{data.get('nombre', '')} {data.get('apellido', '')}",
                "created_at": datetime.now().isoformat()
            }
            
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(pacientes[nuevo_id], indent=2).encode())
        
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "No encontrado"}).encode())
    
    def log_message(self, format, *args):
        # Silenciar logs
        pass


if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', 8000), APIHandler)
    print("""
╔════════════════════════════════════════════════════════╗
║   🏥 CLÍNICA PEDIÁTRICA API - Funcionando             ║
╚════════════════════════════════════════════════════════╝

🌐 Servidor corriendo en:

   http://localhost:8000

📡 Endpoints disponibles:

   GET  /               → Estado de la API
   GET  /health         → Health check
   GET  /api/estadisticas  → Estadísticas
   GET  /api/pacientes  → Listar pacientes
   POST /api/pacientes  → Crear paciente

🧪 Prueba en navegador:

   http://localhost:8000/health
   http://localhost:8000/api/estadisticas

⏸️  Presiona Ctrl+C para detener

════════════════════════════════════════════════════════
    """)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n✓ Servidor detenido")
        server.server_close()
