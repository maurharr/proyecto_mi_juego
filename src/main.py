import pygame
from pygame.locals import *
from random import choice
from config import *
from utils import *

#▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅  Configuración  ▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅


# Inicializar modulos de Pygame
pygame.init()


# Pantalla
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption("Taxi Driver")


# Configuración de reloj
clock = pygame.time.Clock()

#logo
logo = pygame.image.load("./src/assets/images/reloj.png")
pygame.display.set_icon(logo)

#fuente
fuente = pygame.font.Font("./src/assets/fonts/BlockKie.ttf", 36)
fuente_pausa = pygame.font.Font("./src/assets/fonts/BlockKie.ttf", 72)
fuente_dialog = pygame.font.Font("./src/assets/fonts/BlockKie.ttf", 54)
fuente_mensaje = pygame.font.Font("./src/assets/fonts/BlockKie.ttf", 28)
fuente_credito = pygame.font.Font("./src/assets/fonts/BlockKie.ttf", 20)


#Fondo
fondo1 = pygame.image.load("./src/assets/images/background.png")
fondo2 = pygame.image.load("./src/assets/images/background1.png")
fondo3 = pygame.image.load("./src/assets/images/background2.png")
lista_fondos = [fondo1, fondo2, fondo3]


#imagenes
image_player_car = pygame.image.load("./src/assets/images/player.png")

image_enemy = pygame.image.load("./src/assets/images/enemy.png")
image_enemy1 = pygame.image.load("./src/assets/images/enemy1.png")
image_enemy2 = pygame.image.load("./src/assets/images/enemy2.png")
image_enemy3 = pygame.image.load("./src/assets/images/enemy3.png")
image_enemy4 = pygame.image.load("./src/assets/images/enemy4.png")
image_enemy5 = pygame.image.load("./src/assets/images/enemy5.png")
lista_image_enemy = [image_enemy, image_enemy1, image_enemy2, image_enemy3, image_enemy4, image_enemy5]

image_rock = pygame.image.load("./src/assets/images/rock.png")
image_reloj = pygame.image.load("./src/assets/images/reloj.png")

intro = pygame.image.load("./src/assets/images/intro.png")
background_pause = pygame.image.load("./src/assets/images/background_pause.png")
background_crash = pygame.image.load("./src/assets/images/crash.png")
background_game_over = pygame.image.load("./src/assets/images/game_over.png")


# #sonidos
explosion_sound = pygame.mixer.Sound("./src/assets/sounds/explosion.mp3")
explosion_sound.set_volume(0.05)

reloj_bonus_sound = pygame.mixer.Sound("./src/assets/sounds/reloj_bonus.mp3")
reloj_bonus_sound.set_volume(0.1)

time_left_sound = pygame.mixer.Sound("./src/assets/sounds/time_left.mp3")
time_left_sound.set_volume(0.4)

game_over_sound = pygame.mixer.Sound("./src/assets/sounds/game_over.mp3")
game_over_sound.set_volume(0.2)

pygame.mixer.music.load("./src/assets/sounds/background.mp3")
pygame.mixer.music.set_volume(0.2)

listen_music = True

#▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅ GUARDADO DE LA MAX PUNTACION ▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅


try:
    with open(".\src\score.txt", "r") as file: 
        contador_record = float(file.read()) # Aca almaceno el valor guardado en el archivo "score.txt" en entero por la variable contador_record para prox. ser comparada y reemplazada

except FileNotFoundError:
    print("No existe 'score.txt'. Por lo tanto, se creará uno.")
    with open(".\src\score.txt", "w") as file: # Con esta linea puedo crear el archivo "score.txt"
        file.write("0") # Le entrego un valor, en este caso el 0, para despues poder ser reemplazado.
        contador_record = 0


#▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅   FUNCIONES   ▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅


def cargar_autos(lista:list, cantidad:int, imagen=None, sentido:bool=True, top=340):
    """
    Esta función se utiliza para cargar una lista con objetos rectangulares que representan autos.

    Args:
        lista (lista): Una lista en la que se agregarán los objetos rectangulares que representan los autos.
        cantidad (int): La cantidad de autos que se deben cargar en la lista.
        imagen (pygame.Surface, opcional): La imagen que se utilizará para representar los autos. Si no se proporciona, se usará una imagen predeterminada. Valor por defecto: None.
        sentido (booleano): Un valor booleano que indica si los autos se mueven en la dirección predeterminada (True) o en dirección contraria (False). Valor por defecto: True.
        top: La posición vertical inicial en la que se generarán los autos. Si no se proporciona, se utilizará una posición predeterminada. Valor por defecto: 340.
        """
    for i in range(cantidad):
        if sentido:
            lista.append(crear_rectangulo(imagen=get_random(lista_image_enemy), left=get_random(posiciones_x), top=get_random(pos_y_1)))
        else:
            lista.append(crear_rectangulo(imagen=pygame.transform.flip(get_random(lista_image_enemy),True, False), left=get_random(posiciones_x), top=get_random(pos_y_2)))

