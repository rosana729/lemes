// ════════════════════════════════════════════════════════════════════════════
// 🔐 SUPABASE CONFIGURATION
// ════════════════════════════════════════════════════════════════════════════
// EDITA ESTOS VALORES CON TUS CREDENCIALES DE SUPABASE

const SUPABASE_CONFIG = {
    // 👇 REEMPLAZA CON TUS VALORES DE SUPABASE
    URL: 'https://ikqwnmcowwakkxjwevbr.supabase.co',      // Ve a: Supabase > Settings > API > Project URL
    KEY: 'ikqwnmcowwakkxjwevbr',                          // Ve a: Supabase > Settings > API > anon public key
    
    // Estos son opcionales, para usuarios sin Supabase aún
    DEMO_MODE: false,                               // Si es true, permite login de demostración
};

// ════════════════════════════════════════════════════════════════════════════
// VALIDAR CONFIGURACIÓN
// ════════════════════════════════════════════════════════════════════════════

function validateSupabaseConfig() {
    const isConfigured = 
        SUPABASE_CONFIG.URL !== 'https://your-project.supabase.co' &&
        SUPABASE_CONFIG.KEY !== 'your-anon-key';
    
    if (!isConfigured && !SUPABASE_CONFIG.DEMO_MODE) {
        console.warn('⚠️  ADVERTENCIA: Supabase no está configurado');
        console.warn('Para habilitar login real, actualiza config.js con:');
        console.warn('1. URL de Supabase');
        console.warn('2. Clave anon de Supabase');
        return false;
    }
    
    return true;
}

// Validar al cargar página
window.addEventListener('load', () => {
    const isValid = validateSupabaseConfig();
    if (!isValid) {
        console.warn('📝 Estás en DEMO MODE. El login usa credenciales de prueba locales.');
    } else {
        console.log('✅ Supabase está configurado correctamente');
    }
});
