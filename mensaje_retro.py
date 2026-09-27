import os
import random
import subprocess
import wave

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


# ============================================================
# TEXTO
# ============================================================
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


# ============================================================
# CONFIGURACION VIDEO
# ============================================================

ANCHO = 1280
ALTO = 720
FPS = 30

ARCHIVO_VIDEO_SIN_AUDIO = "mensaje_retro_sin_audio.mp4"
ARCHIVO_AUDIO = "mensaje_retro_audio.wav"
ARCHIVO_FINAL = "mensaje_retro_final.mp4"

FRAMES_POR_LETRA = 3

PAUSA_ENTRE_LINEAS = 0.5
PAUSA_LINEA_VACIA = 0.4
PAUSA_FINAL = 5


# ============================================================
# CONFIGURACION VISUAL
# ============================================================

NEGRO = (0, 0, 0)
VERDE = (0, 255, 80)
VERDE_OSCURO = (0, 80, 30)

RUTA_FUENTE = "/System/Library/Fonts/Menlo.ttc"
TAMANO_FUENTE = 26

X_INICIAL = 90
Y_INICIAL = 150
ESPACIADO_LINEAS = 48


# ============================================================
# CONFIGURACION AUDIO
# ============================================================

SAMPLE_RATE = 44100

# Volumen general aproximado
VOLUMEN_TECLA = 0.35
VOLUMEN_RETORNO = 0.45

# Duraciones
DURACION_TECLA = 0.035
DURACION_RETORNO = 0.12


# ============================================================
# FUENTE
# ============================================================

if os.path.exists(RUTA_FUENTE):
    fuente = ImageFont.truetype(
        RUTA_FUENTE,
        TAMANO_FUENTE
    )
else:
    fuente = ImageFont.load_default()


# ============================================================
# FUNCIONES AUDIO
# ============================================================

def generar_sonido_tecla():
    """
    Genera un clic corto tipo teclado/terminal.
    Devuelve un array numpy de audio mono.
    """

    muestras = int(SAMPLE_RATE * DURACION_TECLA)

    # Ruido
    ruido = np.random.normal(
        0,
        1,
        muestras
    )

    # Tono aleatorio
    frecuencia = random.randint(650, 900)

    t = np.linspace(
        0,
        DURACION_TECLA,
        muestras,
        endpoint=False
    )

    tono = np.sin(
        2 * np.pi * frecuencia * t
    )

    # Mezcla
    audio = (
        ruido * 0.55
        + tono * 0.45
    )

    # Fade out
    envolvente = np.linspace(
        1,
        0,
        muestras
    )

    audio *= envolvente
    audio *= VOLUMEN_TECLA

    return audio


def generar_sonido_retorno():
    """
    Genera un sonido de final de linea.
    """

    muestras = int(
        SAMPLE_RATE * DURACION_RETORNO
    )

    t = np.linspace(
        0,
        DURACION_RETORNO,
        muestras,
        endpoint=False
    )

    ruido = np.random.normal(
        0,
        1,
        muestras
    )

    tono = np.sin(
        2 * np.pi * 380 * t
    )

    audio = (
        ruido * 0.65
        + tono * 0.35
    )

    envolvente = np.linspace(
        1,
        0,
        muestras
    )

    audio *= envolvente
    audio *= VOLUMEN_RETORNO

    return audio


def crear_silencio(segundos):
    """
    Genera silencio.
    """

    muestras = int(
        SAMPLE_RATE * segundos
    )

    return np.zeros(
        muestras,
        dtype=np.float32
    )


def guardar_wav(audio, nombre_archivo):
    """
    Guarda el array numpy en WAV mono 16-bit.
    """

    # Evitar saturacion
    audio = np.clip(
        audio,
        -1.0,
        1.0
    )

    # Convertir a 16 bits
    audio_16bit = (
        audio * 32767
    ).astype(np.int16)

    with wave.open(
        nombre_archivo,
        "w"
    ) as archivo_wav:

        archivo_wav.setnchannels(1)
        archivo_wav.setsampwidth(2)
        archivo_wav.setframerate(
            SAMPLE_RATE
        )

        archivo_wav.writeframes(
            audio_16bit.tobytes()
        )


