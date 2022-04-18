from typing import Any

import pygame
import random

pygame.init()

display_width = 1600
display_height = 900

black = (0, 0, 0)
white = (255, 255, 255)

red = (200, 0, 0)
green = (0, 200, 0)

block_color = (225, 225, 255)
cesta = pygame.Surface((800, 900))
trava = pygame.Surface((1600, 900))
trava.fill('dark green')
cesta.fill('grey')
pocetna = pygame.image.load('pocetnaa.png')

car_width = 73

game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('utrkivać')
clock = pygame.time.Clock()

car_img = pygame.image.load('avto.png')
gameIcon = pygame.image.load('pocetnaa.png')

mud = pygame.image.load('mud.png')
mud = pygame.transform.scale(mud, (200, 200))
rock = pygame.image.load('rock.png')
rock = pygame.transform.scale(rock, (200, 200))
water = pygame.image.load('water.png')
water = pygame.transform.scale(water, (200, 200))
dugme = pygame.image.load('undo.png')
dugme = pygame.transform.scale(dugme, (300, 300))

L = [mud, rock, water]

pygame.display.set_icon(gameIcon)
pause = False

# REGISTER USER EVENTS
OBSTACLE_DODGED = pygame.USEREVENT + 1


class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self) -> None:
        game_display.blit(self.image, self.rect.topleft)


class Car(pygame.sprite.Sprite):
    def __init__(self, image, car_h, car_w, starting_pos_x, starting_pos_y):
        super().__init__()
        self.image = image
        self.height = car_h
        self.width = car_w
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.start_pos_x = starting_pos_x
        self.start_pos_y = starting_pos_y
        self.rect = pygame.Rect(self.start_pos_x, self.start_pos_y, self.width, self.height)
        self.rect = self.rect.inflate(-20, -10)
        # change this to alter car speed
        self.velocity = 3

    def update(self, *args: Any, **kwargs: Any) -> None:
        # handle crash
        if self.rect.x > 1050 or self.rect.x < 350:
            crash()
            self.kill()

    def handle_movement(self, keys_pressed):
        if keys_pressed[pygame.K_LEFT] and self.rect.x - self.velocity > 0:
            self.rect.x -= self.velocity

        if keys_pressed[pygame.K_RIGHT] and self.rect.x + self.velocity + self.height < display_width:
            self.rect.x += self.velocity


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image, obstacle_h, obstacle_w, starting_pos_x, movement_multiplier: float):
        super().__init__()
        self.starting_pos_y = -600
        self.starting_pos_x = starting_pos_x
        self.image = image
        self.height = obstacle_h
        self.width = obstacle_w
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = pygame.Rect(self.starting_pos_x, self.starting_pos_y, self.width, self.height)
        self.multi = movement_multiplier

    def update(self, *args: Any, **kwargs: Any) -> None:
        # move the obstacle
        self.rect.y += 3 * self.multi

        # handle obstacle "dodge"
        if self.rect.y > display_height:
            print("dodged")
            pygame.event.post(pygame.event.Event(OBSTACLE_DODGED))
            self.kill()


def display_score(count):
    font = pygame.font.SysFont("comicsansms", 25)
    text = font.render("Bodovi: " + str(count), True, white)
    game_display.blit(text, (1400, 0))


def text_objects(text, font):
    text_surface = font.render(text, True, white)
    return text_surface, text_surface.get_rect()


