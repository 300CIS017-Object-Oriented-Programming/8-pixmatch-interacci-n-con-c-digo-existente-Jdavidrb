# Importamos las bibliotecas necesarias
import streamlit as st  # Importamos streamlit con alias "st".
import os  # Trabajar con comandos del sistema operativo(manejo de rutas).
import time as tm # Trabajar con tiempos.
import random # Generar numeros aleatorios.
import base64 #  Codificar y decodificar datos en base64.
import json # Trabajar con datos JSON.
from PIL import Image  # Manejo de imagenes.
from streamlit_autorefresh import st_autorefresh # Para refrescar la pagina automaticamente usando autorefresh.

# Configuramos la página de Streamlit
st.set_page_config(page_title="PixMatch", page_icon="🕹️", layout="wide", initial_sidebar_state="expanded")

# Obtenemos la letra del disco en el que se está ejecutando el script
vDrive = os.path.splitdrive(os.getcwd())[0]
# Establecemos la ruta del proyecto
vpth = "./"

# Definimos el estilo de los emojis en el juego y otros elementos de la interfaz
sbe = """
        <span style='font-size: 140px;
                  border-radius: 7px;
                  text-align: center;
                  display: inline;
                  padding-top: 3px;
                  padding-bottom: 3px;
                  padding-left: 0.4em;
                  padding-right: 0.4em;
                  '>
                  |fill_variable|
        </span>"""


pressed_emoji = """
                    <span style='font-size: 24px;
                            border-radius: 7px;
                            text-align: center;
                            display:inline;
                            padding-top: 3px;
                            padding-bottom: 3px;
                            padding-left: 0.2em;
                            padding-right: 0.2em;
                            '>
                            |fill_variable|
                    </span>
                """

horizontal_bar = """
                <hr style='margin-top: 0; margin-bottom: 0; height: 1px; border: 1px solid #635985;'>
                <br>
"""  # thin divider line

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
if "expired_cells" not in mystate: mystate.expired_cells = []
if "myscore" not in mystate: mystate.myscore = 0
if "plyrbtns" not in mystate: mystate.plyrbtns = {}
if "sidebar_emoji" not in mystate: mystate.sidebar_emoji = ''
if "emoji_bank" not in mystate: mystate.emoji_bank = []
if "GameDetails" not in mystate: mystate.GameDetails = ['Medium', 6, 7,'']
if "failures" not in mystate: mystate.failures = 0 # (Modificacion no 3)


# Esta función ajusta el espacio desde la parte superior de la página o la barra lateral
def ReduceGapFromPageTop(wch_section='main page'):
    # Si la sección es la página principal, ajusta el espacio en la página principal
    if wch_section == 'main page':
        st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", True)
    # Si la sección es la barra lateral, ajusta el espacio en la barra lateral
    elif wch_section == 'sidebar':
        st.markdown(" <style> div[class^='st-emotion-cache-10oheav'] { padding-top: 0rem; } </style> ", True)
    # Si la sección es 'all', ajusta el espacio tanto en la página principal como en la barra lateral
    elif wch_section == 'all':
        st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", True)
        st.markdown(" <style> div[class^='st-emotion-cache-10oheav'] { padding-top: 0rem; } </style> ", True)


