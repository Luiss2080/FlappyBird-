import pygame
import sys
import time
import random
import os
from pygame.locals import *

pygame.init()
ancho = 500
alto = 700
superficie_juego = pygame.display.set_mode((ancho, alto))

imagen_fondo = pygame.image.load(os.path.dirname(__file__)+"./Imagenes/FondoVioleta.png")
imagen_pajaro = pygame.image.load(os.path.dirname(__file__)+"./Imagenes/bird.png")
tubo_superior = pygame.image.load(os.path.dirname(__file__)+"./Imagenes/pipe_top.png")
tubo_inferior = pygame.image.load(os.path.dirname(__file__)+"./Imagenes/pipe_bot.png")
imagen_corazon = pygame.image.load(os.path.dirname(__file__)+"./Imagenes/Corazones.png")
fps = pygame.time.Clock()

# Sonidos
pygame.mixer.init()
sonido_salto = pygame.mixer.Sound(os.path.dirname(__file__)+"./Imagenes/Sonidos/Salto.wav")
sonido_pasar_obstaculo = pygame.mixer.Sound(os.path.dirname(__file__)+"./Imagenes/Sonidos/PasarObstaculo.wav")
sonido_fallo_obstaculo = pygame.mixer.Sound(os.path.dirname(__file__)+"./Imagenes/Sonidos/Colision.wav")
musica_fondo = pygame.mixer.music.load(os.path.dirname(__file__)+"./Imagenes/Sonidos/FondoAmarillo.mp3")
pygame.mixer.music.play(-1)  # Repetir música de fondo


# Función para obtener altura aleatoria para el tubo
def obtener_altura_tubo():
    altura_tubo = [random.randint(200, int(alto / 2) - 20), random.randint(int(alto / 2) + 20, alto - 200)]
    return altura_tubo

# Función para verificar colisión con el tubo
def colision_tubo(posicion_tubo, ancho_tubo, altura_tubo, posicion_pajaro):
    rect_pajaro = pygame.Rect(posicion_pajaro[0], posicion_pajaro[1], 34, 24)

    # Verificar colisión con el tubo superior
    rect_tubo_superior = pygame.Rect(posicion_tubo, -altura_tubo[0], ancho_tubo, altura_tubo[0])
    mask_pajaro = pygame.mask.from_surface(imagen_pajaro)
    mask_tubo_superior = pygame.mask.from_surface(tubo_superior)

    offset = (int(rect_tubo_superior.x - rect_pajaro.x), int(rect_tubo_superior.y - rect_pajaro.y))
    result = mask_pajaro.overlap(mask_tubo_superior, offset)

    if result is not None:
        return True

    # Verificar colisión con el tubo inferior
    rect_tubo_inferior = pygame.Rect(posicion_tubo, altura_tubo[1], ancho_tubo, alto - altura_tubo[1])
    mask_tubo_inferior = pygame.mask.from_surface(tubo_inferior)

    offset = (int(rect_tubo_inferior.x - rect_pajaro.x), int(rect_tubo_inferior.y - rect_pajaro.y))
    result = mask_pajaro.overlap(mask_tubo_inferior, offset)

    if result is not None:
        return True

    return False

def main():
    puntaje = 0
    vidas = 3  # Número inicial de vidas
    tiempo_inicio = pygame.time.get_ticks()  # Tiempo de inicio del juego
    posicion_pajaro = [100, 350]
    gravedad = 1
    velocidad = 0
    salto = -30
    colision_activada = False  # Variable para asegurarse de que la colisión se cuente una vez

    # tubo
    posicion_tubo = 700
    ancho_tubo = 50
    altura_tubo = obtener_altura_tubo()

    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    velocidad += salto
                    sonido_salto.play()

        # Fuerza hacia abajo
        velocidad += gravedad
        velocidad *= 0.95
        posicion_pajaro[1] += velocidad

        # tubo
        if posicion_tubo >= -20:
            posicion_tubo -= 10
        else:
            posicion_tubo = 700
            altura_tubo = obtener_altura_tubo()
            puntaje += 1
            sonido_pasar_obstaculo.play()
            colision_activada = False  # Reiniciar la variable de colisión al pasar un tubo

        # Superficie
        superficie_juego.blit(imagen_fondo, [0, 0])

        # Dibujar tubo
        superficie_juego.blit(tubo_superior, (posicion_tubo, -altura_tubo[0]))
        superficie_juego.blit(tubo_inferior, (posicion_tubo, altura_tubo[1]))

        # Dibujar pájaro
        superficie_juego.blit(imagen_pajaro, (int(posicion_pajaro[0]), int(posicion_pajaro[1])))

        # Colisión
        if colision_tubo(posicion_tubo, ancho_tubo, altura_tubo, posicion_pajaro) and not colision_activada:
            sonido_fallo_obstaculo.play()
            vidas -= 1  # Restar una vida
            colision_activada = True  # Evitar que la colisión se cuente múltiples veces
            print(f"¡Colisión! Vidas restantes: {vidas}")

            if vidas == 0:
                print(f"¡Fin del juego! Puntaje final: {puntaje}")
                ejecutando = False

        # Bordes
        if posicion_pajaro[1] >= alto:
            posicion_pajaro[1] = alto
            velocidad = 0
        elif posicion_pajaro[1] <= 0:
            posicion_pajaro[1] = 0
            velocidad = 0

        # Mostrar cronómetro
        tiempo_transcurrido = (pygame.time.get_ticks() - tiempo_inicio) // 1000  # Convertir a segundos
        fuente = pygame.font.Font(None, 36)
        texto_tiempo = fuente.render(f"Tiempo: {tiempo_transcurrido}s", True, (255, 255, 255))
        superficie_juego.blit(texto_tiempo, (10, 10))

        # Mostrar vidas
        corazon_size = 15
        for i in range(vidas):
            corazon_pequeno = pygame.transform.scale(imagen_corazon, (corazon_size, corazon_size))
            superficie_juego.blit(corazon_pequeno, (ancho - 30 - i * (corazon_size + 5), 10))

        pygame.display.flip()
        fps.tick(25)

    pygame.quit()

main()
