import pygame
import sys
import random
from time import sleep

padWidth = 480  # 창의 가로길이
padHeight = 640  # 창의 세로길이

# 바위 이미지
rockImage = ['PyShooting/rock01.png', 'PyShooting/rock02.png', 'PyShooting/rock03.png', 'PyShooting/rock04.png', 'PyShooting/rock05.png', \
             'PyShooting/rock06.png', 'PyShooting/rock07.png', 'PyShooting/rock08.png', 'PyShooting/rock09.png', 'PyShooting/rock10.png', \
             'PyShooting/rock11.png', 'PyShooting/rock12.png', 'PyShooting/rock13.png', 'PyShooting/rock14.png', 'PyShooting/rock15.png', \
             'PyShooting/rock16.png', 'PyShooting/rock17.png', 'PyShooting/rock18.png', 'PyShooting/rock19.png', 'PyShooting/rock20.png', \
             'PyShooting/rock21.png', 'PyShooting/rock22.png', 'PyShooting/rock23.png', 'PyShooting/rock24.png', 'PyShooting/rock25.png', \
             'PyShooting/rock26.png', 'PyShooting/rock27.png', 'PyShooting/rock28.png', 'PyShooting/rock29.png', 'PyShooting/rock30.png']

# 바위 폭발 사운드
explosionSound = ['PyShooting/explosion01.wav', 'PyShooting/explosion02.wav', 'PyShooting/explosion03.wav', 'PyShooting/explosion04.wav']

# 객체 창에 그리기
def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))

# 스코어 띄우기
def writeScore(count):
    global gamePad
    font = pygame.font.Font('PyShooting/NanumGothic.ttf', 20)   # 폰트, 글자 크기 설정
    text = font.render('파괴한 운석 수:' + str(count), True, (255, 255, 255))  # 창에 나타낼 글씨 생성 (텍스트, Anti Aliasing 여부, 색)
    gamePad.blit(text, (10, 0))  # 창에 글씨 나타내기 (문구, x좌표, y좌표)

# 문구 띄우기
def writeMessage(text):
    global gamePad, gameOverSound
    textFont = pygame.font.Font('PyShooting/NanumGothic.ttf', 60)
    text = textFont.render(text, True, (255, 0, 0))
    textpos = text.get_rect()  # 텍스트 객체 출력 위치 갖고옴
    textpos.center = (padWidth/2, padHeight/2)  # 텍스트 객체의 중심좌표 설정
    gamePad.blit(text, textpos)
    pygame.display.update()   # 창 업데이트 (추가 된 글씨, 객체 나타냄)
    pygame.mixer.music.stop()   #
    gameOverSound.play()   # 노래 객체 재생
    sleep(2)
    pygame.mixer.music.play(-1)   # 종료시까지 반복
    runGame()

# 바위랑 전투기 충돌 시
def crash():
    global gamePad
    writeMessage('전투기 파괴!')

# 게임 오버상황이 발생 시
def gameOver():
    global gamePad
    writeMessage('게임 오버!')

# 바위가 지나갈 시 놓친 운석 카운트
def writePassed(count):
    global gamePad
    font = pygame.font.Font('PyShooting/NanumGothic.ttf', 20)
    text = font.render('놓친 운석:' + str(count), True, (255, 0, 0))
    gamePad.blit(text, (350, 0))

# 창, 이미지 초기화
def initGame():
    global gamePad, clock, background, fighter, missile, explosion, missileSound, gameOverSound
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight)) # 가로 : padWidth, 세로 : padHeight 창 생성
    pygame.display.set_caption('PyShooting') # 타이틀 설정
    background = pygame.image.load('PyShooting/background.png') # 게임 배경 설정
    fighter = pygame.image.load('PyShooting/fighter.png') # 전투기 이미지
    missile = pygame.image.load('PyShooting/missile.png') # 미사일 이미지
    explosion = pygame.image.load('PyShooting/explosion.png') # 바위 파괴시 이미지
    pygame.mixer.music.load('PyShooting/music.wav') # 게임 배경음악 불러오기
    pygame.mixer.music.play(-1) # 게임 배경음악 종료시까지 재생
    missileSound = pygame.mixer.Sound('PyShooting/missile.wav')  # 미사일 사운드
    gameOverSound = pygame.mixer.Sound('PyShooting/gameover.wav')  # 게임종료 사운드
    clock = pygame.time.Clock()  # FPS를 맞추기 위한 초기화