# Esta función maneja la creación, escritura y lectura de la tabla de líderes
def Leaderboard(what_to_do):
    if what_to_do == 'create':
        # Si se proporcionó el nombre del jugador
        if mystate.GameDetails[3] != '':
            # Y si el archivo 'leaderboard.json' no existe
            if os.path.isfile(vpth + 'leaderboard.json') == False:
                # Crea un diccionario vacío y lo escribe en el archivo 'leaderboard.json'
                tmpdict = {}
                json.dump(tmpdict, open(vpth + 'leaderboard.json', 'w'))

    # Si la acción es 'write'
    elif what_to_do == 'write':
        # Y si se proporcionó el nombre del jugador
        if mystate.GameDetails[3] != '':
            # Y si el archivo 'leaderboard.json' existe
            if os.path.isfile(vpth + 'leaderboard.json'):
                # Lee el archivo 'leaderboard.json'
                leaderboard = json.load(open(vpth + 'leaderboard.json'))
                leaderboard_dict_lngth = len(leaderboard)

                # Añade los detalles del juego del jugador al diccionario de la tabla de líderes
                leaderboard[mystate.GameDetails[3]] = {'NameCountry': mystate.GameDetails[3],
                                                       'HighestScore': mystate.myscore}
                # Ordena el diccionario de la tabla de líderes en orden descendente por la puntuación más alta
                leaderboard = dict(sorted(leaderboard.items(), key=lambda item: item[1]['HighestScore'], reverse=True))

                # Si la longitud de la tabla de líderes es mayor que 4 (Modificacion no 1)
                if len(leaderboard) > 4:
                    # Elimina los últimos elementos de la tabla de líderes hasta que su longitud sea 4 (Modificacion no1)
                    for i in range(len(leaderboard) - 4): leaderboard.popitem()

                # Escribe el diccionario de la tabla de líderes en el archivo 'leaderboard.json'
                json.dump(leaderboard, open(vpth + 'leaderboard.json', 'w'))

    # Si la acción es 'read'
    elif what_to_do == 'read':
        # Y si se proporcionó el nombre del jugador
        if mystate.GameDetails[3] != '':
            # Y si el archivo 'leaderboard.json' existe
            if os.path.isfile(vpth + 'leaderboard.json'):
                # Lee el archivo 'leaderboard.json'
                leaderboard = json.load(open(vpth + 'leaderboard.json'))

                # Ordena el diccionario de la tabla de líderes en orden descendente por la puntuación más alta
                leaderboard = dict(sorted(leaderboard.items(), key=lambda item: item[1]['HighestScore'], reverse=True))

                # Crea columnas para mostrar los ganadores pasados
                sc0, sc1, sc2, sc3, sc4 = st.columns((2, 3, 3, 3))
                rknt = 0
                # Para cada clave en la tabla de líderes
                for vkey in leaderboard.keys():
                    # Si el nombre del país no está vacío
                    if leaderboard[vkey]['NameCountry'] != '':
                        # Incrementa el contador de rango
                        rknt += 1
                        # Mostrar los ganadores segun el rango
                        if rknt == 1:
                            sc0.write('🏆 Ganadores pasados:')
                            sc1.write(
                                f"🥇 | {leaderboard[vkey]['NameCountry']}: :red[{leaderboard[vkey]['HighestScore']}]")
                        # Si el rango es 2, muestra el segundo ganador
                        elif rknt == 2:
                            sc2.write(
                                f"🥈 | {leaderboard[vkey]['NameCountry']}: :red[{leaderboard[vkey]['HighestScore']}]")
                        # Si el rango es 3, muestra el tercer ganador
                        elif rknt == 3:
                            sc3.write(
                                f"🥈 | {leaderboard[vkey]['NameCountry']}: :red[{leaderboard[vkey]['HighestScore']}]")

                        elif rknt == 4: # (modificacion no2)
                            sc4.write(
                                f"🥉 | {leaderboard[vkey]['NameCountry']}: :red[{leaderboard[vkey]['HighestScore']}]")


