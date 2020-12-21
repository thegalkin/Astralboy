import pygame
from math import atan2, pi, sin, cos, radians
from random import randint
from time import time, sleep

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
background = pygame.image.load("static/background.png").convert()

crosshairsImage = pygame.transform.scale(pygame.image.load("static/crosshairs.png"), (90, 90))

x_ship = display_width / 2
y_ship = display_height / 2
ship_acceleration = 2
x_shot = 0
y_shot = 0
x_bg = 0
angle = -90
shot = False
shot_speed = 10
engine_on = False
shots_list = []
asteroids_list = []
asteroids_objects = []

asteroids_spawn_areaSize = 100.0
asteroids_speed = 1
asteroids_amount = 10
asteroids_time = 5
user_score = 0
user_lives = 5

font = pygame.font.Font("static/font.ttf", 20)


def run():
    global x_ship, y_ship, x_shot, y_shot, shot, shipOn, x_bg, angle, font, user_score, user_lives
    game = True

    w_pressed = False
    s_pressed = False
    d_pressed = False
    mouse_move = False
    start = False
    ang = -90
    angle = -90
    crosshairs = CrossHairs(0, 0)
    asteroids_previous = 0

    while game:
        global engine_on
        if time() - asteroids_previous >= asteroids_time:
            asteroids_previous = time()
            for i in range(randint(1, 10)):
                Asteroid(randint(display_width, display_width + asteroids_spawn_areaSize),
                         randint(-asteroids_spawn_areaSize, display_height + asteroids_spawn_areaSize))
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
                    Missile(x_ship + 80, y_ship + 25, angle)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    w_pressed = False
                if event.key == pygame.K_s:
                    s_pressed = False
                if event.key == pygame.K_d:
                    d_pressed = False
            if event.type == pygame.MOUSEMOTION:
                mouseX = pygame.mouse.get_pos()[0]
                mouseY = pygame.mouse.get_pos()[1]-35
                angle = ang = (180 / pi) * atan2(x_ship - mouseX, y_ship - mouseY)
                crosshairs.move(mouseX, mouseY)
                mouse_move = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouseX = pygame.mouse.get_pos()[0]
                mouseY = pygame.mouse.get_pos()[1]
                if 200 < mouseX < 600 and 150 < mouseY < 450:
                    start = True

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

        if x_ship > 0:
            x_ship -= ship_acceleration

        if start:
            moveBg()

            ship = Ship(x_ship, y_ship, engine_on, ang)
            ship.move()
            # moveShip(ang)



            for asteroidI in asteroids_list:
                asteroidI.move()
                asteroidI.rollnrock()
            for shot in shots_list:
                shot.move()
            score = font.render("Score: " + str(user_score), True, (255, 0, 0))
            display.blit(score, (600, 20))
            lives = font.render("Lives: " + str(user_lives), True, (255, 0, 0))
            display.blit(lives, (200, 20))
        else:
            display.blit(background, (0, 0))
            for asteroidI in asteroids_list:
                asteroidI.move()
                asteroidI.rollnrock()
            s = pygame.Surface((400, 300), pygame.SRCALPHA)
            s.fill((34, 36, 98, 128))
            display.blit(s, (200, 150))
            menu = pygame.image.load("static/menu.png")
            display.blit(menu, (200, 150))
            score = font.render("Score: " + str(user_score), True, (255, 0, 0))
            display.blit(score, (600, 20))
            lives = font.render("Lives: " + str(user_lives), True, (255, 0, 0))
            display.blit(lives, (200, 20))

        pygame.display.update()
        clock.tick(60)


def moveShip(ang):
    if engine_on:
        display.blit(pygame.transform.rotate(shipOn, ang), (x_ship, y_ship))
    else:
        display.blit(pygame.transform.rotate(shipOff, ang), (x_ship, y_ship))


def moveBg():
    global x_bg
    rel_x = x_bg % background.get_rect().width
    display.blit(background, (rel_x - background.get_rect().width, 0))
    if rel_x < display_width:
        display.blit(background, (rel_x, 0))
    x_bg -= 5


def bake_asteroid(angle, scaleSquare):
    return pygame.transform.rotate(pygame.transform.scale(asteroidImage, (scaleSquare, scaleSquare)), -angle)


