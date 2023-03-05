import pygame, sys
from pygame.locals import *

FPS = 40
actual_fps=pygame.time.Clock()
screen_width=1400
screen_height=800
red = (255, 130, 130)
green = (130,255,130)
white = (255, 255, 255)
darkRed = (150, 100, 100)
darkGreen = (100,150,100)





pygame.init()
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("TRON GAME")
welcome_background=pygame.image.load("welcomebackground3.png").convert()
background=pygame.image.load("background.png").convert()
control_background=pygame.image.load("controlsbackground.png").convert()
credit_background=pygame.image.load("background.png").convert()
gameover_background=pygame.image.load("gameoverbackground.png").convert()
back_symbol=pygame.image.load("backspace_key.png")
back_symbol=pygame.transform.scale(back_symbol, (200, 75))
font = pygame.font.SysFont("comicsans", 80)
welcome_background_sound = pygame.mixer.Sound('welcomebackgroundsound.mp3')
button_click_sound = pygame.mixer.Sound('buttonclicksound.wav')
collision_sound = pygame.mixer.Sound('collisionsound.wav')
gamebackground_sound = pygame.mixer.Sound('gamebackgroundsound.mp3')

class tronBike:
    def __init__(self, number, color, darkColor, side):
        self.w = 10
        self.h = 10
        self.x = abs(side - 100)
        self.y = screen_height/2 - self.h
        self.speed = 10
        self.color = color
        self.darkColor = darkColor
        self.history = [[self.x, self.y]]
        self.number = number
        self.length = 1

    
    def draw(self):
        for i in range(len(self.history)):
            if i == self.length - 1:
                pygame.draw.rect(screen, self.darkColor, (self.history[i][0], self.history[i][1], self.w, self.h))
            else:    
                pygame.draw.rect(screen, self.color, (self.history[i][0], self.history[i][1], self.w, self.h))

    
    def move(self, xdir, ydir):
        self.x += xdir*self.speed
        self.y += ydir*self.speed
        self.history.append([self.x, self.y])
        self.length += 1
        if self.x < 0 or self.x > screen_width or self.y < 0 or self.y > screen_height:
            gameOver(self.number)

    
    def check_collision(self, opponent):
        if abs(opponent.history[opponent.length - 1][0] - self.history[self.length - 1][0]) < self.w and abs(opponent.history[opponent.length - 1][1] - self.history[self.length - 1][1]) < self.h:
            gameOver(0)
        for i in range(opponent.length):
            if abs(opponent.history[i][0] - self.history[self.length - 1][0]) < self.w and abs(opponent.history[i][1] - self.history[self.length - 1][1]) < self.h:
                gameOver(self.number)

        for i in range(len(self.history) - 1):
            if abs(self.history[i][0] - self.x) < self.w and abs(self.history[i][1] - self.y) < self.h and self.length > 2:
                gameOver(self.number)

def gameOver(number):
    gamebackground_sound.stop()
    collision_sound.play()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_BACKSPACE:
                    button_click_sound.play()
                    welcome_screen()
        if number == 0:
            text = font.render("Both the Players Collided!", True, (39, 242, 235))
        else:
            if number == 1:
                text = font.render("Red Player Lost the Game!", True, (39, 242, 235))
            if number == 2:
                text = font.render("Green Player Lost the Game!", True, (39, 242, 235))
        screen.blit(gameover_background,(0,0))
        screen.blit(text, (screen_width/2 - text.get_width() //2, screen_height//2 - text.get_height()//2))
        screen.blit(back_symbol,(15,15))
        pygame.display.update()
        actual_fps.tick(FPS)


def tron():
    loop = True

    bike1 = tronBike(1, red, darkRed, 0)
    bike2 = tronBike(2, green, darkGreen, screen_width)

    x_red = 1
    y_red = 0
    x_green = -1
    y_green = 0
    
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_UP:
                    if not (x_green == 0 and y_green == 1):
                        x_green = 0
                        y_green = -1
                if event.key == pygame.K_DOWN:
                    if not (x_green == 0 and y_green == -1):
                        x_green = 0
                        y_green = 1
                if event.key == pygame.K_LEFT:
                    if not (x_green == 1 and y_green == 0):
                        x_green = -1
                        y_green = 0
                if event.key == pygame.K_RIGHT:
                    if not (x_green == -1 and y_green == 0):
                        x_green = 1
                        y_green = 0
                if event.key == pygame.K_w:
                    if not (x_red == 0 and y_red == 1):
                        x_red = 0
                        y_red = -1
                if event.key == pygame.K_s:
                    if not (x_red == 0 and y_red == -1):
                        x_red = 0
                        y_red = 1
                if event.key == pygame.K_a:
                    if not (x_red == 1 and y_red == 0):
                        x_red = -1
                        y_red = 0
                if event.key == pygame.K_d:
                    if not (x_red == -1 and y_red == 0):
                        x_red = 1
                        y_red = 0
                   
        screen.blit(background, (0, 0))
        bike1.draw()
        bike2.draw()

        bike1.move(x_red, y_red)
        bike2.move(x_green, y_green)

        bike1.check_collision(bike2)
        bike2.check_collision(bike1)
        
        pygame.display.update()
        actual_fps.tick(10)

def control_screen():
    welcome_background_sound.play()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==KEYDOWN and (event.key==K_BACKSPACE):
                welcome_background_sound.stop()
                pygame.time.delay(100)
                button_click_sound.play()
                print("SUCCESSFULLY ENTERED INTO MENU !!")
                welcome_screen()
            else:
                screen.blit(control_background,(0,0))      
                pygame.display.update()
                actual_fps.tick(FPS)


def welcome_screen():
    welcome_background_sound.play()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN and (event.key==K_SPACE):
                print("SUCCESSFULLY ENTERED INTO GAME !!")
                welcome_background_sound.stop()
                pygame.time.delay(100)
                button_click_sound.play()
                #pygame.time.delay(0)
                gamebackground_sound.play()
                tron()
            if event.type==KEYDOWN and (event.key==K_r):
                print("SUCCESSFULLY ENTERED INTO CONTROLS !!")
                welcome_background_sound.stop()
                pygame.time.delay(100)
                button_click_sound.play()
                control_screen()
            if event.type==KEYDOWN and (event.key==K_c):
                print("SUCCESSFULLY EXITED !!")
                welcome_background_sound.stop()
                pygame.time.delay(100)
                button_click_sound.play()
                pygame.time.delay(400)
                pygame.quit()
                sys.exit()
            else:      
                screen.blit(welcome_background,(0,0))
                pygame.display.update()
                actual_fps.tick(FPS)
welcome_screen()