# Esta función configura la página inicial del juego
def InitialPage():
    # Configura la barra lateral de Streamlit
    with st.sidebar:
        # Muestra el título del juego y una barra horizontal
        st.subheader("🖼️ Pix Match:")
        st.markdown(horizontal_bar, True)

        # Abre y redimensiona la imagen del logo de la barra lateral
        sidebarlogo = Image.open('sidebarlogo.jpg').resize((300, 390))
        # Muestra la imagen del logo en la barra lateral
        st.image(sidebarlogo, use_column_width='auto')


    # Define las instrucciones del juego
    hlp_dtl = f"""<span style="font-size: 26px;">
    <ol>
    <li style="font-size:15px";>El juego comienza con (a) una imagen en la barra lateral y (b) una cuadrícula N x N de botones de imágenes, donde N=6:Fácil, N=7:Medio, N=8:Difícil.</li>
    <li style="font-size:15px";>Necesitas hacer coincidir la imagen de la barra lateral con un botón de imagen de la cuadrícula, presionando el botón (correspondiente) (lo más rápido posible).</li>
    <li style="font-size:15px";>Cada coincidencia correcta de imágenes te dará <strong>+N</strong> puntos (donde N=5:Fácil, N=3:Medio, N=1:Difícil); cada coincidencia incorrecta de imágenes te dará <strong>-1</strong> punto.</li>
    <li style="font-size:15px";>La imagen de la barra lateral y las imágenes de la cuadrícula se regenerarán dinámicamente después de un intervalo de segundos fijo (Fácil=8, Medio=6, Difícil=5). Cada regeneración tendrá una penalización de <strong>-1</strong> punto</li>
    <li style="font-size:15px";>Cada uno de los botones de la cuadrícula solo puede ser presionado una vez durante todo el juego.</li>
    <li style="font-size:15px";>El juego se completa cuando todos los botones de la cuadrícula son presionados.</li>
    <li style="font-size:15px";>Al final del juego, si tienes una puntuación positiva, habrás <strong>ganado</strong>; de lo contrario, habrás <strong>perdido</strong>.</li>
    </ol></span>"""

    # Crea dos columnas para mostrar las instrucciones del juego y una imagen de ayuda
    sc1, sc2 = st.columns(2)
    # Establece la semilla para la generación de números aleatorios
    random.seed()
    # Selecciona una imagen de ayuda aleatoria
    GameHelpImg = vpth + random.choice(["MainImg1.jpg", "MainImg2.jpg", "MainImg3.jpg", "MainImg4.jpg"])
    # Abre y redimensiona la imagen de ayuda
    GameHelpImg = Image.open(GameHelpImg).resize((550, 550))
    # Muestra la imagen de ayuda en la segunda columna
    sc2.image(GameHelpImg, use_column_width='auto')

    # En la primera columna, muestra el título de las instrucciones del juego y una barra horizontal
    sc1.subheader('Reglas | Instrucciones de juego:')
    sc1.markdown(horizontal_bar, True)
    # Muestra las instrucciones del juego
    sc1.markdown(hlp_dtl, unsafe_allow_html=True)
    # Muestra una barra horizontal en la página principal
    st.markdown(horizontal_bar, True)

    # Muestra los detalles del autor del juego
    author_dtl = "<strong>Juego feliz: 😎 Shawn Pereira: shawnpereira1969@gmail.com</strong>"
    st.markdown(author_dtl, unsafe_allow_html=True)


# Esta función lee un archivo de imagen y lo codifica en base64
def ReadPictureFile(wch_fl):
    try:
        pxfl = f"{vpth}{wch_fl}"
        return base64.b64encode(open(pxfl, 'rb').read()).decode()
    except:
        return ""


# Esta función verifica si un botón ha sido presionado y actualiza el estado del juego en consecuencia
def PressedCheck(vcell):
    # Si el botón no ha sido presionado
    if mystate.plyrbtns[vcell]['isPressed'] == False:
        # Marca el botón como presionado
        mystate.plyrbtns[vcell]['isPressed'] = True
        # Agrega la celda a la lista de celdas expiradas
        mystate.expired_cells.append(vcell)

        # Si el emoji del botón coincide con el emoji de la barra lateral
        if mystate.plyrbtns[vcell]['eMoji'] == mystate.sidebar_emoji:
            # Marca el botón como verdadero
            mystate.plyrbtns[vcell]['isTrueFalse'] = True
            # Aumenta la puntuación del jugador
            mystate.myscore += 5

            # Ajusta la puntuación en función del nivel de dificultad
            if mystate.GameDetails[0] == 'Easy':
                mystate.myscore += 5
            elif mystate.GameDetails[0] == 'Medium':
                mystate.myscore += 3
            elif mystate.GameDetails[0] == 'Hard':
                mystate.myscore += 1
        else:
            # Si el emoji del botón no coincide con el emoji de la barra lateral, marca el botón como falso
            mystate.plyrbtns[vcell]['isTrueFalse'] = False
            # Disminuye la puntuación del jugador
            mystate.myscore -= 1
            # (Modificacion no3)
            mystate.failures += 1  # Incrementamos el contador de fallos



