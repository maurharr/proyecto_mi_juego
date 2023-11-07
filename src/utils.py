import pygame
from pygame.locals import *
from config import *

#▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅  Funciones  ▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅


def terminar():
    """
    Esta función se encarga de cerrar la aplicación del juego.
    """
    pygame.quit()
    exit()

def get_random(lista:list):
    """
    Devuelve un elemento aleatorio de la lista proporcionada.

    Args:
        lista: Una lista de la cual se seleccionará un elemento al azar.

    Returns:
        Un elemento aleatorio de la lista de entrada.
    """
    from random import choice
    return choice(lista)

def pausa():
    """
    Esta función se encarga de la pausa del juego entrando en un bucle para permitirle al jugador darse un descanso para despues continuar con el juego o salir.
    La pausa se puede cerrar presionando el botón [ENTER] o la tecla [P].
    """
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminar()        
            if event.type == KEYDOWN: 
                if event.key == K_ESCAPE:
                    terminar()
                if event.key == K_RETURN or event.key == K_p:
                    return
                                
def crear_rectangulo(imagen=None, left:float=100, top:float=100, ancho:float=80, largo:float=50, color=blue, borde:float=3, radio:float=0) -> dict:
    """
    Crea un rectángulo con opciones personalizables en un diccionario.

    Args:
        imagen (Surface, opcional): La imagen a mostrar en el rectángulo. Valor por defecto: None.
        left (float): La coordenada x del extremo izquierdo del rectángulo. Valor por defecto: 100.
        top (float): La coordenada y del extremo superior del rectángulo. Valor por defecto: 100.
        ancho (float): El ancho del rectángulo. Valor por defecto: 80.
        largo (float): El largo del rectángulo. Valor por defecto: 50.
        color (color): El color del rectángulo si no se proporciona una imagen. Valor por defecto: blue.
        borde (float): El ancho del borde del rectángulo. Valor por defecto: 3.
        radio (float): El radio de las esquinas del rectángulo. Valor por defecto: 0.

    Returns:
        dict: Un diccionario que contiene la información del rectángulo, incluyendo su imagen, su rectángulo, su color, el ancho de su borde y su radio de las esquinas.
    """
    rect = pygame.Rect(left, top, ancho, largo)
    if imagen:
        imagen = pygame.transform.scale(imagen, (ancho, largo))
    return {
        "imagen":imagen,
        "rect":rect,
        "color":color,
        "borde":borde,
        "radio":radio
        }
       
def mostrar_texto(superficie, texto, fuente, coordenadas, color_fuente=white, color_fondo=black):
    """
    Renderiza y muestra texto en una superficie.

    Args:
        superficie (Surface): La superficie en la que se mostrará el texto.
        texto (str): El texto que se va a mostrar.
        fuente (Font): La fuente utilizada para el texto.
        coordenadas (tupla): Las coordenadas (x, y) donde se mostrará el texto.
        color_fuente (color): El color del texto. Valor por defecto: white.
        color_fondo (color): El color del fondo del texto. Valor por defecto: black.
    """
    texto_renderizado = fuente.render(texto, True, color_fuente, color_fondo) #Convierte el texto en una imagen/superficie que pueda ser mostrada en una screen.
    texto_rectangulo = texto_renderizado.get_rect(center=coordenadas)
    superficie.blit(texto_renderizado, texto_rectangulo)
    