def crear_boton(superficie, left: float = 100, top: float = 100, ancho: float = 80, largo: float = 50, color=blue, borde: float = 3, radio: float = 0, texto=None, fuente=fuente_mensaje):
    rect = pygame.Rect(left, top, ancho, largo)
    dict = {
        "rect": rect,
        "color": color,
        "borde": borde,
        "radio": radio,
        "texto": texto
    }
    pygame.draw.rect(superficie, dict["color"], dict["rect"], dict["borde"], dict["radio"])
    texto = mostrar_texto(superficie, texto, fuente, (dict["rect"].center), black, None)
    return dict  
    
def menu():
    """
    Muestra el menú principal del juego y maneja las interacciones del jugador.

    El menú permite al jugador elegir entre jugar, acceder a las opciones del juego o salir.
    """
    global listen_music

    while True:
        screen.blit(intro, origen)
        mostrar_texto(screen, "Creado por Mauricio Harriet, 2023", fuente_credito, (WIDTH-150, HEIGTH-14), white, None)
        mostrar_texto(screen, "TAXI DRIVER", fuente_pausa, (WIDTH-200, 100), black, None)
        boton_jugar = crear_boton(screen, WIDTH-300, 200, 200, 50, grey, 0, 20, "Jugar", fuente)
        boton_opciones = crear_boton(screen, WIDTH-300, 300, 200, 50, grey, 0, 20, "Opciones", fuente)
        boton_salir = crear_boton(screen, WIDTH-300, 400, 200, 50, grey, 0, 20, "Salir", fuente)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                terminar()    
            if event.type == MOUSEBUTTONUP:
                if boton_jugar["rect"].collidepoint(event.pos):
                    global fondo
                    fondo = get_random(lista_fondos)
                    return
                if boton_opciones["rect"].collidepoint(event.pos):
                    menu_opciones()
                if boton_salir["rect"].collidepoint(event.pos):
                    terminar()

def menu_opciones():
    """
    Muestra el menú de opciones del juego y permite le permite al jugador activar o desactivar el volumen de la música y regresar al menú principal.
    """
    global listen_music  # Indicar que estamos utilizando la variable global
    while True:
        screen.blit(intro, origen)
        mostrar_texto(screen, "Creado por Mauricio Harriet, 2023", fuente_credito, (WIDTH-150, HEIGTH-14), white, None)
        mostrar_texto(screen, "OPCIONES", fuente_pausa, (WIDTH-200, 100), black, None)
        boton_atras = crear_boton(screen, WIDTH-300, 300, 200, 50, grey, 0, 20, "Atras", fuente)
        if listen_music:
            boton_volumen = crear_boton(screen, WIDTH-300, 200, 200, 50, grey, 0, 20, "Volumen ON", fuente)
        else:
            boton_volumen = crear_boton(screen, WIDTH-300, 200, 200, 50, grey, 0, 20, "Volumen OFF", fuente)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                terminar()    
            if event.type == MOUSEBUTTONUP:
                if boton_volumen["rect"].collidepoint(event.pos):
                    listen_music = not listen_music
                if boton_atras["rect"].collidepoint(event.pos):
                    return
                

#▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅  Parametros  ▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅


#Jugador
contador_vidas = 3
start_game = False
pj_avisado = False

#Hitbox del escenario
motion_enabled_rect = crear_rectangulo(None, 0, 100, WIDTH, HEIGTH-200, white)
contramano = crear_rectangulo(None, 0, 100, WIDTH, 175, yellow)
pasto = crear_rectangulo(None, 100, 275, color=black)


#▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅


while True:


    # Generación del player -------------
    player = crear_rectangulo(image_player_car, 100, 435, 80, 40, red)


    # Generación de Piedras -------------
    rock = crear_rectangulo(image_rock, WIDTH, 280, 40, 40, blue)


    # Generación del reloj bonus -------------
    reloj_bonus = crear_rectangulo(image_reloj, WIDTH*5, get_random(posiciones_y), 40, 40, green)
    f_time_left = False

    # Generación de autos en buena dirección -------------
    enemy_list = []
    enemy_count = 4
    cargar_autos(enemy_list, enemy_count, image_enemy)


    # Generación de autos en dirección contraria -------------
    enemy_reverse_list = []
    enemy_reverse_count = 4
    cargar_autos(enemy_reverse_list, enemy_reverse_count, pygame.transform.flip(image_enemy,True,False), False, top=choice([pos_y3,pos_y4]))


    # Más parametros -------------
    contador_puntos = 0
    f_timer = True
    timer = 30
    f_up = False
    f_down = False
    f_speedup = False
    

    # Trucos -------------
    f_mortalidad = True
    f_secret_car = False
    f_show_hitbox = False


    #▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅  Pantalla de inicio  ▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅

    if not start_game:
        menu()

    if not pj_avisado:
        screen.blit(background_pause, origen)
        pygame.draw.rect(screen, black, (50, 0, WIDTH - 100, HEIGTH))
        pygame.draw.rect(screen, black, (0, 0, WIDTH, 50))
        pygame.draw.rect(screen, black, (0, HEIGTH - 50, WIDTH, 50))
        mostrar_texto(screen, " COMO JUGAR ", fuente_pausa, (WIDTH // 2, 100), red, None)

        lista_avisos = [
            "Te moves arriba con 'W'",
            "Te moves abajo con 'S'",
            "Aceleras con 'D' - Bonificación de puntos X1",
            "Yendo en dirección contraria - Bonificación de puntos X3",
            "",
            "Evita chocar con autos y piedras",
            "o perderás una vida",
            "Si perdes todas tus vidas, perderás el juego",
            "",
            "Recuerda agarrar relojes para seguir jugando.",
            "",
            "¡Buena suerte!",
        ]
        text_y = 170
        for aviso in lista_avisos:
            mostrar_texto(screen, aviso, fuente_mensaje, (WIDTH // 2, text_y), white, None)
            text_y += 30

        mostrar_texto(screen, "Presione 'Enter' para empezar a jugar", fuente, (WIDTH//2, HEIGTH - 50), green, None)
        pygame.display.flip()
        pausa()

    pj_avisado = True
    start_game = True
    is_running = True

    if listen_music:
        pygame.mixer.music.play(-1)     


    #▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅  Bucle principal  ▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅


    while is_running:

        # Configuración de los FPS
        clock.tick(FPS)
        
        # Si estoy acelerando, los puntos se duplican
        if f_speedup:
            contador_puntos += punto


        #▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅  Configuración de eventos  ▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅


        for event in pygame.event.get():

            if event.type == QUIT:
                terminar()

        # Eventos al presionar un botón -------------
            if event.type == KEYDOWN:

                # Cerrar el juego con ESC
                if event.key == K_ESCAPE:
                    terminar()

                # Moverse para arriba
                if event.key == K_w:
                    f_up = True

                # Moverse para abajo
                if event.key == K_s:
                    f_down = True

                # Acelerar el auto
                if event.key == K_d:
                    f_speedup = True
                    
                # Activar la pausa
                if event.key == K_p:
                    if listen_music:
                        pygame.mixer.music.pause()
                    screen.blit(background_pause, origen)
                    pygame.draw.rect(screen, black, (0,0,WIDTH, 50))
                    pygame.draw.rect(screen, black, (0,HEIGTH-50,WIDTH, 50))
                    mostrar_texto(screen, f"PUNTAJE: {int(contador_puntos)}", fuente, (WIDTH-100, 25), white)
                    mostrar_texto(screen, f"VIDAS: {contador_vidas}", fuente, (100, 25), white)
                    mostrar_texto(screen, " PAUSA ", fuente_pausa, center_screen, white, black)
                    mostrar_texto(screen, " Pulsa 'P' para continuar ", fuente_dialog, (center_x, center_y+150), white, black)
                    mostrar_texto(screen, " Pulsa 'ESC' para salir ", fuente_dialog, (center_x, center_y+200), white, black)
                    pygame.display.flip()
                    pausa()
                    if listen_music:
                        pygame.mixer.music.unpause()

                # Activar truco inmortalidad
                if event.key == K_0:
                    f_mortalidad = False

                # Activar y Desactivar hitbox visuales
                if event.key == K_1:
                    f_show_hitbox = True
                if event.key == K_2:
                    f_show_hitbox = False


            # Eventos al dejar de apretar un botón -------------
            if event.type == KEYUP:

                # Dejar de mover el auto hacia arriba
                if event.key == K_w:
                    f_up = False

                # Dejar de mover el auto hacia abajo
                if event.key == K_s:
                    f_down = False

                # Dejar de acelerar
                if event.key == K_d:
                    f_speedup = False

                # Desactivar la inmortalidad
                if event.key == K_0:
                    f_mortalidad = True


        #▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅  Configuración de movimientos  ▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅


        # Jugador -------------

        # Movimiento hacia abajo
        if f_down and player["rect"].bottom <= motion_enabled_rect["rect"].bottom:
            player["rect"].bottom += speed_y

        # Movimiento hacia arriba
        if f_up and player["rect"].top >= motion_enabled_rect["rect"].top:
            player["rect"].bottom -= speed_y


        # Piedras -------------
        if f_speedup:
            rock["rect"].right -= speed_x*3
        else:
            rock["rect"].right -= speed_x


        # Reloj Bonus -------------
        if f_speedup:
            reloj_bonus["rect"].right -= speed_x*3
        else:
            reloj_bonus["rect"].right -= speed_x


        # Autos en buena direccion -------------
        for enemy in enemy_list:
            if f_speedup:
                enemy["rect"].left -= speed_x*2
            else:
                enemy["rect"].left += speed_x//3


        # Autos en direccion contraria -------------
        for enemy in enemy_reverse_list:
            if f_speedup:
                enemy["rect"].left -= 11
            else:
                enemy["rect"].left -= 5



        #▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅   Configuración de Colisiones   ▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅


        # Carretera en contramano -------------
        if player["rect"].colliderect(contramano["rect"]):
            contador_puntos += punto*3


        # Pasto -------------
        if player["rect"].colliderect(pasto["rect"]):
            speed_y = 2
        else:
            speed_y = 4


        # Reloj Bonus -------------
        if reloj_bonus["rect"].colliderect(player["rect"]):
            timer += 10
            reloj_bonus["rect"].left = WIDTH*5
            reloj_bonus["rect"].top = get_random(posiciones_y)
            if listen_music:
                reloj_bonus_sound.play()

        if reloj_bonus["rect"].right <= 0:
            reloj_bonus["rect"].left = WIDTH*5
            reloj_bonus["rect"].top = get_random(posiciones_y)
                    

        # Piedras -------------
        if f_mortalidad and rock["rect"].colliderect(player["rect"]):
            is_running = False 
            if contador_vidas >= 2:
                if listen_music:
                    explosion_sound.play()

        if rock["rect"].right <= 0:
            rock["rect"].left = WIDTH


        # Autos en buena direccion -------------
        for enemy in enemy_list[:]:

            if f_mortalidad and player["rect"].colliderect(enemy["rect"]):
                is_running = False
                if contador_vidas >= 2:
                    if listen_music:
                        explosion_sound.play()
                
            if enemy["rect"].right < 0:
                enemy_list.remove(enemy)

                if len(enemy_list) <= 1:
                    cargar_autos(enemy_list, enemy_count, image_enemy)


        # Autos en direccion contraria -------------
        for enemy in enemy_reverse_list[:]:

            if f_mortalidad and player["rect"].colliderect(enemy["rect"]):
                is_running = False
                if contador_vidas >= 2:
                    if listen_music:
                        explosion_sound.play()
            
            if enemy["rect"].right < 0:
                enemy_reverse_list.remove(enemy)

                if len(enemy_reverse_list) <= 1:
                    cargar_autos(enemy_reverse_list, enemy_reverse_count, pygame.transform.flip(image_enemy,True,False), False, top=choice([pos_y3,pos_y4]))


        #▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅   Dibujo en la pantalla   ▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅
        

        #Fondo ------------------
        screen.blit(fondo, origen)


        # Rectangulos negros "polares" ------------------
        pygame.draw.rect(screen, black, (0,0,WIDTH, 50))
        pygame.draw.rect(screen, black, (0,HEIGTH-50,WIDTH, 50))


        # Textos ------------------
        if f_timer:
            if timer > 10:
                mostrar_texto(screen, f"TIEMPO: {int(timer)}", fuente, (WIDTH//2, 25), white)
                if listen_music and f_time_left:
                    
                    time_left_sound.stop()
                    f_time_left = False
            else:
                mostrar_texto(screen, f"TIEMPO: {int(timer)}", fuente, (WIDTH//2, 25), red)
                if listen_music and not f_time_left:
                    time_left_sound.play()
                    f_time_left = True
            timer-=0.02
            if timer<1:
                is_running=False

        # Texto de record y vidas
        mostrar_texto(screen, f"RECORD: {int(contador_record)}", fuente, (WIDTH-100, HEIGTH-25), white)
        mostrar_texto(screen, f"VIDAS: {contador_vidas}", fuente, (100, 25), white)

        # Texto del  contador de puntos
        if contador_puntos > contador_record:
            mostrar_texto(screen, f"PUNTAJE: {int(contador_puntos)}", fuente, (WIDTH-100, 25), yellow)
        else:
            mostrar_texto(screen, f"PUNTAJE: {int(contador_puntos)}", fuente, (WIDTH-100, 25), white)
        
        # Texto del truco de inmortalidad
        if not f_mortalidad:
            mostrar_texto(screen, "Truco activado - Inmortalidad", fuente, (240, HEIGTH-25), yellow)


        # Jugador ------------------
        screen.blit(player["imagen"], player["rect"])


        # Piedras ------------------
        screen.blit(rock["imagen"], rock["rect"])
            

        # Reloj Bonus ------------------
        screen.blit(reloj_bonus["imagen"], reloj_bonus["rect"])


        # Autos en buena dirección ------------------
        for enemy in enemy_list:
            screen.blit(enemy["imagen"], enemy["rect"])
            if f_show_hitbox:
                pygame.draw.rect(screen, enemy["color"], enemy["rect"], enemy["borde"])


        # Autos en dirección contraria ------------------
        for enemy in enemy_reverse_list:
            screen.blit(enemy["imagen"], enemy["rect"])
            if f_show_hitbox:
                pygame.draw.rect(screen, enemy["color"], enemy["rect"], enemy["borde"])


        # Si f_show_hitbox es True, me permite ver las hitbox ------------------
        if f_show_hitbox:
            pygame.draw.rect(screen, player["color"], player["rect"], player["borde"])
            pygame.draw.rect(screen, rock["color"], rock["rect"], rock["borde"])
            pygame.draw.rect(screen, pasto["color"], pasto["rect"], pasto["borde"])
            pygame.draw.rect(screen, reloj_bonus["color"], reloj_bonus["rect"], reloj_bonus["borde"])
            pygame.draw.rect(screen, motion_enabled_rect["color"], motion_enabled_rect["rect"], motion_enabled_rect["borde"])
            pygame.draw.rect(screen, contramano["color"], contramano["rect"], contramano["borde"])

        # Actualizar pantalla ------------------
        pygame.display.flip()


    #▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅  GAME OVER  ▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅ 

    # Si el contador de puntos, supera al contador del record, este reemplazará su valor con el nuevo.
    if contador_puntos > contador_record:
        contador_record = contador_puntos

    # Pierdo una vida al perder
    contador_vidas -= 1

    # Si el contador de vidas es mayor a 0, entro a la operación para reintentar jugar:
    if contador_vidas > 0:
        with open("./src/score.txt", "w") as file:
            file.write(str(contador_record)) #Guardo el valor del contador_record en "score.txt"
        time_left_sound.stop()
        pygame.mixer.music.stop()
        screen.blit(background_crash, origen)
        pygame.draw.rect(screen, black, (0,0,WIDTH, 50))
        pygame.draw.rect(screen, black, (0,HEIGTH-50,WIDTH, 50))
        mostrar_texto(screen, f"RECORD: {int(contador_record)}", fuente, (WIDTH-100, HEIGTH-25), white)
        mostrar_texto(screen, f"PUNTAJE: {int(contador_puntos)}", fuente, (WIDTH-100, 25), white)
        mostrar_texto(screen, f"VIDAS: {contador_vidas}", fuente, (100, 25), white)
        mostrar_texto(screen, "Presione Enter para reintentar", fuente, (WIDTH//2, HEIGTH - 75), green)
        mostrar_texto(screen, " Intentalo otra vez ", fuente_pausa, center_screen, white)
        pygame.display.flip()
        pausa()
    # Si el contador de vidas es igual a 0, entro al game over definitivo.
    else:
        with open("./src/score.txt", "w") as file:
            file.write(str(contador_record)) #Guardo el valor del contador_record en "score.txt"
        pygame.mixer.music.stop()
        screen.blit(background_game_over, origen)
        pygame.draw.rect(screen, black, (0,0,WIDTH, 50))
        pygame.draw.rect(screen, black, (0,HEIGTH-50,WIDTH, 50))
        mostrar_texto(screen, f"TU PUNTAJE: {int(contador_puntos)}", fuente, (center_x, center_y+150), white)
        mostrar_texto(screen, f"RECORD: {int(contador_record)}", fuente, (center_x, center_y+180), white)
        mostrar_texto(screen, "Presione Enter para continuar", fuente, (WIDTH//2, HEIGTH - 75), yellow)
        pygame.display.flip()
        if listen_music:
            game_over_sound.play()
        contador_vidas = 3
        # Espero continuar para volver al menú
        pausa()
        game_over_sound.stop()
        start_game = False
        
terminar()