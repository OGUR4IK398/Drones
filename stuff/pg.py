import pygame
import sys

screen = pygame.display.set_mode((800, 600))

r = pygame.Rect(0, 0, 800, 600)
pygame.draw.rect(screen, (255, 255, 255), r, 0)

size = 20

c = 0

font = pygame.font.SysFont('couriernew', 40)
text = font.render(str('Hello'), True, (0, 0, 0))
screen.blit(text, (50, 50))

for j in range(600//size):
    for i in range(800//size):
        r = pygame.Rect(size * i, size * j, size, size)
        if j % 2 == 0:
            if i % 2 == 0:
                pygame.draw.rect(screen, (0, 255, 255), r, 0)
            else:
                pygame.draw.rect(screen, (255, 0, 255), r, 0)
        else:
            if i % 2 == 0:
                pygame.draw.rect(screen, (255, 0, 255), r, 0)
            else:
                pygame.draw.rect(screen, (0, 255, 255), r, 0)
        c += 1


while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
    pygame.display.flip()