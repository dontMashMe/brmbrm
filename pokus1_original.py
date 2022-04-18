import pygame
import time
import random

pygame.init()
 
display_width = 1600
display_height = 900
 
black = (0,0,0)
white = (255,255,255)

red = (200,0,0)
green = (0,200,0)
 
block_color = (225,225,255)
cesta=pygame.Surface((800,900))
trava=pygame.Surface((1600,900))
trava.fill('dark green')
cesta.fill('grey')
pocetna=pygame.image.load('pocetnaa.png')
 
car_width = 73
 
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('utrkivać')
clock = pygame.time.Clock()
 
carImg = pygame.image.load('avto.png')
gameIcon = pygame.image.load('pocetnaa.png')

mud=pygame.image.load('mud.png')
mud=pygame.transform.scale(mud,(200,200))
rock=pygame.image.load('rock.png')
rock=pygame.transform.scale(rock,(200,200))
water=pygame.image.load('water.png')
water=pygame.transform.scale(water,(200,200))
dugme=pygame.image.load('undo.png')
dugme=pygame.transform.scale(dugme,(300,300))

L=[mud,rock,water]

pygame.display.set_icon(gameIcon)
pause = False

class gumb:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        actio = False
		
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                actio = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

	
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return actio

 
def things_dodged(count):
    font = pygame.font.SysFont("comicsansms", 25)
    text = font.render("Bodovi: "+str(count), True, white)
    gameDisplay.blit(text,(1400,0))


def things(thingx, thingy,thingw, thingh,color,L):
       gameDisplay.blit(a,[thingx, thingy, thingw, thingh])
    

def car(x,y):
    gameDisplay.blit(carImg,(x,y))
 
def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()
     
 
def crash():
    largeText = pygame.font.SysFont("comicsansms",115)
    TextSurf, TextRect = text_objects("Izgubio si", largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        button("IGRAJ PONOVNO",350,600,250,100,'green','lime',game_loop)
        button("IZAĐI",1000,600,250,100,'red','pink',game_intro)

        pygame.display.update()
        clock.tick(15) 

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
  
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))
    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)
    

def quitgame():
    pygame.quit()
    quit()

def unpause():
    global pause
    pause = False
    

def paused():

    largeText = pygame.font.SysFont("comicsansms",115)
    TextSurf, TextRect = text_objects("Pauzirano", largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    

    while pause:
        for event in pygame.event.get():
    
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        button("NASTAVI",350,600,250,100,'green','lime',unpause)
        button("ODUSTANI",1000,600,250,100,'red','pink',game_intro)

        pygame.display.update()
        clock.tick(15)   


def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        gameDisplay.blit(pocetna,(0,0))
        largeText = pygame.font.SysFont("comicsansms",115)
        TextSurf, TextRect = text_objects("UTRKA", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)
        
        button("START!",350,600,250,100,'green','lime',game_loop)
        button("IZAĐI",1000,600,250,100,'red','pink',quitgame)

        pygame.display.update()
        clock.tick(15)
        
def game_loop():
    global a
    global pause
    
    x = (display_width * 0.42)
    y = (display_height * 0.7)
 
    x_change = 0 
    
    thing_startx = random.randrange(500,1100)
    thing_starty = -600
    thing_speed = 4
    thing_width = 100
    thing_height = 100
 
    thingCount = 1
 
    dodged = 0
 
    gameExit = False
 
    while not gameExit:
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_p:
                    pause = True
                    paused()
                    
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
 
        x += x_change
        
        
        gameDisplay.blit(trava,(0,0))
        gameDisplay.blit(cesta,(400,0))
        gumb_back= gumb(0, 0, dugme, 0.5)
        mx, my = pygame.mouse.get_pos()
        gumb_back.draw(gameDisplay)

        if gumb_back.rect.collidepoint((mx, my)):
            if clic:
                game_intro()
        clic=False
       
        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    clic=True

                    
        for i in range(2):
            a=random.choice(L)
            things(thing_startx, thing_starty, thing_width, thing_height, block_color,L)
        
        
        thing_starty += thing_speed
        car(x,y)
        things_dodged(dodged)
 
        if x > 1050 or  x < 350:
            crash()
 
        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(500,1100)
            dodged += 1
            thing_speed += 1
            thing_width += (dodged * 0.5)

        if y < thing_starty+thing_height:
            print('y crossover')

            if x > thing_startx and x <thing_startx + thing_width or x+car_width >thing_startx and x + car_width < thing_startx+thing_width:
                print('x crossover')
                crash()
       
        pygame.display.update()
        clock.tick(60)

game_intro()
game_loop()
pygame.quit()
quit()


#ne radi umiranje kad se zabije u prepreku
#auto se kreće čudno
#gumb za nazad šteka

