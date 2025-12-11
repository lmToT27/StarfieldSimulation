import pygame
import random
from Config import *

class star_t:
    def __init__(self):
       self.x = random.uniform(-SCREEN_WIDTH, SCREEN_WIDTH)
       self.y = random.uniform(-SCREEN_HEIGHT, SCREEN_HEIGHT)
       self.z = random.uniform(1, MAX_DEPTH)
       self.old_z = self.z

    def Reset(self):
       self.x = random.uniform(-SCREEN_WIDTH, SCREEN_WIDTH)
       self.y = random.uniform(-SCREEN_HEIGHT, SCREEN_HEIGHT)
       self.z = MAX_DEPTH 
       self.old_z = self.z
    
    def Update(self, dt):
        self.old_z = self.z
        self.z -= SPEED * dt
        if self.z < 1:
            self.Reset()


    def Draw(self, surface, offsetx, offsety):
        old_x = self.x / self.old_z * FOV + offsetx
        old_y = self.y / self.old_z * FOV + offsety

        x = self.x / self.z * FOV + offsetx 
        y = self.y / self.z * FOV + offsety 

        radius = (1 - self.z / SCREEN_WIDTH) * 4
        radius = int(radius)
        if radius < 1: radius = 1

        pygame.draw.line(surface, "#FFFFFF", (x, y), (old_x, old_y), radius)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Starfield Simulation - by lmToT27")
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

star_list = [star_t() for _ in range(STAR_AMOUNT)]

running = True

while running:
    dt = clock.tick(120) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mx, my = pygame.mouse.get_pos()

    screen.fill("#000000")
    for star in star_list:
        star.Update(dt)
        star.Draw(screen, mx, my)
    pygame.display.flip()

pygame.quit()