# ============================================================
# FUNCION PARA CREAR FRAME
# ============================================================

def crear_frame(
    lineas,
    mostrar_cursor=False
):

    imagen = Image.new(
        "RGB",
        (ANCHO, ALTO),
        NEGRO
    )

    draw = ImageDraw.Draw(imagen)

    # --------------------------------------------------------
    # CABECERA
    # --------------------------------------------------------

    draw.text(
        (X_INICIAL, 65),
        "IBM FINANCIAL NETWORK",
        font=fuente,
        fill=VERDE
    )

    draw.text(
        (X_INICIAL, 100),
        "SECURE TERMINAL // CASE FILE",
        font=fuente,
        fill=VERDE_OSCURO
    )

    # --------------------------------------------------------
    # TEXTO PRINCIPAL
    # --------------------------------------------------------

    y = Y_INICIAL

    ultima_linea_con_texto = -1

    for i, linea in enumerate(lineas):

        if linea:
            ultima_linea_con_texto = i

        draw.text(
            (X_INICIAL, y),
            linea,
            font=fuente,
            fill=VERDE
        )

        y += ESPACIADO_LINEAS

    # --------------------------------------------------------
    # CURSOR
    # --------------------------------------------------------

    if (
        mostrar_cursor
        and ultima_linea_con_texto >= 0
    ):

        texto_cursor = lineas[
            ultima_linea_con_texto
        ]

        bbox = draw.textbbox(
            (0, 0),
            texto_cursor,
            font=fuente
        )

        ancho_texto = (
            bbox[2] - bbox[0]
        )

        cursor_x = (
            X_INICIAL
            + ancho_texto
            + 8
        )

        cursor_y = (
            Y_INICIAL
            + ultima_linea_con_texto
            * ESPACIADO_LINEAS
        )

        draw.rectangle(
            [
                cursor_x,
                cursor_y + 3,
                cursor_x + 12,
                cursor_y + TAMANO_FUENTE
            ],
            fill=VERDE
        )

    # --------------------------------------------------------
    # PIL -> OPENCV
    # --------------------------------------------------------

    frame = np.array(imagen)

    frame = cv2.cvtColor(
        frame,
        cv2.COLOR_RGB2BGR
    )

    # --------------------------------------------------------
    # EFECTO CRT
    # --------------------------------------------------------

    for y in range(
        0,
        ALTO,
        4
    ):

        cv2.line(
            frame,
            (0, y),
            (ANCHO, y),
            (0, 15, 0),
            1
        )

    # --------------------------------------------------------
    # RUIDO DE PANTALLA
    # --------------------------------------------------------

    ruido = np.random.normal(
        0,
        3,
        frame.shape
    ).astype(np.int16)

    frame = np.clip(
        frame.astype(np.int16)
        + ruido,
        0,
        255
    ).astype(np.uint8)

    return frame


# ============================================================
# CREAR VIDEO
# ============================================================

fourcc = cv2.VideoWriter_fourcc(
    *"mp4v"
)

video = cv2.VideoWriter(
    ARCHIVO_VIDEO_SIN_AUDIO,
    fourcc,
    FPS,
    (ANCHO, ALTO)
)

if not video.isOpened():
    raise RuntimeError(
        "No se ha podido crear el archivo de video."
    )


# ============================================================
# PREPARAR TEXTO Y AUDIO
# ============================================================

lineas_actuales = [
    ""
] * len(texto_lineas)

fragmentos_audio = []

segundos_por_letra = (
    FRAMES_POR_LETRA / FPS
)


# ============================================================
# GENERAR ANIMACION
# ============================================================

