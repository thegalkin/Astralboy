import pygame
from math import atan2, pi
from random import randint
pygame.init()

display_width = 800
display_height = 600

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Astralboy")

clock = pygame.time.Clock()

shipOn = pygame.transform.scale(pygame.image.load("static/spaceship_on.png"), (70, 90))
shipOff = pygame.transform.scale(pygame.image.load("static/spaceship_off.png"), (70, 90))
missile = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("static/missile.png"), (20, 40)), -90)
asteroidImage = pygame.image.load("static/asteroid.png")

def bake_asteroid(angle, scaleSquare):
    return pygame.transform.rotate(pygame.transform.scale(asteroidImage, (scaleSquare, scaleSquare)), -angle)


x_ship = display_width/2
y_ship = display_height/2
ship_acceleration = 2
x_shot = 0
y_shot = 0
shot = False
engine_on = False
shots_list = []
asteroids_list = []
asteroids_objects = []

asteroids_spawn_areaSize = 100.0
asteroids_speed = 1
asteroids_amount = 10

def run():
    global x_ship, y_ship, x_shot, y_shot, shot, shipOn
    game = True

    w_pressed = False
    s_pressed = False
    d_pressed = False
    for i in range(asteroids_amount):
            Asteroid(randint(display_width, display_width+asteroids_spawn_areaSize), randint(-asteroids_spawn_areaSize, display_height+asteroids_spawn_areaSize))
    while game:
        global engine_on
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    w_pressed = True
                if event.key == pygame.K_s:
                    s_pressed = True
                if event.key == pygame.K_d:
                    d_pressed = True
                if event.key == pygame.K_SPACE:
                    Missile(x_ship + 80, y_ship + 25)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    w_pressed = False
                if event.key == pygame.K_s:
                    s_pressed = False
                if event.key == pygame.K_d:
                    d_pressed = False
            if event.type == pygame.MOUSEMOTION:
                engine_on = True
                mouseX = pygame.mouse.get_pos()[0]
                mouseY = pygame.mouse.get_pos()[1]
                angle = angle = (180 / pi) * atan2(x_ship - mouseX, y_ship - mouseY) 
                # print(angle)
                
                
                display.blit(pygame.transform.rotate(shipOn, int(angle)),shipOn.get_rect(center=(x_ship,y_ship))) #I need space_ship to rotate towards my cursor
                pygame.display.update()
                clock.tick(60)
            else: 
                engine_on = False


        if w_pressed:
            if y_ship < -70:
                y_ship = 525
            else:
                y_ship -= 5
        if s_pressed:
            if y_ship > 600:
                y_ship = 0
            else:
                y_ship += 5
        if d_pressed:
            if x_ship <= 680:
                engine_on = True
                x_ship += 5
        else:
            engine_on = False

        display.fill((255, 255, 255))
        moveShip()
        for shot in shots_list:
            shot.move()

        # display.blit(asteroid, (100, 100))


        if x_ship > 0:
            x_ship -= ship_acceleration
        
        for asteroidI in asteroids_list:
            asteroidI.move()    
        pygame.display.update()
        clock.tick(60)


def moveShip():
    global engine_on
    if engine_on:
        display.blit(shipOn, (x_ship, y_ship))
    else:
        display.blit(shipOff, (x_ship, y_ship))

class Asteroid:
    def __init__(self, x, y):
            self.x = x
            self.y = y
            asteroids_list.append(self)
            self.angle = randint(0,90)
            self.scale = randint(10,150)
            
    def move(self):
        if -asteroids_spawn_areaSize < self.x: # < display_width+asteroids_spawn_areaSize or asteroids_spawn_areaSize < self.y < display_height+asteroids_spawn_areaSize:
            display.blit(bake_asteroid(self.angle, self.scale), (self.x, self.y))
            self.x -= asteroids_speed
        else:
            asteroids_list.remove(self)


    
class Missile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        shots_list.append(self)

    def move(self):
        if 0 < self.x < display_width or 0 < self.y < display_height:
            display.blit(missile, (self.x, self.y))
            self.x += 10
        else:
            shots_list.remove(self)


run()
