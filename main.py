import random, re, pygame, os, asyncio

pygame.init()
pygame.mixer.init()


#Words
actions = open('./Words/Actions.txt').read().split('\n')
animals = open('./Words/Animals.txt').read().split('\n')
objects = open('./Words/Objects.txt').read().split('\n')
people = open('./Words/People.txt').read().split('\n')
world = open('./Words/World.txt').read().split('\n')
allwords = [actions,animals,objects,people,world]
for category in allwords:
    for word in category:
        if word == '':
            category.remove(word)

#Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

TEAL = (0,255,255)
ORANGE = (255,165,0)
SALMON = (238,119,119)
PURPLE = (108,66,192)
DARKGREEN = (4,121,82)
YELLOW = (255,255,0)
DARKYELLOW = (190,190,0)
DARKRED = (180,20,90)

colors = (WHITE,BLACK,RED,GREEN,BLUE,TEAL,ORANGE,SALMON,PURPLE,DARKGREEN,YELLOW,DARKYELLOW,DARKRED)

# Sounds

# ding = pygame.mixer.Sound('./Sounds/ding.wav')
# buzzer = pygame.mixer.Sound('./Sounds/buzzer.wav')


#Squares
size = (60,60)

class Player():
    def __init__(self, num, color):
        self.pos = 0
        self.num = num
        self.color = color
        self.turn = False

    def move(self, num):
        self.pos += num

    def getSquare(self, squares):
        for s in squares:
            if s.pos == self.pos:
                return s

class Square():
    def __init__(self, rect, pos, category, color):
        self.rect = rect
        self.pos = pos
        self.category = category
        self.color = color

class Button():
    def __init__(self, rect, activeColor, inactiveColor, text):
        self.rect = rect
        self.activeColor = activeColor
        self.inactiveColor = inactiveColor
        self.text = text

    def draw(self, screen):
        cur = pygame.mouse.get_pos()
        if self.rect.collidepoint(cur):
            pygame.draw.rect(screen, self.activeColor, self.rect)
        else:
            pygame.draw.rect(screen, self.inactiveColor, self.rect)
        pygame.draw.rect(screen,BLACK,self.rect,4)

def createSquares():
    squares = []
    for i in range(1,9): # left
        category = ''
        color = None
        if i == 1:
            category = 'Object'
            color = TEAL
        elif i == 2:
            category = 'Action'
            color = ORANGE
        #elif i == 3 or i == 8:
        #    category = '♠'
        #    color = WHITE
        elif i == 4:
            category = 'World'
            color = PURPLE
        elif i == 5:
            category = 'Person'
            color = YELLOW
        elif i == 6 or i == 3 or i == 8:
            category = 'Random'
            color = SALMON
        elif i == 7:
            category = 'Animals'
            color = DARKGREEN
        squares.append(Square(pygame.Rect((0,540-i*60),size),i-3+30,category,color))
    for i in range(1,10): # bottom
        category = ''
        color = None
        if i == 1 or i == 8 or i == 5:
            category = 'Random'
            color = SALMON
        elif i == 2 or i == 9:
            category = 'Animals'
            color = DARKGREEN
        elif i == 3:
            category = 'Object'
            color = TEAL
        elif i == 4:
            category = 'Action'
            color = ORANGE
        #elif i == 5:
        #    category = '♠'
        #    color = WHITE
        elif i == 6:
            category = 'World'
            color = PURPLE
        elif i == 7:
            category = 'Person'
            color = YELLOW
        squares.append(Square(pygame.Rect((540-i*60,540),size),i-2+20,category,color))
    for i in range(1,10): # right
        category = ''
        color = None
        if i == 1 or i == 8:
            category = 'World'
            color = PURPLE
        elif i == 2 or i == 9:
            category = 'Person'
            color = YELLOW
        elif i == 3 or i == 7:
            category = 'Random'
            color = SALMON
        elif i == 4:
            category = 'Animals'
            color = DARKGREEN
        elif i == 5:
            category = 'Object'
            color = TEAL
        elif i == 6:
            category = 'Action'
            color = ORANGE
        #elif i == 7:
        #    category = '♠'
        #    color = WHITE
        squares.append(Square(pygame.Rect((540,i*60),size),i-1+10,category,color))
    for i in range(0,10): # top
        category = ''
        color = None
        if i == 0 or i == 7:
            category = 'Object'
            color = TEAL
        elif i == 1 or i == 8:
            category = 'Action'
            color = ORANGE
        #elif i == 2 or i == 9:
        #    category = '♠'
        #    color = WHITE
        elif i == 3:
            category = 'World'
            color = PURPLE
        elif i == 4:
            category = 'Person'
            color = YELLOW
        elif i == 5 or i == 2 or i == 9:
            category = 'Random'
            color = SALMON
        elif i == 6:
            category = 'Animals'
            color = DARKGREEN
        squares.append(Square(pygame.Rect((i*60,0),size), i, category,color))
    return squares

