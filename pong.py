import pygame, random
from pygame.locals import*

WINSIZE = [640, 640]
white = (255, 255, 255)
black = (0, 0, 0)
PADDLEWIDTH = 15
PADDLEHEIGHT = 50
BALLSIZE = 10
score = 0
Done = 0
yMin = 0
yMax = WINSIZE[0] - PADDLEHEIGHT

class paddle:
    def __init__(self, x, y, score):
        self.x = x
        self.y = y
        self.score = score

    def ai_move(self):
        if self.y + (PADDLEHEIGHT / 2) < playball.y - (BALLSIZE/2):
            self.y += 1
        if self.y + (PADDLEHEIGHT / 2) > playball.y - (BALLSIZE/2):
            self.y -= 1

    def input(self):
        keystate = pygame.key.get_pressed()
        if keystate[K_UP]:
            if self.y > yMin:
                self.y -= 1
        if keystate[K_DOWN]:
            if self.y < yMax:
                self.y += 1

    def render(self):
        pygame.draw.rect(screen, white, (self.x, self.y, PADDLEWIDTH, PADDLEHEIGHT), 0)

class ball:
    def __init__(self, x, y, dirX, dirY):
        self.x = x
        self.y = y
        self.dirX = dirX
        self.dirY = dirY
    def move(self):
        self.x += self.dirX
        self.y += self.dirY
    def col_check(self):
        if self.y < 0:
            self.dirY = self.dirY * -1
        if self.y + BALLSIZE > WINSIZE[1]:
            self.dirY *= -1
        if self.x + BALLSIZE > WINSIZE[0]:
            self.dirX = self.dirX * -1
        if self.x < 0:
            #score += 1
            restart()
        if collision(self.x, self.y, player1.x, player1.y):
            self.dirX = 0.5
            self.dirY = ((playball.y + BALLSIZE/2) - (player1.y + PADDLEHEIGHT/2))/25
        if collision(self.x, self.y, player2.x, player2.y):
            self.dirX = -0.5
            self.dirY = ((playball.y + BALLSIZE/2) - (player2.y + PADDLEHEIGHT/2))/25
    def render(self):
        pygame.draw.rect(screen, white, (self.x, self.y, BALLSIZE, BALLSIZE), 0)

def collision(ballX, ballY, paddleX, paddleY):
    if((ballX + BALLSIZE >= paddleX and ballX <= paddleX + PADDLEWIDTH) and (ballY + BALLSIZE > paddleY and ballY <= paddleY + PADDLEHEIGHT)):
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
    pygame.display.set_caption('pong')
    global clock
    clock = pygame.time.Clock()
    global player1
    player1 = paddle(10, 320, 0)
    global player2
    player2 = paddle(620, 320, 0)
    global playball
    playball = ball(320, 320, 1, 1)
    restart()

def restart():
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
def handle_paddles():
    player1.input()
    player2.ai_move()
        

main()
