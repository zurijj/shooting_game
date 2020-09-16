import pygame
import sys
import random
from time import sleep

padWidth = 480
padHeight = 640
rockImage = ['PyShooting/rock01.png', 'PyShooting/rock02.png', 'PyShooting/rock03.png', 'PyShooting/rock04.png', 'PyShooting/rock05.png', \
             'PyShooting/rock06.png', 'PyShooting/rock07.png', 'PyShooting/rock08.png', 'PyShooting/rock09.png', 'PyShooting/rock10.png', \
             'PyShooting/rock11.png', 'PyShooting/rock12.png', 'PyShooting/rock13.png', 'PyShooting/rock14.png', 'PyShooting/rock15.png', \
             'PyShooting/rock16.png', 'PyShooting/rock17.png', 'PyShooting/rock18.png', 'PyShooting/rock19.png', 'PyShooting/rock20.png', \
             'PyShooting/rock21.png', 'PyShooting/rock22.png', 'PyShooting/rock23.png', 'PyShooting/rock24.png', 'PyShooting/rock25.png', \
             'PyShooting/rock26.png', 'PyShooting/rock27.png', 'PyShooting/rock28.png', 'PyShooting/rock29.png', 'PyShooting/rock30.png']
explosionSound = ['PyShooting/explosion01.wav', 'PyShooting/explosion02.wav', 'PyShooting/explosion03.wav', 'PyShooting/explosion04.wav']


def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))

def writeScore(count):
    global gamePad
    font = pygame.font.Font('PyShooting/NanumGothic.ttf', 20)
    text = font.render('파괴한 운석 수:' + str(count), True, (255, 255, 255))
    gamePad.blit(text, (10, 0))

def writeMessage(text):
    global gamePad, gameOverSound
    textFont = pygame.font.Font('PyShooting/NanumGothic.ttf', 60)
    text = textFont.render(text, True, (255, 0, 0))
    textpos = text.get_rect()
    textpos.center = (padWidth/2, padHeight/2)
    gamePad.blit(text, textpos)
    pygame.display.update()
    pygame.mixer.music.stop()
    gameOverSound.play()
    sleep(2)
    pygame.mixer.music.play(-1)
    runGame()

def crash():
    global gamePad
    writeMessage('전투기 파괴!')

def gameOver():
    global gamePad
    writeMessage('게임 오버!')

def writePassed(count):
    global gamePad
    font = pygame.font.Font('PyShooting/NanumGothic.ttf', 20)
    text = font.render('놓친 운석:' + str(count), True, (255, 0, 0))
    gamePad.blit(text, (350, 0))

def initGame():
    global gamePad, clock, background, fighter, missile, explosion, missileSound, gameOverSound
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('PyShooting')
    background = pygame.image.load('PyShooting/background.png')
    fighter = pygame.image.load('PyShooting/fighter.png')
    missile = pygame.image.load('PyShooting/missile.png')
    explosion = pygame.image.load('PyShooting/explosion.png')
    pygame.mixer.music.load('PyShooting/music.wav')
    pygame.mixer.music.play(-1)
    missileSound = pygame.mixer.Sound('PyShooting/missile.wav')
    gameOverSound = pygame.mixer.Sound('PyShooting/gameover.wav')
    clock = pygame.time.Clock()

def runGame():
    global gamePad, clock, background, fighter, missile, explosion, missileSound

    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]

    x = padWidth * 0.45
    y = padHeight * 0.9
    fighterX = 0

    missileXY = []

    rock = pygame.image.load(random.choice(rockImage))
    rockSize = rock.get_rect().size
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]
    destroySound = pygame.mixer.Sound(random.choice(explosionSound))

    rockX = random.randrange(0, padWidth - rockWidth)
    rockY = 0
    rockSpeed = 2

    isShot = False
    shotCount = 0
    rockPassed = 0


    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                pygame.quit()
                sys.exit()

            if event.type in [pygame.KEYDOWN]: # 키가 눌리면
                if event.key == pygame.K_LEFT:
                    fighterX -= 5

                elif event.key == pygame.K_RIGHT:
                    fighterX += 5

                elif event.key == pygame.K_SPACE:
                    missileSound.play()
                    missileX = x + fighterWidth / 2
                    missileY = y - fighterHeight
                    missileXY.append([missileX, missileY])

            if event.type in [pygame.KEYUP]:
                if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                    fighterX = 0

        drawObject(background, 0, 0)

        x += fighterX
        if x < 0:
            x = 0
        elif x > padWidth - fighterWidth:
            x = padWidth - fighterWidth

        if y < rockY + rockHeight:
            if (rockX > x and rockX < x + fighterWidth) or \
                    (rockX + rockWidth > x and rockX + rockWidth < x + fighterWidth):
                crash()

        drawObject(fighter, x, y)

        if len(missileXY) != 0:
            for i, bxy in enumerate(missileXY):
                bxy[1] -= 10 # 미사일은 위로 발사
                missileXY[i][1] = bxy[1]

                if bxy[1] < rockY:
                    if bxy[0] > rockX and bxy[0] < rockX + rockWidth:
                        missileXY.remove(bxy)
                        isShot = True
                        shotCount += 1

                if bxy[1] <= 0: # 미사일 화면 밖으로
                    try:
                        missileXY.remove(bxy)
                    except:
                        pass

        if len(missileXY) != 0:
            for bx, by in missileXY:
                drawObject(missile, bx, by)

        writeScore(shotCount)

        rockY += rockSpeed

        if rockY > padHeight:
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            rockPassed += 1
            if rockPassed == 3:
                gameOver()

        writePassed(rockPassed)

        if isShot:
            drawObject(explosion, rockX, rockY)
            destroySound.play()
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            destroySound = pygame.mixer.Sound(random.choice(explosionSound))
            isShot = False

            rockSpeed += 0.02
            if rockSpeed >= 10:
                rockSpeed = 10

        drawObject(rock, rockX, rockY)

        pygame.display.update()

        clock.tick(60)

    pygame.quit()

initGame()
runGame()