def newWord(square):
    if square.category == 'Object':
        word = random.choice(objects)
        objects.remove(word)
    elif square.category == 'Action':
        word = random.choice(actions)
        actions.remove(word)
    elif square.category == 'World':
        word = random.choice(world)
        world.remove(word)
    elif square.category == 'Person':
        word = random.choice(people)
        people.remove(word)
    elif square.category == 'Animals':
        word = random.choice(animals)
        animals.remove(word)
    else:
        category = random.choice(allwords)
        word = random.choice(category)
        category.remove(word)
    return word

# Initialize all game variables
clock = pygame.time.Clock()
screen = pygame.display.set_mode([600,600]) #, pygame.FULLSCREEN)
pygame.display.set_caption("Articulate")
squares = createSquares()
players = [Player(1,RED),Player(2,BLUE)]
players[0].turn = True
squarefont = pygame.font.SysFont('Arial', 15, True, False)
spadefont = pygame.font.SysFont('Arial', 30, True, False)
titlefont = pygame.font.SysFont('Arial', 45, True, False)
buttonfont = pygame.font.SysFont('Arial Black', 55, True, False)
turnActive = False
go = Button(pygame.Rect(200,250,200,100),GREEN,(20,190,78),'GO!')
passbutton = Button(pygame.Rect(250,460,100,50),YELLOW,DARKYELLOW,'Pass')
oops = Button(pygame.Rect(400,460,100,50),RED,DARKRED, 'Oops')
spinnerButtons = [Button(pygame.Rect(100,270,40,30),RED,DARKRED,'1'),Button(pygame.Rect(150,270,40,30),RED,DARKRED,'2'),Button(pygame.Rect(200,270,40,30),RED,DARKRED,'3'),Button(pygame.Rect(250,270,40,30),RED,DARKRED,'4'),Button(pygame.Rect(300,270,40,30),RED,DARKRED,'5'),Button(pygame.Rect(100,320,40,30),RED,DARKRED,'6'),Button(pygame.Rect(150,320,40,30),RED,DARKRED,'7'),Button(pygame.Rect(200,320,40,30),RED,DARKRED,'8'),Button(pygame.Rect(250,320,40,30),RED,DARKRED,'9'),Button(pygame.Rect(300,320,40,30),RED,DARKRED,'10')]
fulltimer = pygame.Rect(150,400,300,50)
timertext = ''
timeleft =  30.016
countdown = True
word = ''
category_text = ''
category_color = BLUE
currScore = 0
currSquare = players[0].getSquare(squares)
spinnerSquare = False
drawtimeout = False
passed = False