# Esta función restablece el tablero de juego
def ResetBoard():
    # Obtiene el número total de celdas por fila o columna
    total_cells_per_row_or_col = mystate.GameDetails[2]

    # Selecciona un emoji aleatorio de la lista de emojis para la barra lateral
    sidebar_emoji_no = random.randint(1, len(mystate.emoji_bank)) - 1
    mystate.sidebar_emoji = mystate.emoji_bank[sidebar_emoji_no]

    # Inicializa una variable para verificar si el emoji de la barra lateral está en la lista
    sidebar_emoji_in_list = False

    # Recorre todas las celdas del tablero
    for vcell in range(1, ((total_cells_per_row_or_col ** 2) + 1)):
        # Selecciona un emoji aleatorio de la lista de emojis
        rndm_no = random.randint(1, len(mystate.emoji_bank)) - 1

        # Si el botón no ha sido presionado
        if mystate.plyrbtns[vcell]['isPressed'] == False:
            # Asigna el emoji aleatorio al botón
            vemoji = mystate.emoji_bank[rndm_no]
            mystate.plyrbtns[vcell]['eMoji'] = vemoji

            # Si el emoji del botón coincide con el emoji de la barra lateral, marca la variable como verdadera
            if vemoji == mystate.sidebar_emoji: sidebar_emoji_in_list = True

    # Si el emoji de la barra lateral no está en ningún botón, añade el emoji de forma aleatoria
    if sidebar_emoji_in_list == False:
        # Crea una lista de todas las celdas
        tlst = [x for x in range(1, ((total_cells_per_row_or_col ** 2) + 1))]
        # Crea una lista de las celdas que no están en la lista de celdas expiradas
        flst = [x for x in tlst if x not in mystate.expired_cells]

        # Si hay celdas disponibles
        if len(flst) > 0:
            # Selecciona una celda aleatoria de la lista
            lptr = random.randint(0, (len(flst) - 1))
            lptr = flst[lptr]

            # Asigna el emoji de la barra lateral a la celda seleccionada
            mystate.plyrbtns[lptr]['eMoji'] = mystate.sidebar_emoji