# 게임 실행
def runGame():
    global gamePad, clock, background, fighter, missile, explosion, missileSound

    fighterSize = fighter.get_rect().size  # 비행기 객체의 크기를 가져옴
    fighterWidth = fighterSize[0]  # 비행기 중심의 X 좌표
    fighterHeight = fighterSize[1]  # 비행기 중심의 Y 좌표

    x = padWidth * 0.45  # 초기 비행기 X 위치
    y = padHeight * 0.9  # 초기 비행기 Y 위치
    fighterX = 0  # 비행기의 움직임

    missileXY = []   # 미사일 객체

    rock = pygame.image.load(random.choice(rockImage))  # 바위객체 rockImage에서 임의로 1개 선택
    rockSize = rock.get_rect().size
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]
    destroySound = pygame.mixer.Sound(random.choice(explosionSound))

    rockX = random.randrange(0, padWidth - rockWidth) # 0부터 (창의 넓이 - 바위 가로) 중 랜덤으로 바위의 위치 설정
    rockY = 0
    rockSpeed = 2  # 바위가 떨어지는 속도

    isShot = False
    shotCount = 0
    rockPassed = 0


    onGame = False
    while not onGame:
        for event in pygame.event.get():  # 창에서 키보드 입력 등 이벤트 효과처리
            if event.type in [pygame.QUIT]: # 창 닫으면 종료
                pygame.quit()
                sys.exit()

            if event.type in [pygame.KEYDOWN]: # 키보드가 눌렸을 때 반응
                if event.key == pygame.K_LEFT: # 화살표 왼쪽
                    fighterX -= 5

                elif event.key == pygame.K_RIGHT: # 화살표 오른쪽
                    fighterX += 5

                elif event.key == pygame.K_SPACE: # 스페이스바
                    missileSound.play() # 미사일 발사 소리 재생
                    missileX = x + fighterWidth / 2   # 전투기의 가운데에서 발사 (x는 현재 전투기의 x 위치)
                    missileY = y - fighterHeight  # 전투기에서 발사 (y는 현재 전투기의 y 위치)
                    missileXY.append([missileX, missileY])  # 미사일 객체를 리스트에 넣어줌 (미사일 X, Y 좌표값)

            if event.type in [pygame.KEYUP]: # 키보드가 떼졌을 때 반응
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighterX = 0

        drawObject(background, 0, 0)

        x += fighterX  # 키보드 누른 것에 대한 전투기 X 좌표
        if x < 0: # 전투기가 왼쪽에서 벗어나지 못하도록 처리
            x = 0
        elif x > padWidth - fighterWidth: # 전투기가 오른쪽으로 벗어나지 못하도록 처리
            x = padWidth - fighterWidth

        if y < rockY + rockHeight: # 전투기의 y 좌표 위치
            if (rockX > x and rockX < x + fighterWidth) or \
                    (rockX + rockWidth > x and rockX + rockWidth < x + fighterWidth): # 전투기와 바위가 부딪혔을 때
                crash()

        drawObject(fighter, x, y) # 비행기 이미지를 x, y 좌표로 창에 그림

        if len(missileXY) != 0:
            for i, bxy in enumerate(missileXY):  # i는 몇번째인지, bxy는 미사일의 (x, y) 좌표
                bxy[1] -= 10 # bxy의 y 좌표 : 미사일이 위로 올라가도록 설정
                missileXY[i][1] = bxy[1] # 리스트에 들어있는 미사일 Y 좌표 설정

                if bxy[1] < rockY:  # 미사일의 Y좌표가 바위의 Y좌표보다 작은 경우
                    if bxy[0] > rockX and bxy[0] < rockX + rockWidth: # 바위 X 좌표 < 미사일 X 좌표 < 바위 X 좌표 + 바위 가로길이
                        missileXY.remove(bxy) # 미사일 삭제
                        isShot = True
                        shotCount += 1

                if bxy[1] <= 0: # 미사일 화면 밖으로
                    try:
                        missileXY.remove(bxy)
                    except:
                        pass

        if len(missileXY) != 0: # 미사일 그리기
            for bx, by in missileXY:
                drawObject(missile, bx, by)

        writeScore(shotCount)

        rockY += rockSpeed # 바위 Y 좌표 증가 ( 바위가 떨어지게 )

        if rockY > padHeight: # 바위 Y 위치가 창에서 벗어날 경우
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