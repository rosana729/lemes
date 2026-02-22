// ════════════════════════════════════════════
// API CLIENT - Gestiona todas las llamadas a la API
// ════════════════════════════════════════════

const API_BASE = 'http://127.0.0.1:8000/api';

class ClinicaAPI {
    constructor() {
        this.token = localStorage.getItem('token');
        this.usuario = JSON.parse(localStorage.getItem('usuario') || '{}');
    }

    // ════════════════════════════════════════════
    // AUTENTICACIÓN
    // ════════════════════════════════════════════

    async login(email, contraseña) {
        try {
            const response = await fetch(`${API_BASE}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, contraseña })
            });

            if (!response.ok) {
                throw new Error('Credenciales inválidas');
            }

            const data = await response.json();
            this.token = data.access_token;
            this.usuario = data.usuario;

            localStorage.setItem('token', this.token);
            localStorage.setItem('usuario', JSON.stringify(this.usuario));

            return { success: true, usuario: this.usuario };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    logout() {
        this.token = null;
        this.usuario = {};
        localStorage.removeItem('token');
        localStorage.removeItem('usuario');
    }

    // ════════════════════════════════════════════
    // PACIENTES
    // ════════════════════════════════════════════

    async obtenerPacientes() {
        return this._get('/pacientes');
    }

    async obtenerPaciente(id) {
        return this._get(`/pacientes/${id}`);
    }

    async crearPaciente(datos) {
        return this._post('/pacientes', datos);
    }

    async actualizarPaciente(id, datos) {
        return this._put(`/pacientes/${id}`, datos);
    }

    async eliminarPaciente(id) {
        return this._delete(`/pacientes/${id}`);
    }

    // ════════════════════════════════════════════
    // HISTORIAS CLÍNICAS
    // ════════════════════════════════════════════

    async crearHistoria(datos) {
        return this._post('/historias-clinicas', datos);
    }

    async obtenerHistoriasPaciente(pacienteId) {
        return this._get(`/historias-clinicas/paciente/${pacienteId}`);
    }

    async obtenerHistoria(id) {
        return this._get(`/historias-clinicas/${id}`);
    }

    async actualizarHistoria(id, datos) {
        return this._put(`/historias-clinicas/${id}`, datos);
    }

    // ════════════════════════════════════════════
    // CITAS
    // ════════════════════════════════════════════

    async crearCita(datos) {
        return this._post('/citas', datos);
    }

    async obtenerCitasDoctor(doctorId) {
        return this._get(`/citas/doctor/${doctorId}`);
    }

    async obtenerCitasPaciente(pacienteId) {
        return this._get(`/citas/paciente/${pacienteId}`);
    }

    async actualizarCita(id, datos) {
        return this._put(`/citas/${id}`, datos);
    }

    async eliminarCita(id) {
        return this._delete(`/citas/${id}`);
    }

    // ════════════════════════════════════════════
    // ESTADÍSTICAS
    // ════════════════════════════════════════════

    async obtenerEstadisticas() {
        return this._get('/estadisticas');
    }

    async obtenerUsuarios() {
        return this._get('/usuarios');
    }

    // ════════════════════════════════════════════
    // MÉTODOS PRIVADOS
    // ════════════════════════════════════════════

    async _get(endpoint) {
        try {
            const headers = { 'Content-Type': 'application/json' };
            if (this.token) headers['Authorization'] = `Bearer ${this.token}`;

            const response = await fetch(`${API_BASE}${endpoint}`, { headers });
            if (response.status === 401) {
                this.logout();
                window.location.href = '/';
                return { error: 'Sesión expirada' };
            }
            return await response.json();
        } catch (error) {
            return { error: error.message };
        }
    }

    async _post(endpoint, datos) {
        try {
            const headers = { 'Content-Type': 'application/json' };
            if (this.token) headers['Authorization'] = `Bearer ${this.token}`;

            const response = await fetch(`${API_BASE}${endpoint}`, {
                method: 'POST',
                headers,
                body: JSON.stringify(datos)
            });

            if (response.status === 401) {
                this.logout();
                window.location.href = '/';
                return { error: 'Sesión expirada' };
            }

            return await response.json();
        } catch (error) {
            return { error: error.message };
        }
    }

    async _put(endpoint, datos) {
        try {
            const headers = { 'Content-Type': 'application/json' };
            if (this.token) headers['Authorization'] = `Bearer ${this.token}`;

            const response = await fetch(`${API_BASE}${endpoint}`, {
                method: 'PUT',
                headers,
                body: JSON.stringify(datos)
            });

            return await response.json();
        } catch (error) {
            return { error: error.message };
        }
    }

    async _delete(endpoint) {
        try {
            const headers = { 'Content-Type': 'application/json' };
            if (this.token) headers['Authorization'] = `Bearer ${this.token}`;

            const response = await fetch(`${API_BASE}${endpoint}`, {
                method: 'DELETE',
                headers
            });

            return await response.json();
        } catch (error) {
            return { error: error.message };
        }
    }
}

// Instancia global
const api = new ClinicaAPI();