# Esta función prepara un nuevo juego
def PreNewGame():
    # Obtiene el número total de celdas por fila o columna
    total_cells_per_row_or_col = mystate.GameDetails[2]
    # Reinicia las celdas expiradas y la puntuación
    mystate.expired_cells = []
    mystate.myscore = 0
    mystate.failures = 0 # (Modificacion no3)

    # Define las listas de emojis
    foxes = ['😺', '😸', '😹', '😻', '😼', '😽', '🙀', '😿', '😾']
    emojis = ['😃', '😄', '😁', '😆', '😅', '😂', '🤣', '😊', '😇', '🙂', '🙃', '😉', '😌', '😍', '🥰', '😘', '😗', '😙', '😚', '😋', '😛',
              '😝', '😜', '🤪', '🤨', '🧐', '🤓', '😎', '🤩', '🥳', '😏', '😒', '😞', '😔', '😟', '😕', '🙁', '☹️', '😣', '😖', '😫', '😩',
              '🥺', '😢', '😠', '😳', '😥', '😓', '🤗', '🤔', '🤭', '🤫', '🤥', '😶', '😐', '😑', '😬', '🙄', '😯', '😧', '😮', '😲', '🥱',
              '😴', '🤤', '😪', '😵', '🤐', '🥴', '🤒']
    humans = ['👶', '👧', '🧒', '👦', '👩', '🧑', '👨', '👩‍🦱', '👨‍🦱', '👩‍🦰', '‍👨', '👱', '👩', '👱', '👩‍', '👨‍🦳', '👩‍🦲', '👵', '🧓',
              '👴', '👲', '👳']
    foods = ['🍏', '🍎', '🍐', '🍊', '🍋', '🍌', '🍉', '🍇', '🍓', '🍈', '🍒', '🍑', '🥭', '🍍', '🥥', '🥝', '🍅', '🍆', '🥑', '🥦', '🥬',
             '🥒', '🌽', '🥕', '🧄', '🧅', '🥔', '🍠', '🥐', '🥯', '🍞', '🥖', '🥨', '🧀', '🥚', '🍳', '🧈', '🥞', '🧇', '🥓', '🥩', '🍗',
             '🍖', '🦴', '🌭', '🍔', '🍟', '🍕']
    clocks = ['🕓', '🕒', '🕑', '🕘', '🕛', '🕚', '🕖', '🕙', '🕔', '🕤', '🕠', '🕕', '🕣', '🕞', '🕟', '🕜', '🕢', '🕦']
    hands = ['🤚', '🖐', '✋', '🖖', '👌', '🤏', '✌️', '🤞', '🤟', '🤘', '🤙', '👈', '👉', '👆', '🖕', '👇', '☝️', '👍', '👎', '✊', '👊',
             '🤛', '🤜', '👏', '🙌', '🤲', '🤝', '🤚🏻', '🖐🏻', '✋🏻', '🖖🏻', '👌🏻', '🤏🏻', '✌🏻', '🤞🏻', '🤟🏻', '🤘🏻', '🤙🏻', '👈🏻',
             '👉🏻', '👆🏻', '🖕🏻', '👇🏻', '☝🏻', '👍🏻', '👎🏻', '✊🏻', '👊🏻', '🤛🏻', '🤜🏻', '👏🏻', '🙌🏻', '🤚🏽', '🖐🏽', '✋🏽', '🖖🏽',
             '👌🏽', '🤏🏽', '✌🏽', '🤞🏽', '🤟🏽', '🤘🏽', '🤙🏽', '👈🏽', '👉🏽', '👆🏽', '🖕🏽', '👇🏽', '☝🏽', '👍🏽', '👎🏽', '✊🏽', '👊🏽',
             '🤛🏽', '🤜🏽', '👏🏽', '🙌🏽']
    animals = ['🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼', '🐨', '🐯', '🦁', '🐮', '🐷', '🐽', '🐸', '🐵', '🙈', '🙉', '🙊', '🐒', '🐔',
               '🐧', '🐦', '🐤', '🐣', '🐥', '🦆', '🦅', '🦉', '🦇', '🐺', '🐗', '🐴', '🦄', '🐝', '🐛', '🦋', '🐌', '🐞', '🐜', '🦟', '🦗',
               '🦂', '🐢', '🐍', '🦎', '🦖', '🦕', '🐙', '🦑', '🦐', '🦞', '🦀', '🐡', '🐠', '🐟', '🐬', '🐳', '🐋', '🦈', '🐊', '🐅', '🐆',
               '🦓', '🦍', '🦧', '🐘', '🦛', '🦏', '🐪', '🐫', '🦒', '🦘', '🐃', '🐂', '🐄', '🐎', '🐖', '🐏', '🐑', '🦙', '🐐', '🦌', '🐕',
               '🐩', '🦮', '🐕‍🦺', '🐈', '🐓', '🦃', '🦚', '🦜', '🦢', '🦩', '🐇', '🦝', '🦨', '🦦', '🦥', '🐁', '🐀', '🦔']
    vehicles = ['🚗', '🚕', '🚙', '🚌', '🚎', '🚓', '🚑', '🚒', '🚐', '🚚', '🚛', '🚜', '🦯', '🦽', '🦼', '🛴', '🚲', '🛵', '🛺', '🚔', '🚍',
                '🚘', '🚖', '🚡', '🚠', '🚟', '🚃', '🚋', '🚞', '🚝', '🚄', '🚅', '🚈', '🚂', '🚆', '🚇', '🚊', '🚉', '✈️', '🛫', '🛬',
                '💺', '🚀', '🛸', '🚁', '🛶', '⛵️', '🚤', '🛳', '⛴', '🚢']
    houses = ['🏠', '🏡', '🏘', '🏚', '🏗', '🏭', '🏢', '🏬', '🏣', '🏤', '🏥', '🏦', '🏨', '🏪', '🏫', '🏩', '💒', '🏛', '⛪️', '🕌', '🕍',
              '🛕']
    purple_signs = ['☮️', '✝️', '☪️', '☸️', '✡️', '🔯', '🕎', '☯️', '☦️', '🛐', '⛎', '♈️', '♉️', '♊️', '♋️', '♌️', '♍️',
                    '♎️', '♏️', '♐️', '♑️', '♒️', '♓️', '🆔', '🈳']
    red_signs = ['🈶', '🈚️', '🈸', '🈺', '🈷️', '✴️', '🉐', '㊙️', '㊗️', '🈴', '🈵', '🈹', '🈲', '🅰️', '🅱️', '🆎', '🆑', '🅾️', '🆘',
                 '🚼', '🛑', '⛔️', '📛', '🚫', '🚷', '🚯', '🚳', '🚱', '🔞', '📵', '🚭']
    blue_signs = ['🚾', '♿️', '🅿️', '🈂️', '🛂', '🛃', '🛄', '🛅', '🚹', '🚺', '🚻', '🚮', '🎦', '📶', '🈁', '🔣', '🔤', '🔡', '🔠', '🆖',
                  '🆗', '🆙', '🆒', '🆕', '🆓', '0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟',
                  '🔢', '⏏️', '▶️', '⏸', '⏯', '⏹', '⏺', '⏭', '⏮', '⏩', '⏪', '⏫', '⏬', '◀️', '🔼', '🔽', '➡️', '⬅️', '⬆️',
                  '⬇️', '↗️', '↘️', '↙️', '↖️', '↪️', '↩️', '⤴️', '⤵️', '🔀', '🔁', '🔂', '🔄', '🔃', '➿', '🔚', '🔙', '🔛',
                  '🔝', '🔜']
    moon = ['🌕', '🌔', '🌓', '🌗', '🌒', '🌖', '🌑', '🌜', '🌛', '🌙']

    # Establece la semilla para la generación de números aleatorios
    random.seed()

    # Selecciona el banco de emojis en función del nivel de dificultad
    if mystate.GameDetails[0] == 'Easy':
        wch_bank = random.choice(['foods', 'moon', 'animals'])
        mystate.emoji_bank = locals()[wch_bank]
    elif mystate.GameDetails[0] == 'Medium':
        wch_bank = random.choice(
            ['foxes', 'emojis', 'humans', 'vehicles', 'houses', 'hands', 'purple_signs', 'red_signs', 'blue_signs'])
        mystate.emoji_bank = locals()[wch_bank]
    elif mystate.GameDetails[0] == 'Hard':
        wch_bank = random.choice(
            ['foxes', 'emojis', 'humans', 'foods', 'clocks', 'hands', 'animals', 'vehicles', 'houses', 'purple_signs',
             'red_signs', 'blue_signs', 'moon'])
        mystate.emoji_bank = locals()[wch_bank]

    # Inicializa los botones del jugador
    mystate.plyrbtns = {}
    for vcell in range(1, ((total_cells_per_row_or_col ** 2) + 1)):
        mystate.plyrbtns[vcell] = {'isPressed': False, 'isTrueFalse': False, 'eMoji': ''}


