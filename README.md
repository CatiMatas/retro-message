Retro Terminal Video Generator

Generador de vídeos estilo terminal IBM/CRT con texto animado, efecto máquina de escribir y sonido sincronizado.

Este proyecto crea automáticamente un archivo MP4 a partir de una lista de líneas de texto definida en Python. Está pensado para producir mensajes audiovisuales con estética de ordenador antiguo: fondo negro, texto verde fósforo, cursor, líneas CRT y sonidos de teclado.

Qué hace el proyecto

El script:

muestra el texto carácter a carácter;
simula una terminal retro con fondo negro y texto verde;
añade un cursor parpadeante;
incorpora líneas y ruido visual tipo CRT;
genera sonidos de tecla y de final de línea;
sincroniza el audio con la escritura;
crea un vídeo MP4 final utilizando FFmpeg.

Por qué puede ser útil

Puede utilizarse para crear:

introducciones para juegos y actividades;
mensajes de misión;
vídeos para escape rooms o gymkhanas;
presentaciones con estética retro;
mensajes narrativos para plataformas como Loquiz;
prototipos sencillos de animación generada con Python.

Requisitos

El proyecto ha sido probado con:

Python 3.14
OpenCV
NumPy
Pillow
FFmpeg

Librerías de Python

Instala las dependencias con:

python3 -m pip install opencv-python numpy pillow

FFmpeg

En macOS con Homebrew:

brew install ffmpeg

Comprueba la instalación:

ffmpeg -version

Uso

Abre mensaje_retro.py.
Modifica el contenido de la lista texto_lineas.

Ejemplo:

texto_lineas = [
    "Una importante operación financiera internacional",
    "relacionada con la compra de una obra de arte",
    "ha quedado bloqueada.",
    "",
    "El comprador asegura haber realizado correctamente el pago.",
    "El vendedor afirma que nunca recibió el dinero.",
    "",
    "VUESTRA MISIÓN:",
    "Seguid el rastro del dinero y descubrid qué ha pasado.",
    "",
    "Buena suerte."
]

Cada elemento de la lista representa una línea.

Para introducir un espacio entre bloques utiliza:

""

Guarda el archivo.
Ejecuta desde la terminal, dentro de la carpeta del proyecto:

python3 mensaje_retro.py

Archivos generados

El script genera automáticamente:

mensaje_retro_sin_audio.mp4
mensaje_retro_audio.wav
mensaje_retro_final.mp4

El archivo principal es:

mensaje_retro_final.mp4

Este archivo contiene la animación y el sonido sincronizado.

Personalización

Algunos parámetros que pueden modificarse en el script:

ANCHO = 1280
ALTO = 720
FPS = 30
FRAMES_POR_LETRA = 3
PAUSA_ENTRE_LINEAS = 0.5
PAUSA_FINAL = 5

También pueden modificarse:

tamaño de la fuente;
posición del texto;
espaciado entre líneas;
intensidad del verde;
volumen de las teclas;
duración de los sonidos;
velocidad de escritura;
encabezados de la terminal.

Estructura recomendada

retro-terminal-video/
├── mensaje_retro.py
├── README.md
└── output/

Los archivos MP4 y WAV generados pueden mantenerse fuera del repositorio si no son necesarios para el código fuente.

Flujo de trabajo

Editar texto
    ↓
Guardar mensaje_retro.py
    ↓
python3 mensaje_retro.py
    ↓
Generación de vídeo
    ↓
Generación de audio
    ↓
FFmpeg combina ambos
    ↓
mensaje_retro_final.mp4

Notas sobre plataformas de juego

Si una plataforma no admite la carga directa de MP4 pero acepta vídeos de YouTube o Vimeo, el archivo final puede subirse como vídeo no listado y utilizarse mediante su enlace.

Ayuda

Si el script no encuentra FFmpeg, comprueba:

ffmpeg -version

Si aparece un error relacionado con una librería de Python, comprueba que esté instalada con:

python3 -m pip list

Mantenimiento

Proyecto mantenido por Cati Matas.

Licencia

El código de este proyecto se distribuye bajo la MIT License.

Esto permite usar, copiar, modificar y distribuir el software, incluso para fines comerciales, siempre que se conserve el aviso de copyright y la licencia correspondiente.

Consulta el archivo LICENSE para ver los términos completos.

> La licencia MIT de este repositorio se aplica al código fuente del proyecto. Los textos narrativos, vídeos finales, materiales de juegos, contenidos de clientes y otros recursos externos no se consideran incluidos salvo que se indique expresamente.
