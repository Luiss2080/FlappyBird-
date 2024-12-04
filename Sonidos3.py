import pygame
import sys
import time
import random
from pygame.locals import *

pygame.init()
width = 500
height = 700
play_surface = pygame.display.set_mode((width, height))
background_image = pygame.image.load("./Imagenes/back.png").convert()
bird_image = pygame.image.load("./Imagenes/bird.png").convert_alpha()
top_pipe = pygame.image.load("./Imagenes/pipe_top.png").convert_alpha()
bot_pipe = pygame.image.load("./Imagenes/pipe_bot.png").convert_alpha()
fps = pygame.time.Clock()

# Sonidos
pygame.mixer.init()
sonido_salto = pygame.mixer.Sound("./Imagenes/Sonidos/Salto.wav")
sonido_pasar_obstaculo = pygame.mixer.Sound("./Imagenes/Sonidos/PasarObstaculo.wav")
sonido_fallo_obstaculo = pygame.mixer.Sound("./Imagenes/Sonidos/Colision.wav")
musica_fondo = pygame.mixer.music.load("./Imagenes/Sonidos/FondoAmarillo.mp3")
pygame.mixer.music.play(-1)  # Repetir música de fondo

# top pipe
def pipe_random_height():
    pipe_h = [random.randint(200, int(height / 2) - 20), random.randint(int(height / 2) + 20, height - 200)]
    return pipe_h

def collision(pipe_pos, pipe_width, pipe_height, player_pos):
    rect_player = pygame.Rect(player_pos[0], player_pos[1], 34, 24)

    # Verificar colisión con el tubo superior
    rect_pipe_top = pygame.Rect(pipe_pos, -pipe_height[0], pipe_width, pipe_height[0])
    mask_player = pygame.mask.from_surface(bird_image)
    mask_pipe_top = pygame.mask.from_surface(top_pipe)

    offset = (int(rect_pipe_top.x - rect_player.x), int(rect_pipe_top.y - rect_player.y))
    result = mask_player.overlap(mask_pipe_top, offset)

    if result is not None:
        return True

    # Verificar colisión con el tubo inferior
    rect_pipe_bot = pygame.Rect(pipe_pos, pipe_height[1], pipe_width, height - pipe_height[1])
    mask_pipe_bot = pygame.mask.from_surface(bot_pipe)

    offset = (int(rect_pipe_bot.x - rect_player.x), int(rect_pipe_bot.y - rect_player.y))
    result = mask_player.overlap(mask_pipe_bot, offset)

    if result is not None:
        return True

    return False

def main():
    score = 0
    player_pos = [100, 350]
    gravity = 1
    speed = 0
    jump = -30

    # pipe
    pipe_pos = 700
    pipe_width = 50
    pipe_height = pipe_random_height()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    speed += jump
                    sonido_salto.play()

        # Down Force
        speed += gravity
        speed *= 0.95
        player_pos[1] += speed

        # pipe
        if pipe_pos >= -20:
            pipe_pos -= 10
        else:
            pipe_pos = 700
            pipe_height = pipe_random_height()
            score += 1
            sonido_pasar_obstaculo.play()

        # Surface
        play_surface.blit(background_image, [0, 0])

        # draw pipe
        play_surface.blit(top_pipe, (pipe_pos, -pipe_height[0]))
        play_surface.blit(bot_pipe, (pipe_pos, pipe_height[1]))

        # player
        play_surface.blit(bird_image, (int(player_pos[0]), int(player_pos[1])))

        # Collision
        if collision(pipe_pos, pipe_width, pipe_height, player_pos):
            print(f"Game Over. Score: {score}")
            sonido_fallo_obstaculo.play()
            run = False

        # Borders
        if player_pos[1] >= height:
            player_pos[1] = height
            speed = 0
        elif player_pos[1] <= 0:
            player_pos[1] = 0
            speed = 0

        pygame.display.flip()
        fps.tick(25)

    pygame.quit()

main()