# Esta función devuelve un emoji basado en la puntuación del jugador
def ScoreEmoji():
    if mystate.myscore == 0:
        return '😐'
    elif -5 <= mystate.myscore <= -1:
        return '😏'
    elif -10 <= mystate.myscore <= -6:
        return '☹️'
    elif mystate.myscore <= -11:
        return '😖'
    elif 1 <= mystate.myscore <= 5:
        return '🙂'
    elif 6 <= mystate.myscore <= 10:
        return '😊'
    elif mystate.myscore > 10:
        return '😁'


# Esta función inicia un nuevo juego
def NewGame():
    # Llama a la función ResetBoard para preparar el tablero de juego
    ResetBoard()
    # Obtiene el número total de celdas por fila o columna
    total_cells_per_row_or_col = mystate.GameDetails[2]

    # Configura la barra lateral de Streamlit
    ReduceGapFromPageTop('sidebar')
    with st.sidebar:
        # Muestra el título del juego y una barra horizontal
        st.subheader(f"🖼️ Pix Match: {mystate.GameDetails[0]}")
        st.markdown(horizontal_bar, True)

        # Muestra el emoji de la barra lateral
        st.markdown(sbe.replace('|fill_variable|', mystate.sidebar_emoji), True)

        # Configura un temporizador de autorefresco y disminuye la puntuación del jugador si el temporizador es mayor que 0
        aftimer = st_autorefresh(interval=(mystate.GameDetails[1] * 1000), key="aftmr")
        if aftimer > 0: mystate.myscore -= 1

        # Muestra la puntuación del jugador y el número de celdas pendientes
        st.info(
            f"{ScoreEmoji()} Score: {mystate.myscore} | Pending: {(total_cells_per_row_or_col ** 2) - len(mystate.expired_cells)}")

        # Muestra una barra horizontal y un botón para volver a la página principal
        st.markdown(horizontal_bar, True)
        if st.button(f"🔙 Return to Main Page", use_container_width=True):
            mystate.runpage = Main
            st.rerun()

    # Llama a la función Leaderboard para mostrar la tabla de líderes
    Leaderboard('read')
    # Muestra el título de las posiciones de las imágenes y una barra horizontal
    st.subheader("Picture Positions:")
    st.markdown(horizontal_bar, True)

    # Configura el tamaño de los emojis en los botones
    st.markdown("<style> div[class^='css-1vbkxwb'] > p { font-size: 1.5rem; } </style> ", unsafe_allow_html=True)

    # Crea las columnas para los botones del tablero de juego
    for i in range(1, (total_cells_per_row_or_col + 1)):
        tlst = ([1] * total_cells_per_row_or_col) + [2]  # 2 = rt side padding
        globals()['cols' + str(i)] = st.columns(tlst)

    # Rellena el tablero de juego con los botones
    for vcell in range(1, (total_cells_per_row_or_col ** 2) + 1):
        # Determina la fila del botón en función de su número
        if 1 <= vcell <= (total_cells_per_row_or_col * 1):
            arr_ref = '1'
            mval = 0
        elif ((total_cells_per_row_or_col * 1) + 1) <= vcell <= (total_cells_per_row_or_col * 2):
            arr_ref = '2'
            mval = (total_cells_per_row_or_col * 1)
        if 1 <= vcell <= (total_cells_per_row_or_col * 1):
            arr_ref = '1'
            mval = 0

        elif ((total_cells_per_row_or_col * 1) + 1) <= vcell <= (total_cells_per_row_or_col * 2):
            arr_ref = '2'
            mval = (total_cells_per_row_or_col * 1)

        elif ((total_cells_per_row_or_col * 2) + 1) <= vcell <= (total_cells_per_row_or_col * 3):
            arr_ref = '3'
            mval = (total_cells_per_row_or_col * 2)

        elif ((total_cells_per_row_or_col * 3) + 1) <= vcell <= (total_cells_per_row_or_col * 4):
            arr_ref = '4'
            mval = (total_cells_per_row_or_col * 3)

        elif ((total_cells_per_row_or_col * 4) + 1) <= vcell <= (total_cells_per_row_or_col * 5):
            arr_ref = '5'
            mval = (total_cells_per_row_or_col * 4)

        elif ((total_cells_per_row_or_col * 5) + 1) <= vcell <= (total_cells_per_row_or_col * 6):
            arr_ref = '6'
            mval = (total_cells_per_row_or_col * 5)

        elif ((total_cells_per_row_or_col * 6) + 1) <= vcell <= (total_cells_per_row_or_col * 7):
            arr_ref = '7'
            mval = (total_cells_per_row_or_col * 6)

        elif ((total_cells_per_row_or_col * 7) + 1) <= vcell <= (total_cells_per_row_or_col * 8):
            arr_ref = '8'
            mval = (total_cells_per_row_or_col * 7)

        elif ((total_cells_per_row_or_col * 8) + 1) <= vcell <= (total_cells_per_row_or_col * 9):
            arr_ref = '9'
            mval = (total_cells_per_row_or_col * 8)

        elif ((total_cells_per_row_or_col * 9) + 1) <= vcell <= (total_cells_per_row_or_col * 10):
            arr_ref = '10'
            mval = (total_cells_per_row_or_col * 9)

        globals()['cols' + arr_ref][vcell - mval] = globals()['cols' + arr_ref][vcell - mval].empty()

        # Si el botón ha sido presionado, muestra un emoji de verificación o de error en función de si la elección fue correcta o no
        if mystate.plyrbtns[vcell]['isPressed'] == True:
            if mystate.plyrbtns[vcell]['isTrueFalse'] == True:
                globals()['cols' + arr_ref][vcell - mval].markdown(pressed_emoji.replace('|fill_variable|', '✅️'), True)
            elif mystate.plyrbtns[vcell]['isTrueFalse'] == False:
                globals()['cols' + arr_ref][vcell - mval].markdown(pressed_emoji.replace('|fill_variable|', '❌'), True)

        # Si el botón no ha sido presionado, muestra el emoji correspondiente y configura la acción al hacer clic en el botón
        else:
            vemoji = mystate.plyrbtns[vcell]['eMoji']
            globals()['cols' + arr_ref][vcell - mval].button(vemoji, on_click=PressedCheck, args=(vcell,),
                                                             key=f"B{vcell}")
    # Añade un espacio vertical
    st.caption('')
    # Añade una barra horizontal
    st.markdown(horizontal_bar, True)

    # Comprueba si todas las celdas han sido presionadas o si el jugador ha perdido (Modificacion no3)
    if len(mystate.expired_cells) == (total_cells_per_row_or_col ** 2) or mystate.failures > (total_cells_per_row_or_col ** 2) / 2:
        # Si todas las celdas han sido presionadas, escribe los resultados en la tabla de líderes
        Leaderboard('write')

        # Si la puntuación del jugador es positiva, muestra globos
        if mystate.myscore > 0:
            st.balloons()
        # Si la puntuación del jugador es cero o negativa, muestra nieve
        elif mystate.myscore <= 0:
            st.snow()

        # Espera 5 segundos
        tm.sleep(5)
        # Cambia la página a la página principal
        mystate.runpage = Main
        # Recarga la página
        st.rerun()