async def main():
    global clock, scrreen, squares, players, squarefont, spadefont, titlefont, buttonfont, turnActive, go, passbutton, oops, spinnerButtons
    global fulltimer, timertext, timeleft, countdown, word, category_text, category_color, currScore, currSquare, spinnerSquare, drawtimeout, passed
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if go.rect.collidepoint(pygame.mouse.get_pos()) and not turnActive:
                    turnActive = True
                    start_ticks=pygame.time.get_ticks()
                    if players[0].turn:
                        currSquare = players[0].getSquare(squares)
                    else:
                        currSquare = players[1].getSquare(squares)
                    word = newWord(currSquare)
                if passbutton.rect.collidepoint(pygame.mouse.get_pos()) and not passed:
                    passed = True
                    if players[0].turn:
                        currSquare = players[0].getSquare(squares)
                    else:
                        currSquare = players[1].getSquare(squares)
                    word = newWord(currSquare)
                if oops.rect.collidepoint(pygame.mouse.get_pos()):
                    currScore -= 1
                    if currScore < 0:
                        currScore = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_SPACE and turnActive and not countdown:
                    currScore += 1
                    # ding.play()
                    if players[0].turn:
                        currSquare = players[0].getSquare(squares)
                    else:
                        currSquare = players[1].getSquare(squares)
                    word = newWord(currSquare)
        if players[0].turn:
            turntext = "It is Team 1's turn"
            category_text = players[0].getSquare(squares).category
            category_color = players[0].getSquare(squares).color
        else:
            turntext = "It is Team 2's turn"
            category_text = players[1].getSquare(squares).category
            category_color = players[1].getSquare(squares).color
        screen.fill(WHITE)
        if not turnActive:
            screen.blit(titlefont.render(turntext,True,BLACK),(135,100))
            screen.blit(titlefont.render('The category is ',True,BLACK),(110,150))
            screen.blit(titlefont.render(category_text,True,category_color),(390,150))
            go.draw(screen)
            screen.blit(buttonfont.render(go.text,True,BLACK),(go.rect.centerx-55,go.rect.centery-45))
        else:
            seconds = (pygame.time.get_ticks()-start_ticks)/1000
            if seconds < 1:
                timertext = '3'
            elif seconds < 2:
                timertext = '2'
            elif seconds < 3:
                timertext = '1'
            else:
                timertext = ''
                countdown = False
            if timeleft > 0 and not countdown:
                timeleft -= .016
                pygame.draw.rect(screen,RED,(150,400,timeleft*10,50))
                pygame.draw.rect(screen,BLACK,fulltimer,1)
                screen.blit(buttonfont.render('Score: ' + str(currScore),True,BLACK),(100,300))
                if not passed:
                    passbutton.draw(screen)
                    screen.blit(titlefont.render(passbutton.text,True,BLACK),(passbutton.rect.centerx-43,passbutton.rect.centery-25))
                oops.draw(screen)
                screen.blit(titlefont.render(oops.text,True,BLACK),(oops.rect.centerx-47,oops.rect.centery-30))
            elif timeleft <= 0:
                # buzzer.play()
                drawtimeout = True
                turnActive = False
                countdown = True
                passed = False
                timeleft = 30.016
                if players[0].turn == True:
                    players[0].pos += currScore
                    if players[0].pos > 35:
                        players[0].pos = 35
                    currScore = 0
                    if players[0].getSquare(squares).category == 'Random' or players[0].getSquare(squares).category == 'Action':
                        spinnerSquare = True
                    players[0].turn = False
                    players[1].turn = True
                else:
                    players[1].pos += currScore
                    if players[1].pos > 35:
                        players[1].pos = 35
                    currScore = 0
                    if players[1].getSquare(squares).category == 'Random' or players[1].getSquare(squares).category == 'Action':
                        spinnerSquare = True
                    players[1].turn = False
                    players[0].turn = True
            if category_text == 'World' or category_text == 'Random':
                longtextfont = pygame.font.SysFont('Arial', 35, True, False)
                screen.blit(longtextfont.render(word,True,BLACK),(90,150))
                screen.blit(titlefont.render(currSquare.category,True,currSquare.color), (90,100))
            else:
                screen.blit(titlefont.render(word,True,BLACK),(150,150))
                screen.blit(titlefont.render(currSquare.category,True,currSquare.color), (150,100))
            screen.blit(buttonfont.render(timertext,True,BLACK),(300,250))
        for s in squares:
            pygame.draw.rect(screen,s.color,s.rect)
            pygame.draw.rect(screen, BLACK, s.rect, 1)
            if s.category == '♠':
                t = spadefont.render(s.category,True,BLACK)
                screen.blit(t, (s.rect.centerx-7,s.rect.centery-30))
            else:
                t = squarefont.render(s.category,True,BLACK)
                screen.blit(t,s.rect.topleft)
        screen.blit(squarefont.render('FINISH',True,random.choice(colors)),(squares[7].rect.centerx-20,squares[7].rect.centery))
        for p in players:
            offset = 0
            t = squarefont.render(str(p.num),True,BLACK)
            if p.num == 1:
                offset = 12
                offset2 = 3
                offset3 = 9
            else:
                offset = -12
                offset2 = -21
                offset3 = -15
            pygame.draw.circle(screen,p.color,(p.getSquare(squares).rect.center[0]+offset,p.getSquare(squares).rect.center[1]+offset),15)
            pygame.draw.circle(screen,BLACK,(p.getSquare(squares).rect.center[0]+offset,p.getSquare(squares).rect.center[1]+offset),15,1)
            screen.blit(t,(p.getSquare(squares).rect.center[0]+offset3,p.getSquare(squares).rect.center[1]+offset2))
        if drawtimeout:
            screen.blit(titlefont.render('TIME!',True,RED),(250,300))
        pygame.display.flip()
        if drawtimeout:
            pygame.time.wait(5000)
            drawtimeout = False
        await asyncio.sleep(0)

asyncio.run(main())