for indice, linea_completa in enumerate(
    texto_lineas
):

    # --------------------------------------------------------
    # LINEA VACIA
    # --------------------------------------------------------

    if linea_completa == "":

        frames_pausa = int(
            FPS
            * PAUSA_LINEA_VACIA
        )

        for frame_num in range(
            frames_pausa
        ):

            mostrar_cursor = (
                frame_num // 10
            ) % 2 == 0

            frame = crear_frame(
                lineas_actuales,
                mostrar_cursor
            )

            video.write(frame)

        fragmentos_audio.append(
            crear_silencio(
                PAUSA_LINEA_VACIA
            )
        )

        continue

    # --------------------------------------------------------
    # ESCRIBIR CARACTER A CARACTER
    # --------------------------------------------------------

    for caracter in linea_completa:

        lineas_actuales[indice] += (
            caracter
        )

        for frame_num in range(
            FRAMES_POR_LETRA
        ):

            mostrar_cursor = (
                frame_num % 2 == 0
            )

            frame = crear_frame(
                lineas_actuales,
                mostrar_cursor
            )

            video.write(frame)

        # -----------------------------------------------
        # AUDIO DE CADA LETRA
        # -----------------------------------------------

        if caracter == " ":

            fragmentos_audio.append(
                crear_silencio(
                    segundos_por_letra
                )
            )

        else:

            sonido = (
                generar_sonido_tecla()
            )

            duracion_sonido = (
                len(sonido)
                / SAMPLE_RATE
            )

            fragmentos_audio.append(
                sonido
            )

            silencio_restante = (
                segundos_por_letra
                - duracion_sonido
            )

            if silencio_restante > 0:

                fragmentos_audio.append(
                    crear_silencio(
                        silencio_restante
                    )
                )

    # --------------------------------------------------------
    # PAUSA FINAL DE LINEA
    # --------------------------------------------------------

    frames_pausa = int(
        FPS * PAUSA_ENTRE_LINEAS
    )

    for frame_num in range(
        frames_pausa
    ):

        mostrar_cursor = (
            frame_num // 8
        ) % 2 == 0

        frame = crear_frame(
            lineas_actuales,
            mostrar_cursor
        )

        video.write(frame)

    retorno = (
        generar_sonido_retorno()
    )

    fragmentos_audio.append(
        retorno
    )

    duracion_retorno = (
        len(retorno)
        / SAMPLE_RATE
    )

    silencio_restante = (
        PAUSA_ENTRE_LINEAS
        - duracion_retorno
    )

    if silencio_restante > 0:

        fragmentos_audio.append(
            crear_silencio(
                silencio_restante
            )
        )


# ============================================================
# PAUSA FINAL
# ============================================================

frames_finales = int(
    FPS * PAUSA_FINAL
)

for frame_num in range(
    frames_finales
):

    mostrar_cursor = (
        frame_num // 15
    ) % 2 == 0

    frame = crear_frame(
        lineas_actuales,
        mostrar_cursor
    )

    video.write(frame)

fragmentos_audio.append(
    crear_silencio(
        PAUSA_FINAL
    )
)


# ============================================================
# CERRAR VIDEO
# ============================================================

video.release()


# ============================================================
# CREAR AUDIO FINAL
# ============================================================

audio_final = np.concatenate(
    fragmentos_audio
)

guardar_wav(
    audio_final,
    ARCHIVO_AUDIO
)


# ============================================================
# UNIR VIDEO + AUDIO CON FFMPEG
# ============================================================

comando_ffmpeg = [
    "ffmpeg",
    "-y",

    "-i",
    ARCHIVO_VIDEO_SIN_AUDIO,

    "-i",
    ARCHIVO_AUDIO,

    "-c:v",
    "libx264",

    "-pix_fmt",
    "yuv420p",

    "-c:a",
    "aac",

    "-b:a",
    "192k",

    "-shortest",

    ARCHIVO_FINAL
]


resultado = subprocess.run(
    comando_ffmpeg,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)


# ============================================================
# RESULTADO
# ============================================================

print("")
print(
    "------------------------------------------"
)
print(
    "PROCESO TERMINADO"
)
print(
    "------------------------------------------"
)

if resultado.returncode == 0:

    print(
        f"Video final: {ARCHIVO_FINAL}"
    )

    print(
        "El video incluye sonido sincronizado."
    )

    print("")
    print(
        "Tambien se han creado:"
    )

    print(
        f"- {ARCHIVO_VIDEO_SIN_AUDIO}"
    )

    print(
        f"- {ARCHIVO_AUDIO}"
    )

else:

    print(
        "FFmpeg encontro un problema al unir video y audio."
    )

    print(
        "Comprueba FFmpeg con: ffmpeg -version"
    )

print("")