# Esta función configura la página principal del juego
def Main():
    # Reduce el ancho de la barra lateral de Streamlit
    st.markdown('<style>[data-testid="stSidebar"] > div:first-child {width: 310px;}</style>', unsafe_allow_html=True, )
    # Configura el color del botón
    st.markdown(purple_btn_colour, unsafe_allow_html=True)

    # Llama a la función InitialPage para configurar la página inicial
    InitialPage()
    # Configura la barra lateral de Streamlit
    with st.sidebar:
        # Permite al jugador seleccionar el nivel de dificultad
        mystate.GameDetails[0] = st.radio('Difficulty Level:', options=('Easy', 'Medium', 'Hard'), index=1,
                                          horizontal=True, )
        # Permite al jugador introducir su nombre y país (opcional)
        mystate.GameDetails[3] = st.text_input("Player Name, Country", placeholder='Shawn Pereira, India',
                                               help='Optional input only for Leaderboard')

        # Si el jugador pulsa el botón "Nuevo juego"
        if st.button(f"🕹️ New Game", use_container_width=True):
            # Configura los detalles del juego en función del nivel de dificultad seleccionado
            if mystate.GameDetails[0] == 'Easy':
                mystate.GameDetails[1] = 8  # intervalo en segundos
                mystate.GameDetails[2] = 6  # total de celdas por fila o columna

            elif mystate.GameDetails[0] == 'Medium':
                mystate.GameDetails[1] = 6  # intervalo en segundos
                mystate.GameDetails[2] = 7  # total de celdas por fila o columna

            elif mystate.GameDetails[0] == 'Hard':
                mystate.GameDetails[1] = 5  # intervalo en segundos
                mystate.GameDetails[2] = 8  # total de celdas por fila o columna

            # Crea la tabla de líderes
            Leaderboard('create')

            # Prepara el nuevo juego
            PreNewGame()
            # Configura la página para ejecutar el nuevo juego
            mystate.runpage = NewGame
            # Recarga la página
            st.rerun()

        # Muestra una barra horizontal en la barra lateral
        st.markdown(horizontal_bar, True)


# Si la página a ejecutar no está en el estado de la sesión, configura la página a ejecutar como Main
if 'runpage' not in mystate: mystate.runpage = Main
# Ejecuta la página configurada
mystate.runpage()
