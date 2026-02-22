# 🎬 Guía: Crear GIF Demostrativo para GitHub

Una imagen GIF animada en tu README hace que el proyecto sea mucho más atractivo en GitHub.

---

## 📌 Razón por la que necesitas un GIF

✅ **Más visibilidad**: Los repositorios con GIF reciben más stars
✅ **Mejor demostración**: Los usuarios ven cómo funciona sin ejecutarlo
✅ **Profesionalidad**: Demuestra que es un proyecto serio
✅ **Engagement**: Aumenta las posibilidades de que lo usen

---

## Opción 1: ScreenToGif (Windows) ⭐ **MÁS FÁCIL**

### Paso 1: Descargar ScreenToGif

1. Ve a https://www.screentogif.com/#download
2. Descarga la versión **Portable** (no necesita instalación)
3. Descomprime y ejecuta `ScreenToGif.exe`

### Paso 2: Preparar la demostración

Antes de grabar, asegúrate de:

```bash
# 1. Ten tu servidor ejecutándose
python main.py

# 2. Abre en navegador la documentación
http://localhost:8000/docs
```

### Paso 3: Grabar el GIF

1. **Abre ScreenToGif**
2. Click en **"Record"** (esquina superior izquierda)
3. Selecciona un área para grabar (ejemplo: 1280x720 píxeles)
4. **Comienza a grabar** y demuestra:

   ```
   ⏱️ GUIÓN (máximo 15 segundos):
   
   1. [0-2s] Mostrar la página principal del API
   2. [2-5s] Hacer click en "Pacientes" → Probar GET /pacientes
   3. [5-8s] Expandir POST /pacientes y mostrar el esquema
   4. [8-11s] Ir a "Estadísticas" - GET /api/estadisticas
   5. [11-15s] Probar un endpoint real y mostrar respuesta
   ```

5. **Termina la grabación** cuando hayas demostrado todo
6. Click en **"Stop"** (botón rojo)

### Paso 4: Exportar el GIF

1. En la barra derecha, busca **"Export"**
2. Selecciona **"Gif"** → Click en la carpeta de destino
3. Ajusta configuración:
   - **Width**: 1280
   - **Height**: 720
   - **Loop**: Infinito (por defecto)
   - **FPS**: 10 (comprime el archivo)
4. Click en **"Capture!"**
5. Guarda como `demo.gif` en la carpeta `docs/`

### Paso 5: Optimizar el tamaño

Si el GIF es muy grande (>10MB), comprimelo:

```bash
# Instala ImageMagick si no lo tienes
# En Windows: https://imagemagick.org/script/download.php#windows

# Comprime el GIF
magick convert demo.gif -coalesce -colors 256 -fuzz 10% demo-compressed.gif
```

---

## Opción 2: LiceCAP (Muy Ligero) ⚡

### Ventajas

- 📦 **Muy pequeño** (~600 KB)
- 🎯 **Directo a GIF** (sin conversiones)
- ⚡ **Súper rápido**

### Pasos

1. Descarga: https://www.cockos.com/licecap/
2. Descomprime y ejecuta `LiceCAP.exe`
3. Dibuja el área que quieres grabar
4. Click en "Record"
5. Demuestra tu API
6. Click en "Stop"
7. Guarda como `demo.gif`

---

## Opción 3: FFmpeg (Multiplataforma) 🛠️

Para usuarios avanzados que quieren máximo control.

### Instalación

```bash
# Windows (con Chocolatey)
choco install ffmpeg

# O descarga manualmente:
# https://ffmpeg.org/download.html
```

### Grabar video (30 segundos max)

```bash
# Grabar solo una parte de la pantalla
ffmpeg -f gdigrab -framerate 30 -offset_x 100 -offset_y 100 ^
  -video_size 1280x720 -i desktop -t 15 demo.mp4
```

### Convertir a GIF optimizado

```bash
# Paleta + GIF optimizado
ffmpeg -i demo.mp4 -vf "fps=10,scale=1280:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" ^
  -loop 0 demo.gif
```

### Ver resultado

```bash
# Abre el GIF resultante
demo.gif
```

---

## 📝 Agregar el GIF al README

Una vez tengas tu `demo.gif`, agrégalo al README:

```markdown
## 🎬 Demo en Vivo

![API Demo](docs/demo.gif)

**↑ En el GIF anterior puedes ver:**
- Swagger UI en acción
- Endpoints interactivos
- Respuestas en tiempo real
- Validación automática
```

---

## 📊 Dónde poner el archivo

```
tu-proyecto/
├── README.md
├── docs/
│   ├── demo.gif          ← 👈 AQUÍ
│   └── screenshots/
└── ...
```

**Comando para crear la carpeta:**
```bash
mkdir docs
```

---

## ✅ Checklist Final

- [ ] GIF creado (máximo 15 segundos)
- [ ] GIF guardado en `docs/demo.gif`
- [ ] GIF muestra los puntos clave del API
- [ ] Tamaño del GIF es razonable (< 10MB)
- [ ] Agregado al README.md con ![alt](docs/demo.gif)
- [ ] Probado que el link funciona en GitHub

---

## 🎯 Qué Mostrar en el GIF (Recomendación)

### Mejor demostración (15 segundos):

```
1. Mostrar Swagger UI (/docs)
2. Expandir endpoint de Pacientes (GET /api/pacientes)
3. Probar un endpoint real (ej: GET /api/estadisticas)
4. Mostrar respuesta JSON formateada
5. Demostrar Swagger ejecutando un endpoint exitosamente
```

### Esto demuestra:

✅ API funcional
✅ Documentación auto-generada
✅ Endpoints probados
✅ Respuestas válidas
✅ Interfaz amigable

---

## 💡 Tips Profesionales

### 1. Luz y contraste
- Usa tema oscuro del navegador (más profesional)
- Asegúrate que el GIF sea legible

### 2. Velocidad
- 10 FPS es ideal (comprime el archivo)
- Menos rápido que video normal es aceptable

### 3. Tamaño
- Si el GIF > 5MB, comprimelo
- Los usuarios de mobile te lo agradecerán

### 4. Duración
- 10-15 segundos: Ideal
- Menos de 10 segundos: Muy rápido
- Más de 20 segundos: Demasiado largo

---

## 📱 Versión Móvil del GIF

Si quieres un GIF para demostración móvil:

```bash
# Crea versión más pequeña
ffmpeg -i demo.gif -vf "scale=480:-1" demo-mobile.gif
```

Y agrega al README:

```markdown
### 📱 En Dispositivos Móviles

![Mobile Demo](docs/demo-mobile.gif)
```

---

## 🚀 Próximo Paso

Una vez tengas el GIF listo:

1. Pushea los cambios a GitHub:

```bash
git add docs/demo.gif README.md
git commit -m "Add demo GIF to showcase API"
git push origin main
```

2. ¡Listo! Tu proyecto ahora es más visible en GitHub 🎉

---

## 📞 Ayuda

Si tiene problemas:

- Las herramientas son **gratuitas**
- ScreenToGif es la más fácil
- Cualquier herramienta que cree GIF funciona

¡Adelante! 🚀