def crash():
    large_text = pygame.font.SysFont("comicsansms", 115)
    text_surf, text_rect = text_objects("Izgubio si", large_text)
    text_rect.center = ((display_width / 2), (display_height / 2))
    game_display.blit(text_surf, text_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        button("IGRAJ PONOVNO", 350, 600, 250, 100, 'green', 'lime', game_loop)
        button("IZAĐI", 1000, 600, 250, 100, 'red', 'pink', game_intro)

        pygame.display.update()
        clock.tick(15)


def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(game_display, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(game_display, ic, (x, y, w, h))
    small_text = pygame.font.SysFont("comicsansms", 20)
    text_surf, text_rect = text_objects(msg, small_text)
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    game_display.blit(text_surf, text_rect)


def quit_game():
    pygame.quit()
    quit()


def unpause():
    global pause
    pause = False


def paused():
    large_text = pygame.font.SysFont("comicsansms", 115)
    text_surf, text_rect = text_objects("Pauzirano", large_text)
    text_rect.center = ((display_width / 2), (display_height / 2))
    game_display.blit(text_surf, text_rect)

    while pause:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        button("NASTAVI", 350, 600, 250, 100, 'green', 'lime', unpause)
        button("ODUSTANI", 1000, 600, 250, 100, 'red', 'pink', game_intro)

        pygame.display.update()
        clock.tick(15)


def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        game_display.blit(pocetna, (0, 0))
        large_text = pygame.font.SysFont("comicsansms", 115)
        text_surf, text_rect = text_objects("UTRKA", large_text)
        text_rect.center = ((display_width / 2), (display_height / 2))
        game_display.blit(text_surf, text_rect)

        button("START!", 350, 600, 250, 100, 'green', 'lime', game_loop)
        button("IZAĐI", 1000, 600, 250, 100, 'red', 'pink', quit_game)

        pygame.display.update()
        clock.tick(15)


def draw_background():
    game_display.blit(trava, (0, 0))
    game_display.blit(cesta, (400, 0))


def spawn_obstacle(speed_multiplier) -> Obstacle:
    obstacle_start_x = random.randrange(500, 1100)
    obstacle_width = 100
    obstacle_height = 100
    obstacle_img = random.randint(0, 2)
    if obstacle_img == 0:
        obstacle_img = mud
    elif obstacle_img == 1:
        obstacle_img = water
    else:
        obstacle_img = rock
    return Obstacle(image=obstacle_img,
                    obstacle_h=obstacle_height,
                    obstacle_w=obstacle_width,
                    starting_pos_x=obstacle_start_x,
                    movement_multiplier=speed_multiplier
                    )


def game_loop():
    global pause

    # init relevant vars
    game_exit = False
    obstacles_dodged = 0

    # control group for handling all sprite behavior
    all_sprites = pygame.sprite.Group()
    # obstacle group for handling car - obstacle collision
    obstacle_sprites = pygame.sprite.Group()

    # create a car obj
    car_obj = Car(image=car_img,
                  car_h=300,  # hardcoded value, change if necessary
                  car_w=200,  # -||-
                  starting_pos_x=(display_width * 0.42),
                  starting_pos_y=(display_height * 0.7)
                  )
    all_sprites.add(car_obj)

    # create an initial obstacle obj.
    speed_multiplier = 1.0
    obstacle_obj = spawn_obstacle(speed_multiplier)
    all_sprites.add(obstacle_obj)
    obstacle_sprites.add(obstacle_obj)

    # button
    button_back = Button(0, 0, dugme, 0.5)

    while not game_exit:

        mouse_coordinates = pygame.mouse.get_pos()
        # EVENT LOOP
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # obstacle is dodged
            if event.type == OBSTACLE_DODGED:
                obstacles_dodged += 1
                speed_multiplier += 0.25 if speed_multiplier < 6 else 0
                obstacle_obj = spawn_obstacle(speed_multiplier)
                all_sprites.add(obstacle_obj)
                obstacle_sprites.add(obstacle_obj)
                # slightly increase car speed every 2 dodges
                # but not higher than 4
                if obstacles_dodged % 2 == 0 and car_obj.velocity < 4:
                    car_obj.velocity += 0.20

            if event.type == pygame.KEYDOWN:
                # handle pause click
                if event.key == pygame.K_p:
                    pause = True
                    paused()
            # handle mouse click

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_back.rect.collidepoint(mouse_coordinates):
                    game_intro()

        # draw relevant UI
        draw_background()
        display_score(obstacles_dodged)
        button_back.draw()
        # REMOVE THIS
        pygame.draw.rect(game_display, "RED", car_obj.rect)
        pygame.draw.rect(game_display, "RED", obstacle_obj.rect)

        # handle all sprites
        all_sprites.update()
        all_sprites.draw(game_display)

        # handle the car
        keys_pressed = pygame.key.get_pressed()
        car_obj.handle_movement(keys_pressed)

        # handle car crash
        if pygame.sprite.spritecollideany(car_obj, obstacle_sprites):
            crash()

        pygame.display.update()
        clock.tick(60)


game_intro()
game_loop()
pygame.quit()
quit()

# ne radi umiranje kad se zabije u prepreku
# auto se kreće čudno
# button za nazad šteka
