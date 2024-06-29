import random
import math
import pygame
from pygame import mixer
pygame.init()
screen=pygame.display.set_mode((800,600))
running=True

pygame.display.set_caption("Space Invader")
icon = pygame.image.load('assets/ufo.png')
pygame.display.set_icon(icon)

background = pygame.image.load('assets/background.png')
mixer.music.load("assets/background.wav")
mixer.music.set_volume(0.35)
mixer.music.play(-1)

score_value=0
font = pygame.font.Font('freesansbold.ttf', 27)

textX = 10
textY = 10
over_font = pygame.font.Font('freesansbold.ttf', 64)

#text-showing funcs
def show_score(x,y):
    score=font.render("Score : "+str(score_value),True,(255,255,255))
    screen.blit(score, (x, y))
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))



#player vars and funcs
playerImg = pygame.image.load('assets/player.png')
playerX = 370
playerY = 480
playerX_change = 0
def player(x, y):
    screen.blit(playerImg, (x, y))



enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('assets/enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(28)


def enemy(x, y, i):
    screen.blit(enemyImg[i],(x, y))


#bullet vars and funcs
bulletImg = pygame.image.load('assets/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 7
bullet_state = "ready"
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False



while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

        #for keystroke detecshun
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                playerX_change= -3
            if event.key == pygame.K_RIGHT:
                playerX_change= 3
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound("assets/laser.wav")
                    bulletSound.play()
                    bulletX=playerX
                    fire_bullet(bulletX,bulletY)
        if event.type==pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                playerX_change=0

    #updating player coords
    playerX+=playerX_change
    if playerX<=0:
        playerX=0
    elif playerX>=736:
        playerX=736
    player(playerX,playerY)


    # updating enemy coords
    for i in range(num_of_enemies):
        if enemyY[i]> 440:
            for j in range(num_of_enemies):
                enemyY[j]=2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i]=2
            enemyY[i]+= enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] +=  enemyY_change[i]
        # for collision handling zzzzz
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("assets/explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i],enemyY[i],i)


    # updating bullet coords
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    show_score(textX,textY)
    pygame.display.update()