class Ship:
    def __init__(self, x, y, engine, angle):
        self.x = x
        self.y = y
        self.engine = engine
        self.angle = angle
        if self.engine:
            self.img = pygame.transform.rotate(shipOn, self.angle)
            self.rect = self.img.get_rect()
            self.rect.center = (45, 35)
        else:
            self.img = pygame.transform.rotate(shipOff, self.angle)
            self.rect = self.img.get_rect()
            self.rect.center = (45, 35)
        # print(self.rect.x, self.rect.y)
        print(self.rect.y)


    def move(self):
        if self.engine:
            # print(pygame.transform.rotate(shipOn, self.angle).get_rect().center)
            img = pygame.transform.rotate(shipOn, self.angle)
            img.get_rect().center = (45, 35)
            bl = display.blit(self.img, (self.x, self.y))




        else:
            # print(pygame.transform.rotate(shipOn, self.angle).get_rect().center)
            img = pygame.transform.rotate(shipOff, self.angle)
            img.get_rect().center = (45, 35)
            bl = display.blit(self.img, (self.x, self.y))



class CrossHairs:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, x, y):
        self.x = x
        self.y = y
        display.blit(crosshairsImage, (self.x, self.y))


class Asteroid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        asteroids_list.append(self)
        self.angle = randint(0, 90)
        self.scale = randint(10, 150)
        self.speed = randint(1, 5)
        self.rollSpeed = randint(10, 20)
        self.rollDirection = randint(0, 1)

    def move(self):
        global user_lives
        if -asteroids_spawn_areaSize < self.x:  # < display_width+asteroids_spawn_areaSize or asteroids_spawn_areaSize
            # < self.y < display_height+asteroids_spawn_areaSize:
            display.blit(bake_asteroid(self.angle, self.scale), (self.x, self.y))
            self.x -= asteroids_speed
        else:
            asteroids_list.remove(self)
        if self.x - self.scale * 0.5 < x_ship < self.x + self.scale * 0.5 and self.y - self.scale * 0.5 < y_ship < self.y + self.scale * 0.5:
            user_lives -= 1
            asteroids_list.remove(self)

    def rollnrock(self):
        if self.rollDirection == 1:
            self.angle = self.angle + self.rollSpeed
            display.blit(bake_asteroid(self.angle, self.scale), (self.x, self.y))
        else:
            self.angle = self.angle - self.rollSpeed
            display.blit(bake_asteroid(self.angle, self.scale), (self.x, self.y))

class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.stage = 0
        self.maxStage = 8
    def move(self):
        if self.stage < 9:
            display.blit(pygame.image.load("static/explosion/regularExplosion0{}.png".format(self.stage)), (self.x, self.y))
    def animation(self):
        for i in range(9):
            sleep(0.1)
            self.move()


class Missile:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        shots_list.append(self)
        self.angle = angle + 90
        self.life = 500

    def move(self):
        global user_score
        if 0 < self.x < display_width or 0 < self.y < display_height:
            display.blit(pygame.transform.rotate(missile, self.angle), (self.x, self.y))
            self.x += int((shot_speed * cos(radians(self.angle))))
            self.y -= int((shot_speed * sin(radians(self.angle))))
        else:
            shots_list.remove(self)
        for i in range(len(asteroids_list)):
            if asteroids_list[i].x - asteroids_list[i].scale * 0.5 < self.x < asteroids_list[i].x + asteroids_list[
                i].scale * 0.5 and asteroids_list[i].y - asteroids_list[i].scale * 0.5 < self.y < asteroids_list[i].y + \
                    asteroids_list[i].scale * 0.5:
                explosion = Explosion(self.x, self.y)
                explosion.animation()
                del asteroids_list[i]
                user_score += 1
                shots_list.remove(self) 
                break
        self.life -= 10

        # изредка программа ломалась на этом моменте
        # видимо если ракета уже удалилась например из-за астероида, а мы ее пытаемся удалить еще раз
        # дима не может, try except поможет
        try:
            if self.life <= 0:
                shots_list.remove(self)
        except ValueError:
            pass


run()
