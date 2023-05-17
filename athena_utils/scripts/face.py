import pygame
import pygame_gui
import time
import random

pygame.init()

screen = (1024, 600)

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode(screen , pygame.FULLSCREEN)

background = pygame.Surface(screen)
background.fill(pygame.Color('#000000'))

manager = pygame_gui.UIManager(screen)

feliz_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 10), (100, 50)),
                                            text='FELIZ',
                                            manager=manager)

triste_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((120, 10), (100, 50)),
                                            text='TRISTE',
                                            manager=manager)



########
white = (255, 255, 255)
black = (0, 0, 0)
eye_radius = 50
pupil_radius = 20
# Define a posição dos olhos
left_eye_pos = (screen[0] // 3, screen[1] // 2)
right_eye_pos = (screen[0] * 2 // 3, screen[1] // 2)

# Cria os olhos
left_eye = pygame.draw.circle(window_surface, white, left_eye_pos, eye_radius)
right_eye = pygame.draw.circle(window_surface, white, right_eye_pos, eye_radius)

# Define as emoções
neutral = (0, 0)
happy = (-10, -10)
sad = (10, 10)

# Define a posição das pupilas
left_pupil_pos = left_eye_pos
right_pupil_pos = right_eye_pos

# Cria as pupilas
left_pupil = pygame.draw.circle(window_surface, black, left_pupil_pos, pupil_radius)
right_pupil = pygame.draw.circle(window_surface, black, right_pupil_pos, pupil_radius)


# Define a função que atualiza as emoções dos olhos
def update_eyes(emotion):
    global left_pupil_pos, right_pupil_pos

    if emotion == 'close':
        left_eye = pygame.draw.circle(window_surface, black, left_eye_pos, eye_radius)
        right_eye = pygame.draw.circle(window_surface, black, right_eye_pos, eye_radius)
        return None

    elif emotion == 'neutral':
        left_eye = pygame.draw.circle(window_surface, white, left_eye_pos, eye_radius)
        right_eye = pygame.draw.circle(window_surface, white, right_eye_pos, eye_radius)

    elif emotion == 'happy':
        left_eye = pygame.draw.circle(window_surface, white, left_eye_pos, eye_radius)
        right_eye = pygame.draw.circle(window_surface, white, right_eye_pos, eye_radius)

        left_eye_pos2 = tuple(x + y for x, y in zip(left_eye_pos, (0, 30)))
        right_eye_pos2 = tuple(x + y for x, y in zip(right_eye_pos, (0, 30)))

        left_eye2 = pygame.draw.circle(window_surface, black, left_eye_pos2, eye_radius)
        right_eye2 = pygame.draw.circle(window_surface, black, right_eye_pos2, eye_radius)

    elif emotion == 'sad':
        left_eye = pygame.draw.circle(window_surface, white, left_eye_pos, eye_radius)
        right_eye = pygame.draw.circle(window_surface, white, right_eye_pos, eye_radius)

        left_eye_pos2 = tuple(x + y for x, y in zip(left_eye_pos, (0, -30)))
        right_eye_pos2 = tuple(x + y for x, y in zip(right_eye_pos, (0, -30)))

        left_eye2 = pygame.draw.circle(window_surface, black, left_eye_pos2, eye_radius)
        right_eye2 = pygame.draw.circle(window_surface, black, right_eye_pos2, eye_radius)


#########

clock = pygame.time.Clock()
is_running = True
estado = ''
novoEstado = 'neutral'
update_eyes('neutral')

last = time.time()
emotionTime = 4

while is_running:
    time_delta = clock.tick(60) #/1000.0
    # print('teste', time_delta)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == feliz_button:
                print('FELIZ')
                novoEstado = 'happy'
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == triste_button:
                print('TRISTE')
                novoEstado = 'sad'

        manager.process_events(event)

    if novoEstado != estado:
        estado = novoEstado

    if (estado != neutral) and ((time.time() - last) >= emotionTime):
        estado = 'neutral'
        novoEstado = 'neutral'
        last = time.time()

    # if (estado == 'neutral') and (random.random() >= 0.9991):
    #     estador = 'close'
    #     novoEstado = 'close'
    # else:
    #     estador = 'neutral'
    #     novoEstado = 'neutral'

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))

    # desenha olhos
    # window_surface.blit(background, (0, 0))
    update_eyes(estado)

    manager.draw_ui(window_surface)


    pygame.display.update()
