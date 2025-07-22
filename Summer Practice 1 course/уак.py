import pygame
import os

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 1000

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tetrizz")

# загрузка фона
try:
    background = pygame.image.load(os.path.join('images', 'bg.jpg'))
    background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))
except pygame.error as e:
    print(f"Ошибка загрузки фона: {e}")
    background = None

# основной цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # отрисовка фона
    if background:
        screen.blit(background, (0, 0))
    else:
        screen.fill((255, 255, 255))  # белый фон если картинка не загрузилась
    
    pygame.display.flip()

pygame.quit()