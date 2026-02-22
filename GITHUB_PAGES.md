# 🌐 GitHub Pages - Guía de Configuración

Tu proyecto **Clínica Pediátrica** ahora tiene un sitio web profesional listo para GitHub Pages.

---

## ✅ Pasos para Habilitar GitHub Pages

### 1️⃣ **Ir a Settings del Repositorio**

1. Ve a: https://github.com/rosana729/lemes/settings
2. En el menú lateral, busca **"Pages"** (o ve directamente a esta URL):
   ```
   https://github.com/rosana729/lemes/settings/pages
   ```

### 2️⃣ **Configurar la Rama Fuente**

En la sección **"Build and deployment"**:

1. **Source**: Selecciona **"Deploy from a branch"**
2. **Branch**: Selecciona `main` (o `master`)
3. **Folder**: Selecciona `/docs`
4. Click en **"Save"**

![GitHub Pages Settings](../img/github-pages-setup.png)

### 3️⃣ **Esperar a que se Despliegue**

- GitHub generará tu sitio automáticamente
- Toma ~1-2 minutos
- Verás un mensaje: ✅ "Your site is live at..."

### 4️⃣ **Acceder a tu Sitio**

Una vez habilitado, estará disponible en:

```
https://rosana729.github.io/lemes
```

---

## 📝 Estructura de Archivos Creados

```
docs/
├── index.html          ← Página principal
├── style.css           ← Estilos
├── script.js           ← Interactividad
└── _config.yml         ← Configuración Jekyll
```

---

## 🎯 Qué Verán los Visitantes

Tu sitio mostrará:

✅ **Hero Section** - Presentación del proyecto
✅ **Features** - Características principales
✅ **Stack Tecnológico** - Tecnologías usadas
✅ **Inicio Rápido** - Código de instalación
✅ **Endpoints** - API disponible
✅ **Call-to-Action** - Links a GitHub y README

---

## 🔧 Personalización

### Cambiar Titulo/Descripción

Edita `docs/index.html` línea 6:

```html
<title>🏥 Clínica Pediátrica - FastAPI + Supabase</title>
```

### Cambiar Colores

Edita `docs/style.css`:

```css
:root {
    --primary-color: #00d4ff;      /* Ej: #ff6b6b para rojo */
    --secondary-color: #0099cc;
    --dark-bg: #0a0e27;
    /* ... más colores */
}
```

### Agregar Secciones

Agrega en `docs/index.html` dentro del `<body>`:

```html
<section id="mi-seccion" class="nueva-seccion">
    <div class="container">
        <h2>Mi Nueva Sección</h2>
        <p>Contenido aquí</p>
    </div>
</section>
```

Y en `docs/style.css` agrega estilos:

```css
.nueva-seccion {
    padding: 80px 20px;
    background-color: var(--dark-bg);
}
```

---

## 🎬 Agregar GIF Demostrativo

Una vez tengas tu `demo.gif` (ver [GIF_DEMO.md](../GIF_DEMO.md)):

1. Coloca el GIF en `docs/demo.gif`
2. Edita `docs/index.html` después del hero:

```html
<section class="demo">
    <div class="container">
        <h2>🎬 Demo en Vivo</h2>
        <img src="demo.gif" alt="Demo API" style="max-width: 100%; border-radius: 10px;">
    </div>
</section>
```

3. Agrega estilos en `docs/style.css`:

```css
.demo {
    padding: 80px 20px;
    background-color: var(--card-bg);
    text-align: center;
}

.demo img {
    max-width: 800px;
    margin-top: 40px;
    border-radius: 10px;
    box-shadow: 0 10px 30px rgba(0, 212, 255, 0.2);
}
```

---

## 📊 Analytics

Para ver estadísticas de visitantes:

1. Ve a Settings > Pages
2. En "GitHub Pages" busca "Visitors analytics"
3. GitHub mostrará gráficos de tráfico

---

## ✨ Caractéristicas Incluidas

- ✅ **Diseño Responsivo** - Se adapta a móvil/tablet/desktop
- ✅ **Tema Oscuro** - Estilo moderno y profesional
- ✅ **Animaciones** - Transiciones suaves
- ✅ **SEO Básico** - Metadatos optimizados
- ✅ **Rápido** - HTML/CSS/JS estático
- ✅ **Sin Dependencias** - Solo HTML/CSS/JS

---

## 🔗 Links Útiles

| Página | URL |
|--------|-----|
| **Tu Sitio** | https://rosana729.github.io/lemes |
| **GitHub Repo** | https://github.com/rosana729/lemes |
| **API Docs** | http://localhost:8000/docs |
| **Swagger UI** | http://localhost:8000/redoc |

---

## 🚀 Próximos Pasos

1. ✅ Habilitar GitHub Pages (ver arriba)
2. ✅ Crear GIF demostrativo ([GIF_DEMO.md](../GIF_DEMO.md))
3. ✅ Configurar Supabase
4. ✅ Hacer push de cambios

```bash
git add docs/
git commit -m "Add GitHub Pages site"
git push origin main
```

---

## 📞 Solución de Problemas

### El sitio no aparece

- Espera 5 minutos (GitHub toma tiempo)
- Verifica que la rama sea `main` o `master`
- Verifica que la carpeta sea `/docs`
- Recarga la página en Settings > Pages

### Los estilos no cargan

- Limpia el cache del navegador: `Ctrl+Shift+Delete`
- Verifica que `style.css` está en la carpeta `docs/`
- Recarga: `Ctrl+F5`

### Los links no funcionan

- Verifica las URLs en `index.html`
- Asegúrate que los archivos existen
- Los links internos deben ser relativos: `style.css` no `/docs/style.css`

---

## 📱 Compartir

Una vez habilitado, comparte tu sitio:

- **Twitter**: "Echa un vistazo a mi sistema de clínica pediátrica: https://rosana729.github.io/lemes"
- **LinkedIn**: Comparte como logro profesional
- **GitHub**: Actualiza el README con el link

```markdown
🌐 **Sitio Web**: [Ver Demostración](https://rosana729.github.io/lemes)
```

---

## ¡Listo! 🎉

Tu proyecto ahora es visible globalmente en GitHub Pages. 

**Próximo paso**: Crea el GIF demostrativo ([GIF_DEMO.md](../GIF_DEMO.md))
