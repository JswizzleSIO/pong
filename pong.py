import pygame, random, sys, os
from pygame.locals import*
main_dir = os.path.dirname(os.path.abspath("__file__"))

WINSIZE = [640, 640]
white = (255, 255, 255)
black = (0, 0, 0)
PADDLEWIDTH = 15
Done = 0
pygame.init()
font = pygame.font.Font('Minecraft.ttf', 25)
coindwg = pygame.image.load(os.path.join(main_dir, 'coin.png'))

class paddle:
    def __init__(self, x, y, health, length, speed, bspeed):
        self.x = x
        self.y = y
        self.health = health
        self.length = length
        self.speed = speed
        self.bspeed = bspeed

    def ai_move(self):
        if self.y + (self.length / 2) < playball.y - (playball.size/2):
            self.y += 1
        if self.y + (self.length/ 2) > playball.y - (playball.size/2):
            self.y -= 1

    def input(self):
        keystate = pygame.key.get_pressed()
        if keystate[K_UP]:
            if self.y > 0:
                self.y -= self.speed
        if keystate[K_DOWN]:
            if self.y < WINSIZE[0] - self.length:
                self.y += self.speed

    def render(self):
        pygame.draw.rect(screen, white, (self.x, self.y, PADDLEWIDTH, self.length), 0)

class ball:
    def __init__(self, x, y, dirX, dirY, size):
        self.x = x
        self.y = y
        self.dirX = dirX
        self.dirY = dirY
        self.size = size
    def move(self):
        self.x += self.dirX
        self.y += self.dirY
    def col_check(self):
        if self.y < 0:
            self.dirY = self.dirY * -1
        if self.y + self.size > WINSIZE[1]:
            self.dirY *= -1
        if self.x + self.size > WINSIZE[0]:
            player2.health -= 1
            restart()
        if self.x < 0:
            player1.health -= 1
            restart()
        if collision(self, player1):
            self.dirX = 0.5
            self.dirY = ((playball.y + self.size/2) - (player1.y + player1.length/2))/25
        if collision(self, player2):
            self.dirX = -0.5
            self.dirY = ((playball.y + self.size/2) - (player2.y + player2.length/2))/25
            coin.new(player2.x, player2.y)
    def render(self):
        pygame.draw.rect(screen, white, (self.x, self.y, self.size, self.size), 0)

class coin:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
    def new(x, y):
        newcoin = coin(x, y, 20)
        coinlist.append(newcoin)
    def move():
        self.x -= 1
    def col_check():
        collision(self, player1)
    def draw():
        screen.blit(coindwg, (self.x, self.y))
        

def collision(ball, player):
    if((ball.x + ball.size >= player.x and ball.x <= player.x + PADDLEWIDTH) and (ball.y + ball.size > player.y and ball.y <= player.y + player.length)):
        return(1) #collision
    else:
        return(0)

def main():
    initialize_game()
    while not Done:
        handle_paddles()
        playball.move()
        playball.col_check()
        render_all()
        pygame.display.update()
        screen.fill(black)
        pygame.event.clear()
        clock.tick(300)

def initialize_game():
    pygame.init()
    global screen
    screen = pygame.display.set_mode(WINSIZE)
    pygame.display.set_caption('pong legacy')
    global clock
    clock = pygame.time.Clock()
    global player1
    global player2
    player1 = paddle(10, 320, 1, 50, 1, 1)
    player2 = paddle(615, 320, 1, 50, 1, 1)
    global playball
    playball = ball(320, 320, 1, 1, 10)
    global coinlist
    coinlist = []
    global score
    score = 0
    restart()

def restart():
    render_all()
    ren = font.render("3", True, white)
    screen.blit(ren, (320, 280))
    pygame.display.update()
    pygame.time.wait(1000)
    pygame.draw.rect(screen, black, (320, 280, 30, 30), 0)
    ren = font.render("2", True, white)
    screen.blit(ren, (320, 280))
    pygame.display.update()
    pygame.time.wait(1000)
    pygame.draw.rect(screen, black, (320, 280, 30, 30), 0)
    ren = font.render("1", True, white)
    screen.blit(ren, (320, 280))
    pygame.display.update()
    pygame.time.wait(1000)
    pygame.draw.rect(screen, black, (320, 280, 30, 30), 0)
    
    start = random.randrange(0, 2, 1)
    if start == 1:
        playball.dirX = .5
    if start == 2:
        playball.dirX = -.5
    playball.dirY = random.random()
    playball.x = 320
    playball.y = 320
def render_all():
    player1.render()
    player2.render()
    playball.render()
    text = (str(player1.health) + "\\" + str(player2.health))
    ren = font.render(text, True, white)
    screen.blit(ren, (310, 10))
def handle_paddles():
    player1.input()
    player2.ai_move()
        

main()
