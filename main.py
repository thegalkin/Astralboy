import pygame
from math import atan2, pi, sin, cos, radians
from random import randint
from time import time, sleep

pygame.init()

display_width = 800 #ширина игровой области
display_height = 600 #высота игровой области
display = pygame.display.set_mode((display_width, display_height))#создаем дисплей
pygame.display.set_caption("Astralboy")#устанавливаем заголовок окна 

clock = pygame.time.Clock()#запускаем внутриигровые часы
#Блок с загрузкой из памяти игровых изображений 
shipOn = pygame.transform.scale(pygame.image.load("static/spaceship_on.png"), (70, 90))
shipOff = pygame.transform.scale(pygame.image.load("static/spaceship_off.png"), (70, 90))
missileImg = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("static/missile.png"), (20, 40)), -90)
asteroidImage = pygame.image.load("static/asteroid.png")
background = pygame.image.load("static/background.png").convert()
explosion_image_list = [pygame.image.load("static/explosion/regularExplosion0{}.png".format(i)) for i in range(9)]
crosshairsImage = pygame.transform.scale(pygame.image.load("static/crosshairs.png"), (90, 90))
font = pygame.font.Font("static/font.ttf", 20)


#блок с глобальными переменными
ship_acceleration = 2#ускорение корабля
x_bg = 0#положение фона по х
angle = -90#угол поворота корабля
shot = False
shot_speed = 10#скорость полета ракеты
engine_on = False#состояние двигателя
shots_list = []#список ракет на экране
asteroids_list = [] #список астероидов на экране
exsplosions_list = []#список взрывов на экране

asteroids_spawn_areaSize = 100.0 #размер зоны для появляения астероидов
asteroids_speed = 1 #скорость астероидов
asteroids_amount = 10 #кол-во астероидов 
asteroids_time = 5 #скорость появления астероидов
explosion_time = 0.05 #скорость анимации взрыва
user_score = 0 #кол-во очков игрока
user_lives = 5 #кол-во жизней игрока


class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.engine = False
        self.image_orig = shipOff
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.x = display_width / 2
        self.rect.y = display_height / 2
        self.angle = -90

    def update(self):
        if self.engine:
            self.image_orig = shipOn
        else:
            self.image_orig = shipOff

        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]
        self.angle = (180 / pi) * atan2(self.rect.centerx - mouseX, self.rect.centery - mouseY)
        new_image = pygame.transform.rotate(self.image_orig, self.angle)
        old_center = self.rect.center

        self.image = new_image
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        if self.rect.x > 5:
            self.rect.x -= ship_acceleration


ship = Ship()
ship_group = pygame.sprite.Group()
ship_group.add(ship)

missile_group = pygame.sprite.Group()


def run():
    global shot, shipOn, x_bg, angle, font, user_score, user_lives
    game = True

    w_pressed = False
    s_pressed = False
    d_pressed = False
    mouse_move = False
    start = False
    angle = -90
    crosshairs = CrossHairs(0, 0)
    asteroids_previous = 0
    explosion_previous = 0

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
                    missile = Missile()
                    missile_group.add(missile)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    w_pressed = False
                if event.key == pygame.K_s:
                    s_pressed = False
                if event.key == pygame.K_d:
                    d_pressed = False
            if event.type == pygame.MOUSEBUTTONUP:
                mouseX = pygame.mouse.get_pos()[0]
                mouseY = pygame.mouse.get_pos()[1]
                if 200 < mouseX < 600 and 150 < mouseY < 450:
                    start = True

        if w_pressed:
            if ship.rect.y < -70:
                ship.rect.y = 525
            else:
                ship.rect.y -= 5
        if s_pressed:
            if ship.rect.y > 600:
                ship.rect.y = 0
            else:
                ship.rect.y += 5
        if d_pressed:
            if ship.rect.x <= 680:
                ship.engine = True
                ship.rect.x += 5
        else:
            ship.engine = False

        if start:
            moveBg()
            ship_group.draw(display)
            ship_group.update()
            missile_group.draw(display)
            missile_group.update()

            for asteroidI in asteroids_list:
                asteroidI.move()
                asteroidI.rollnrock()
            # for shot in shots_list:
            #     shot.move()
            if len(asteroids_list) > 0:
                if time() - explosion_previous >= explosion_time:
                    explosion_previous = time()
                    for explosion in exsplosions_list:
                        explosion.move()
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

        pygame.display.flip()
        clock.tick(60)


def moveBg():
    global x_bg
    rel_x = x_bg % background.get_rect().width
    display.blit(background, (rel_x - background.get_rect().width, 0))
    if rel_x < display_width:
        display.blit(background, (rel_x, 0))
    x_bg -= 5


def bake_asteroid(angle, scaleSquare):
    return pygame.transform.rotate(pygame.transform.scale(asteroidImage, (scaleSquare, scaleSquare)), -angle)


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
        if self.x - self.scale * 0.5 < ship.rect.centerx < self.x + self.scale * 0.5 and self.y - self.scale * 0.5 < ship.rect.centery < self.y + self.scale * 0.5:
            user_lives -= 1
            explosion = Explosion(self.x, self.y, self.scale)
            asteroids_list.remove(self)
            del self

    def rollnrock(self):
        if self.rollDirection == 1:
            self.angle = self.angle + self.rollSpeed
            display.blit(bake_asteroid(self.angle, self.scale), (self.x, self.y))
        else:
            self.angle = self.angle - self.rollSpeed
            display.blit(bake_asteroid(self.angle, self.scale), (self.x, self.y))


class Explosion:
    def __init__(self, x, y, scale):
        self.x = x
        self.y = y
        self.stage = 0
        self.maxStage = 8
        self.scale = scale
        exsplosions_list.append(self)

    def move(self):
        if self.stage < 9:
            display.blit(pygame.transform.scale(explosion_image_list[self.stage], (self.scale, self.scale)), (self.x, self.y))
            self.stage += 1 
        else:
            exsplosions_list.remove(self)
    

class Missile(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.angle = ship.angle + 90
        self.image_orig = pygame.transform.rotate(missileImg, self.angle)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.centerx = ship.rect.centerx
        self.rect.centery = ship.rect.centery
        self.life = 500
        shots_list.append(self)

    def update(self):
        if 0 < self.rect.x < display_width or 0 < self.rect.y < display_height:
            self.rect.x += int((shot_speed * cos(radians(self.angle))))
            self.rect.y -= int((shot_speed * sin(radians(self.angle))))
        else:
            missile_group.remove(self)
        self.move()

    def move(self):
        global user_score
        for i in range(len(asteroids_list)):
            if asteroids_list[i].x - asteroids_list[i].scale * 0.5 < self.rect.x < asteroids_list[i].x + asteroids_list[
                i].scale * 0.5 and asteroids_list[i].y - asteroids_list[i].scale * 0.5 < self.rect.y < asteroids_list[i].y + \
                    asteroids_list[i].scale * 0.5:
                explosion = Explosion(self.rect.x, self.rect.y, asteroids_list[i].scale)
                del asteroids_list[i]
                user_score += 1
                missile_group.remove(self)
                break
        self.life -= 10

        try:
            if self.life <= 0:
                missile_group.remove(self)
        except ValueError:
            pass


run()
