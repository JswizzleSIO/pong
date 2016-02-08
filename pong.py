import pygame, random, sys, os
from pygame.locals import*
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
#set main directory and load sounds from 'sounds folder'
main_dir = os.path.dirname(os.path.abspath("__file__"))
bump1 = pygame.mixer.Sound(os.path.join('sounds', "bump.ogg"))
hit1 = pygame.mixer.Sound(os.path.join('sounds', "bwubwub.ogg"))
coin1 = pygame.mixer.Sound(os.path.join('sounds', "beep.ogg"))
pygame.mixer.music.load(os.path.join('sounds', "music.ogg"))
#set winsize and basic colours
WINSIZE = [640, 640]
white = (255, 255, 255)
black = (0, 0, 0)
#set paddlewidth since it doesn't change
PADDLEWIDTH = 15
Done = 0
pygame.init()
#load font and images
font = pygame.font.Font('Minecraft.ttf', 25)
titlefont = pygame.font.Font('Minecraft.ttf', 50)
coindwg = pygame.image.load(os.path.join(main_dir, 'coin.png'))
heart = pygame.image.load(os.path.join(main_dir, 'heart.png'))
#set ai offset, see ai move function in paddle class
aiOffset = 0

#effect = pygame.mixer.Sound(os.path.join(main_dir, '1.wav'))


class paddle:
    def __init__(self, x, y, health, length, speed, bspeed):
        self.x = x
        self.y = y
        self.health = health
        self.length = length
        self.speed = speed
        self.bspeed = bspeed

    def ai_move(self):
        #ignoring the ai offset this would check if the paddle center was at the ball center
        #and move it towards if it was not
        #with offset the hit is set to be between the top and bottom of the paddle
        #the purpose it to return the ball with some y velocity(see how y vel is set in ball collision)
        if self.y + (self.length / 2) < playball.y + (playball.size/2) - aiOffset:
            if self.y < WINSIZE[0] - self.length:
                self.y += self.speed#move towards at paddle speed
        if self.y + (self.length/ 2) > playball.y + (playball.size/2) - aiOffset:
            if self.y > 0:
                self.y -= self.speed

    def input(self):
        #same idea as ai move but with input from player
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
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
        #move ball along its current path set by dirX and dirY
        self.x += self.dirX
        self.y += self.dirY
    def col_check(self):
        global aiOffset
        #ball hits top screen will set y velocity to be opposite
        if self.y < 0:
            if self.dirY < 0:#this checks to make sure that ball hasn't been bounced a bit out of bounds and is in the process of bouncing back in
                self.dirY = self.dirY * -1
                play_sound("bounce")
        #same thing but for bottom of screen
        if self.y + self.size > WINSIZE[1]:
            if self.dirY > 0:
                self.dirY *= -1
                play_sound("bounce")
        if self.x + self.size > WINSIZE[0]:
            #if ball hits player2(ai)side remove 1 of their health units, play hit sound and restart
            player2.health -= 1
            play_sound("hit")
            restart()
        if self.x < 0:
            #same thing but checks for no health left and runs the you died function
            player1.health -= 1
            play_sound("hit")
            if player1.health < 1:
                you_died()
            restart()
        if self.dirX < 0:
            #checks for collision with paddle and bounces the ball back but..
            #only if the ball is headed towards you
            #done to avoid bouncing the ball again when its already headed away
            if collision(self, player1):
                self.dirX = 2.5
                self.dirY = (((playball.y + self.size/2) - (player1.y + player1.length/2))/(player1.length/2))*5
                play_sound("bounce")
        if self.dirX > 0:
            #same dealio but also set aiOffset after a bounce and create a new coin
            if collision(self, player2):
                self.dirX = -2.5
                self.dirY = (((playball.y + self.size/2) - (player2.y + player2.length/2))/(player2.length/2))*5
                coin.new(player2.x, (player2.y + player2.length/2))
                aiOffset = random.randrange(0, 48, 1)-24
                play_sound("bounce")
    def render(self):
        pygame.draw.rect(screen, white, (self.x, self.y, self.size, self.size), 0)

class coin:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
    def new(x, y):
        newcoin = coin(x, y, 20)
        coinlist.append(newcoin)
    def move(self):
        self.x -= 3
    def col_check(self):
        #calls collision, if you get the coin with the paddle score increases by 10
        global score
        if collision(self, player1):
            play_sound("coin")
            score += 10
            return(1)
    def draw(self):
        screen.blit(coindwg, (self.x, self.y))


def collision(ball, player):
    #basic collision function takes 2 objects.. yeah
    if((ball.x + ball.size >= player.x and ball.x <= player.x + PADDLEWIDTH) and (ball.y + ball.size > player.y and ball.y <= player.y + player.length)):
        return(1) #collision
    else:
        return(0)

def main():
    global screen
    screen = pygame.display.set_mode(WINSIZE)
    pygame.display.set_caption('pong legacy')
    
    menu_title()
    initialize_game()
    while not Done:
        run_game()
def menu_title():
    pygame.mixer.music.play(-1, 0.2)
    ren = font.render("Paddle Mans Evloutionary Grinding Adventure", True, white)
    screen.blit(ren, (30, 100))
    ren = font.render("AKA", True, white)
    screen.blit(ren, (300, 165))
    ren = titlefont.render("Pong Legacy", True, white)
    screen.blit(ren, (150, 220))
    pygame.display.update()
    key_wait()
    pygame.mixer.music.fadeout(2000)
    
