# Importamos las bibliotecas necesarias
import streamlit as st
import os
import time as tm
import random
import base64
import json
from PIL import Image
from streamlit_autorefresh import st_autorefresh

# Configuramos la página de Streamlit con un título, un icono y un diseño amplio
st.set_page_config(page_title = "PixMatch", page_icon="🕹️", layout = "wide", initial_sidebar_state = "expanded")

# Obtenemos la letra del disco en el que se está ejecutando el script
vDrive = os.path.splitdrive(os.getcwd())[0]
# Establecemos la ruta del proyecto
vpth = "./"

# Definimos el estilo de los emojis en el juego
sbe = """<span style='font-size: 140px;
                      border-radius: 7px;
                      text-align: center;
                      display:inline;
                      padding-top: 3px;
                      padding-bottom: 3px;
                      padding-left: 0.4em;
                      padding-right: 0.4em;
                      '>
                      |fill_variable|
                      </span>"""

# Definimos el estilo de los emojis cuando se presionan
pressed_emoji = """<span style='font-size: 24px;
                                border-radius: 7px;
                                text-align: center;
                                display:inline;
                                padding-top: 3px;
                                padding-bottom: 3px;
                                padding-left: 0.2em;
                                padding-right: 0.2em;
                                '>
                                |fill_variable|
                                </span>"""

# Definimos una barra horizontal para separar secciones de la interfaz
horizontal_bar = "<hr style='margin-top: 0; margin-bottom: 0; height: 1px; border: 1px solid #635985;'><br>"

# Definimos el color de los botones en Streamlit
purple_btn_colour = """
                        <style>
                            div.stButton > button:first-child {background-color: #4b0082; color:#ffffff;}
                            div.stButton > button:hover {background-color: RGB(0,112,192); color:#ffffff;}
                            div.stButton > button:focus {background-color: RGB(47,117,181); color:#ffffff;}
                        </style>
                    """

# Inicializamos el estado de la sesión de Streamlit
mystate = st.session_state
# Inicializamos las variables de estado si no existen
if "expired_cells" not in mystate: mystate.expired_cells = []  # Celdas expiradas
if "myscore" not in mystate: mystate.myscore = 0  # Puntuación del jugador
if "plyrbtns" not in mystate: mystate.plyrbtns = {}  # Botones del jugador
if "sidebar_emoji" not in mystate: mystate.sidebar_emoji = ''  # Emoji de la barra lateral
if "emoji_bank" not in mystate: mystate.emoji_bank = []  # Banco de emojis
if "GameDetails" not in mystate: mystate.GameDetails = ['Medium', 6, 7, '']  # Detalles del juego (dificultad, intervalo de autogeneración, celdas totales por fila o columna, nombre del jugador)