def run_game():
    handle_coins()
    handle_paddles()
    playball.move()
    playball.col_check()
    render_all()
    pygame.display.update()
    screen.fill(black)
    clock.tick(60)

def initialize_game():
    global clock
    clock = pygame.time.Clock()
    global player1
    global player2
    player1 = paddle(10, 320, 1, 20, 2, 1)
    player2 = paddle(615, 320, 12, 50, 5, 1)
    global playball
    playball = ball(320, 320, 1, 1, 10)
    global coinlist
    coinlist = []
    global score
    score = 0

    global upgradelist
    upgradelist = []
    speedup = upgrade(10, 20, speed_up, "Paddle Speed increase")
    sizeup = upgrade(10, 20, size_up, "Paddle length increase")
    upgradelist.append(sizeup)
    upgradelist.append(speedup)
    restart()

def restart():
    render_all()
    pygame.time.wait(1000)
    ren = font.render("3", True, white)
    screen.blit(ren, (320, 280))
    pygame.display.update()
    play_sound("bounce")
    pygame.time.wait(1000)
    pygame.draw.rect(screen, black, (320, 280, 30, 30), 0)
    ren = font.render("2", True, white)
    screen.blit(ren, (320, 280))
    pygame.display.update()
    play_sound("bounce")
    pygame.time.wait(1000)
    pygame.draw.rect(screen, black, (320, 280, 30, 30), 0)
    ren = font.render("1", True, white)
    screen.blit(ren, (320, 280))
    pygame.display.update()
    play_sound("bounce")
    pygame.time.wait(1000)
    play_sound("coin")
    pygame.draw.rect(screen, black, (320, 280, 30, 30), 0)

    player1.y = 320
    player2.y = 320
    start = random.randrange(1, 3, 1)
    if start == 1:
        playball.dirX = 2.5
    if start == 2:
        playball.dirX = -2.5
    playball.dirY = random.random()*5
    playball.x = 320
    playball.y = 320
def render_all():
    heartX = 0
    heartY = 0
    for heartX in range (player1.health):
        screen.blit(heart, (heartX * 35 + 10, heartY))
    for heartX in range (player2.health):
        HDX = heartX*35
        if heartX > 8:
            heartY = 40
            HDX -= 8 * 35
        screen.blit(heart, (WINSIZE[0] - HDX, heartY))
    for object in coinlist:
        object.draw()
    player1.render()
    player2.render()
    playball.render()
    text = (str(score))
    ren = font.render(text, True, white)
    screen.blit(ren, (310, 10))

def handle_coins():
    #move and check if a coin has collision or is off the map
    for object in coinlist:
        object.move()
        if object.x < 0 - object.size:
            coinlist.remove(object)
            del object
        elif object.x < 50:
            if object.col_check():
                coinlist.remove(object)
                del object

def play_sound(event):
    #play sound based on what event is given when called
    if event == "bounce":
        bump1.play()
    if event == "hit":
        hit1.play()
    if event == "coin":
        coin1.play()

def you_died():
    #render the you died text and send you to the store
    ren = font.render("You Died", True, white)
    screen.blit(ren, (300, 280))
    pygame.display.update()
    pygame.time.wait(1000)
    store()

class upgrade:
    #class for upgrade, pretty simple
    def __init__(self, cost, costInc, function, name):
        self.cost = cost
        self.costInc = costInc
        self.function = function
        self.name = name

def store():
    pygame.key.set_repeat(100, 100)
    pos = 0
    instore = 1
    while instore:
        render_store(pos)
        pygame.display.update()
        screen.fill(black)
        pos, instore = store_input(pos, instore)
        if pos > 1:
            pos = 0
        if pos < 0:
            pos = 1
        clock.tick(60)
    pygame.key.set_repeat()

def render_store(pos):
    x = 250
    y = 150
    #draw the upgrade options from the upgrade list and draw a box beside the option you are on
    pygame.draw.rect(screen, white, (x - 30, y + 30 * pos, 20, 20), 0)
    for object in upgradelist:
        text = (object.name + " " + str(object.cost))
        ren = font.render(text, True, white)
        screen.blit(ren, (x, y))
        y += 30
    text = (str(score))
    ren = font.render(text, True, white)
    screen.blit(ren, (310, 10))

def store_input(pos, instore):
    #cycle through upgrade options, pos is your cursor positin in the store
    global score
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_UP:
                pos -= 1
            if event.key == K_DOWN:
                pos += 1
            if event.key == K_SPACE:
                #space to buy and run the upgrade function if you can afford
                if score >= upgradelist[pos].cost:
                    print("can afford")
                    score -= upgradelist[pos].cost
                    upgradelist[pos].cost += upgradelist[pos].costInc
                    upgradelist[pos].function()
                else:
                    print("need more cash")
            #enter to go back and play again
            if event.key == K_RETURN:
                player1.health = 1
                player1.y = 300
                player2.y = 300
                instore = 0
    return(pos, instore)

def speed_up():
    player1.speed += .5
def size_up():
    player1.length += 5

def handle_paddles():
    player1.input()
    player2.ai_move()

def key_wait():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

        

main()
