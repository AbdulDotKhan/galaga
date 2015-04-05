#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Abdul Kadir
#
# Created:     01/06/2012
# Copyright:   (c) Abdul Kadir 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from pygame import *
from random import *
from sys import *
import pygame, sys, random

WHITE =255,255,255 # background
BLUE = 0,0,255
RED = 255,0,0
GREEN = 0,255,0
YELLOW = 255,255,0
PURPLE = 255,0,255
BLACK = 0,0,0
NUM_COLOURS = 7

WIDTH = 600
HEIGHT = 600
FPS = 40
SMALLEST = 10
LARGEST = 40
SLOWEST = 1
FASTEST = 4

playerSpeed = 5

# set up pygame, the window, and the mouse cursor
init()
mainClock = time.Clock()
screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption('Galaga')
mouse.set_visible(False)
enemyImageList = (image.load('ship_bad.png'), image.load('enemy2.png'), image.load('enemy3.png'), image.load('enemy4.png'))

# set up fonts
font = font.SysFont(None, 48)

# set up sounds
gameOverSound = mixer.Sound('gameover.wav')
shotSound = mixer.Sound('shot_weapon.wav')
mixer.music.load('background3.wav')

# set up images
playerImage = transform.scale(image.load('ship.png'),(30,32))
playerRect = playerImage.get_rect()
baddieImage = image.load('ship_bad.png')
screen.fill(BLACK)
game = True
main = True
gameOver = False

# Functions
#=============================================================================#
def doNothing():
    pass

def terminate():
    quit()
    exit()

def checkForQuit():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    pygame.quit()
                    sys.exit()
                return


def collisionCheck(playerRect, enemies):
    for e in enemies:
        if playerRect.colliderect(e['rect']):   ##checks if your object collides
            return True                         ##with baddie (b['rect'])
    return False

def drawText(text, font, surface, x, y, color):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    screen.blit(textobj, textrect)

def drawTextCenter(text,font, surface, x, y, color):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    screen.blit(textobj, textrect)

def drawTextTopRight(text, font, surface, x, y, color):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topright = (x, y)
    screen.blit(textobj, textrect)

def takeInput(slowCheat, reverseCheat, moveLeft, moveRight, moveUp, moveDown, playerRect, projectileCtr, addProjectile, scoreZero, playerImage):
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()

            ##movement commands
        if event.type == KEYDOWN:
            if event.key == ord('z'):
                reverseCheat = True
            if event.key == ord('x'):
                slowCheat = True
            if event.key == K_LEFT or event.key == ord('a'):
                moveRight = False
                moveLeft = True
            if event.key == K_RIGHT or event.key == ord('d'):
                moveLeft = False
                moveRight = True
            if event.key == K_UP or event.key == ord('w'):
                moveDown = False
                moveUp = True
            if event.key == K_DOWN or event.key == ord('s'):
                moveUp = False
                moveDown = True
            if event.key == K_SPACE:
                if projectileCtr > 10:
                    addProjectile = True
                    projectileCtr = 0

        if event.type == KEYUP:
            if event.key == ord('z'):
                reverseCheat = False
                scoreZero = True
            if event.key == ord('x'):
                slowCheat = False
                scoreZero = True
##            if  event.key == ord('c'):
##                if currentImage == playerImage[0]:
##                    currentImage == playerImage[1]
##                else:
##                    currentImage = playerImage[0]
            if event.key == K_ESCAPE:
                    terminate()
            if event.key == K_LEFT or event.key == ord('a'):
                moveLeft = False
            if event.key == K_RIGHT or event.key == ord('d'):
                moveRight = False
            if event.key == K_UP or event.key == ord('w'):
                moveUp = False
            if event.key == K_DOWN or event.key == ord('s'):
                moveDown = False

        if event.type == MOUSEMOTION:
            # If the mouse moves, move the player where the cursor is.   (x,y) ##ip= in place
            playerRect.move_ip(event.pos[0] - playerRect.centerx, event.pos[1] - playerRect.centery)
    return (slowCheat, reverseCheat, moveLeft, moveRight, moveUp, moveDown, playerRect, projectileCtr, addProjectile, scoreZero, playerImage)

def movePlayer(playerRect, moveLeft, moveRight, moveUp, moveDown, playerSpeed):
    if moveLeft and playerRect.left > 0:
        playerRect.move_ip(-1 * playerSpeed, 0)
    if moveRight and playerRect.right < WIDTH:
        playerRect.move_ip(playerSpeed, 0)
    if moveUp and playerRect.top > 0:
        playerRect.move_ip(0, -1 * playerSpeed)
    if moveDown and playerRect.bottom < HEIGHT:
        playerRect.move_ip(0, playerSpeed)
    return playerRect

def projectileToEnemy(projectiles, enemies):
    for p in projectiles:
        numCollisions = 0
        p['y'] -= 6
        pRect = Rect(p['x']-2, p['y']-20, 4, 20)
        for e in enemies:
            if pRect.colliderect(e['rect']):
                enemies.remove(e)
                numCollisions +=1
        if numCollisions > 0:
            projectiles.remove(p)
            return True
    return False

def deleteEnemiesPastBottom(enemies):
    for e in enemies:
        if e['rect'].top > HEIGHT:
            enemies.remove(e)

def deleteEnemyProjectilesPastBottom(enemyProjectiles):
    for p in enemyProjectiles:
         if p['y'] > HEIGHT:
             enemyProjectiles.remove(p)

def deleteProjectilesPastTop(projectiles):
    for p in projectiles:
         if p['y'] < 0:
             projectiles.remove(p)

def drawEverything(score, hp, topScore, playerImage, playerRect, enemies, projectiles, enemyProjectiles, drawTopScore):
    screen.fill(BLACK)

    # score, top score
    drawText('Score: ' + str(score), font, screen, 10, 0, WHITE)
    drawTextTopRight('HP: ' + str(hp), font, screen, WIDTH, 0, WHITE)
    if drawTopScore:
        drawText('Top Score: ' + str(topScore), font, screen, 10, 40, WHITE)

    # player
    screen.blit(playerImage, playerRect)

    # Draw each baddie
    for b in enemies:
        screen.blit(b['surface'], b['rect'])

    # friendly projectiles
    for p in projectiles:
        p['y'] += 2
        pRect = Rect(p['x']-2, p['y']-20, 4, 20)
        draw.rect(screen, BLUE, pRect)

    # enemy projectiles
    for p in enemyProjectiles:
        p['y'] += 8
        pRect = Rect(p['x']-2, p['y']-20, 4, 20)
        draw.rect(screen, RED, pRect)

topScore = 0
tf = (True, False)

while main:

    # reset values
    enemies = []    ##empty list to add to
    projectiles = []
    enemyProjectiles = []
    playerRect.center = (WIDTH / 2, HEIGHT - 50)
    score = 0
    moveLeft = moveRight = moveUp = moveDown = False
    scoreZero = False
    reverseCheat = slowCheat = False
    addProjectile = False
    projectileCtr = 0
    hp = 30
    ctr = 0
    cont = False

    mixer.music.play(-1, 0.0) # music

    screen.fill(BLACK)
    display.flip()

    # level system
    lvl1 = True
    lvl2 = False
    lvl3 = False
    lvl4 = False
    lvl5 = False
    infinite = False

    screen.fill(BLACK)
    drawTextCenter('Level 1',font, screen, WIDTH // 2, HEIGHT // 2, WHITE)
    display.flip()
    time.delay(500)
    checkForQuit()

    # ======================= level 1 begins ==================================#

    while lvl1:
        ctr += 1
        projectileCtr += 1
        scoreZero = False
        baddieImage = enemyImageList[0]
        # Checking For Input - returns (slowCheat, reverseCheat, moveLeft, moveRight, moveUp, moveDown, playerRect, projectileCtr)
        boolList = takeInput(slowCheat, reverseCheat, moveLeft, moveRight, moveUp, moveDown, playerRect, projectileCtr, addProjectile, scoreZero, playerImage)
        reverseCheat = boolList[1]
        moveLeft = boolList[2]
        moveRight = boolList[3]
        moveUp = boolList[4]
        moveDown = boolList[5]
        playerRect = boolList[6]
        projectileCtr = boolList[7]
        addProjectile = boolList[8]
        scoreZero = boolList[9]
        playerImage = boolList[10]


        # Add new baddies at the top of the screen, if needed.
        if not reverseCheat and not slowCheat and ctr % 30 == 0:
            enemySize = randint(15,45)
            newBaddie = {'rect': Rect(randint(0, WIDTH-enemySize), 0 - enemySize, enemySize, enemySize),
                        'speed': randint(SLOWEST, FASTEST),
                        'surface':transform.scale(baddieImage, (enemySize, enemySize)),
                        }
            enemies.append(newBaddie)

        # Move the player around.
        playerRect = movePlayer(playerRect, moveLeft, moveRight, moveUp, moveDown, playerSpeed)

        # add projectiles
        if addProjectile:
            projectiles.append({'x':playerRect.centerx, 'y':playerRect.top})
            addProjectile = False
            shotSound.play()
        # Move the mouse cursor to match the player.
        mouse.set_pos(playerRect.centerx, playerRect.centery)

        # Move the baddies down.
        for b in enemies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
                decision = tf[randint(0,1)]
                if decision == True and ctr % randint(50,100) == 0:
                    enemyProjectiles.append({'x':b['rect'].centerx, 'y':b['rect'].top})
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

        # delete stuff out of bounds
        deleteEnemiesPastBottom(enemies)
        deleteEnemyProjectilesPastBottom(enemyProjectiles)
        deleteProjectilesPastTop(projectiles)


        for p in enemyProjectiles:
            if p['y'] > HEIGHT:
                enemyProjectiles.remove(p)

        if projectileToEnemy(projectiles, enemies):
            score += 10

        if scoreZero:
            score = 0


        drawEverything(score, hp, topScore, playerImage, playerRect, enemies, projectiles, enemyProjectiles, False)
        display.update()

        # Check if any of the baddies have hit the player.
        if collisionCheck(playerRect, enemies):
            hp -= 10

        for p in enemyProjectiles:
            epRect = Rect(p['x']-2, p['y']-20, 4, 20)
            if epRect.colliderect(playerRect):
                hp -= 10
                enemyProjectiles.remove(p)



        if hp <= 0:
            if score > topScore:
                topScore = score # set new top score
            gameOver = True
            break

        if score >= 100:
            cont = True
            break
        mainClock.tick(FPS) ##updates clock

    time.delay(1000)

    if cont:
        lvl1 = False
        lvl2 = True
        lvl3 = False
        lvl4 = False
        lvl5 = False
        infinite = False
        # reset values
        enemies = []    ##empty list to add to
        projectiles = []
        enemyProjectiles = []
        playerRect.center = (WIDTH / 2, HEIGHT - 50)
        score = 0
        moveLeft = moveRight = moveUp = moveDown = False
        scoreZero = False
        reverseCheat = slowCheat = False
        addProjectile = False
        projectileCtr = 0
        hp = 30
        ctr = 0
        cont = False
        screen.fill(BLACK)
        display.flip()
        time.delay(500)
        drawTextCenter('Level 2',font, screen, WIDTH // 2, HEIGHT // 2, WHITE)
        display.flip()
        time.delay(500)
        checkForQuit()

    elif gameOver:
        time.delay(500)
        screen.fill(BLACK)
        drawTextCenter('Game Over',font, screen, WIDTH // 2, HEIGHT // 2, WHITE)
        display.flip()
        time.delay(500)
        screen.fill(BLACK)
        display.flip()
        time.delay(500)
        drawTextCenter('Game Over',font, screen, WIDTH // 2, HEIGHT // 2, WHITE)
        display.flip()
        time.delay(500)
        screen.fill(BLACK)
        display.flip()
        time.delay(500)
        drawTextCenter('Game Over',font, screen, WIDTH // 2, HEIGHT // 2, WHITE)
        time.delay(500)

        lvl1 = True
        lvl2 = False
        lvl3 = False
        lvl4 = False
        lvl5 = False
        infinite = False
        gameOver = False
        checkForQuit()


# =========================== level 2 begins ================================= #

    while lvl2:
        ctr += 1
        projectileCtr += 1
        scoreZero = False
        baddieImage = image.load('enemy2.png')

        # Checking For Input - returns (slowCheat, reverseCheat, moveLeft, moveRight, moveUp, moveDown, playerRect, projectileCtr)
        boolList = takeInput(slowCheat, reverseCheat, moveLeft, moveRight, moveUp, moveDown, playerRect, projectileCtr, addProjectile, scoreZero, playerImage)
        slowCheat = boolList[0]
        reverseCheat = boolList[1]
        moveLeft = boolList[2]
        moveRight = boolList[3]
        moveUp = boolList[4]
        moveDown = boolList[5]
        playerRect = boolList[6]
        projectileCtr = boolList[7]
        addProjectile = boolList[8]
        scoreZero = boolList[9]
        playerImage = boolList[10]


        # Add new baddies at the top of the screen, if needed.
        if not reverseCheat and not slowCheat and ctr % 24 == 0:
            enemySize = randint(15,45)
            newBaddie = {'rect': Rect(randint(0, WIDTH-enemySize), 0 - enemySize, enemySize, enemySize),
                        'speed': randint(SLOWEST, FASTEST),
                        'surface':transform.scale(baddieImage, (enemySize, enemySize)),
                        }
            enemies.append(newBaddie)

        # Move the player around.
        playerRect = movePlayer(playerRect, moveLeft, moveRight, moveUp, moveDown, playerSpeed)

        # add projectiles
        if addProjectile:
            projectiles.append({'x':playerRect.centerx, 'y':playerRect.top})
            addProjectile = False
            shotSound.play()
        # Move the mouse cursor to match the player.
        mouse.set_pos(playerRect.centerx, playerRect.centery)

        # Move the baddies down.
        for b in enemies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
                decision = tf[randint(0,1)]
                if decision == True and ctr % randint(50,100) == 0:
                    enemyProjectiles.append({'x':b['rect'].centerx, 'y':b['rect'].top})
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

        # delete stuff out of bounds
        deleteEnemiesPastBottom(enemies)
        deleteEnemyProjectilesPastBottom(enemyProjectiles)
        deleteProjectilesPastTop(projectiles)


        for p in enemyProjectiles:
            if p['y'] > HEIGHT:
                enemyProjectiles.remove(p)

        if projectileToEnemy(projectiles, enemies):
            score += 10

        if scoreZero:
            score = 0


        drawEverything(score, hp, topScore, playerImage, playerRect, enemies, projectiles, enemyProjectiles, False)
        display.update()

        # Check if any of the baddies have hit the player.
        if collisionCheck(playerRect, enemies):
            if score > topScore:
                topScore = score # set new top score
            hp -= 10

        for p in enemyProjectiles:
            epRect = Rect(p['x']-2, p['y']-20, 4, 20)
            if epRect.colliderect(playerRect):
                hp -= 10
                enemyProjectiles.remove(p)

        if hp <= 0:
            gameOver = True
            break


        if score >= 100:
            cont = True
            break
        mainClock.tick(FPS) ##updates clock

    if cont:
        lvl1 = False
        lvl2 = False
        lvl3 = True
        lvl4 = False
        lvl5 = False
        infinite = False
        # reset values
        enemies = []    ##empty list to add to
        projectiles = []
        enemyProjectiles = []
        playerRect.center = (WIDTH / 2, HEIGHT - 50)
        score = 0
        moveLeft = moveRight = moveUp = moveDown = False
        scoreZero = False
        reverseCheat = slowCheat = False
        addProjectile = False
        projectileCtr = 0
        hp = 30
        ctr = 0
        cont = False
        screen.fill(BLACK)
        display.flip()
        time.delay(500)
        drawTextCenter('Level 3',font, screen, WIDTH // 2, HEIGHT // 2, WHITE)
        display.flip()
        time.delay(500)
        checkForQuit()

    elif gameOver:
        time.delay(500)
        screen.fill(BLACK)
        drawTextCenter('Game Over',font, screen, WIDTH // 2, HEIGHT // 2, WHITE)
        display.flip()
        time.delay(500)
        screen.fill(BLACK)
        display.flip()
        time.delay(500)
        drawTextCenter('Game Over',font, screen, WIDTH // 2, HEIGHT // 2, WHITE)
        display.flip()
        time.delay(500)
        screen.fill(BLACK)
        display.flip()
        time.delay(500)
        drawTextCenter('Game Over',font, screen, WIDTH // 2, HEIGHT // 2, WHITE)
        time.delay(500)
        lvl1 = True
        lvl2 = False
        lvl3 = False
        lvl4 = False
        lvl5 = False
        infinite = False
        gameOver = False
# ========================= level 3 begins =================================== #

    while lvl3:
        ctr += 1
        projectileCtr += 1
        scoreZero = False
        baddieImage = image.load('enemy3.png')

        # Checking For Input - returns (slowCheat, reverseCheat, moveLeft, moveRight, moveUp, moveDown, playerRect, projectileCtr)
        boolList = takeInput(slowCheat, reverseCheat, moveLeft, moveRight, moveUp, moveDown, playerRect, projectileCtr, addProjectile, scoreZero, playerImage)
        slowCheat = boolList[0]
        reverseCheat = boolList[1]
        moveLeft = boolList[2]
        moveRight = boolList[3]
        moveUp = boolList[4]
        moveDown = boolList[5]
        playerRect = boolList[6]
        projectileCtr = boolList[7]
        addProjectile = boolList[8]
        scoreZero = boolList[9]
        playerImage = boolList[10]



        # Add new baddies at the top of the screen, if needed.
        if not reverseCheat and not slowCheat and ctr % 18 == 0:
            enemySize = randint(15,45)
            newBaddie = {'rect': Rect(randint(0, WIDTH-enemySize), 0 - enemySize, enemySize, enemySize),
                        'speed': randint(SLOWEST, FASTEST),
                        'surface':transform.scale(baddieImage, (enemySize, enemySize)),
                        }
            enemies.append(newBaddie)

        # Move the player around.
        playerRect = movePlayer(playerRect, moveLeft, moveRight, moveUp, moveDown, playerSpeed)

        # add projectiles
        if addProjectile:
            projectiles.append({'x':playerRect.centerx, 'y':playerRect.top})
            addProjectile = False
            shotSound.play()
        # Move the mouse cursor to match the player.
        mouse.set_pos(playerRect.centerx, playerRect.centery)

        # Move the baddies down.
        for b in enemies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
                decision = tf[randint(0,1)]
                if decision == True and ctr % randint(50,100) == 0:
                    enemyProjectiles.append({'x':b['rect'].centerx, 'y':b['rect'].top})
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

        # delete stuff out of bounds
        deleteEnemiesPastBottom(enemies)
        deleteEnemyProjectilesPastBottom(enemyProjectiles)
        deleteProjectilesPastTop(projectiles)


        for p in enemyProjectiles:
            if p['y'] > HEIGHT:
                enemyProjectiles.remove(p)

        if projectileToEnemy(projectiles, enemies):
            score += 10

        if scoreZero:
            score = 0


        drawEverything(score, hp, topScore, playerImage, playerRect, enemies, projectiles, enemyProjectiles, False)
        display.update()

        # Check if any of the baddies have hit the player.
        if collisionCheck(playerRect, enemies):
            if score > topScore:
                topScore = score # set new top score
            hp -= 10

        for p in enemyProjectiles:
            epRect = Rect(p['x']-2, p['y']-20, 4, 20)
            if epRect.colliderect(playerRect):
                hp -= 10
                enemyProjectiles.remove(p)



        if hp <= 0:
            gameOver = True
            break

        if score >= 100:
            cont = True
            break
        mainClock.tick(FPS) ##updates clock

    if cont:
        lvl1 = False
        lvl2 = False
        lvl3 = False
        lvl4 = True
        lvl5 = False
        infinite = False
        # reset values
        enemies = []    ##empty list to add to
        projectiles = []
        enemyProjectiles = []
        playerRect.center = (WIDTH / 2, HEIGHT - 50)
        score = 0
        moveLeft = moveRight = moveUp = moveDown = False
        scoreZero = False
        reverseCheat = slowCheat = False
        addProjectile = False
        projectileCtr = 0
        hp = 30
        ctr = 0
        cont = False
        screen.fill(BLACK)
        display.flip()
        time.delay(500)
        drawTextCenter('Level 4',font, screen, WIDTH // 2, HEIGHT // 2, WHITE)
        display.flip()
        time.delay(500)
        checkForQuit()

    elif gameOver:
        time.delay(500)
        screen.fill(BLACK)
        drawTextCenter('Game Over',font, screen, WIDTH // 2, HEIGHT // 2, WHITE)
        display.flip()
        time.delay(500)
        screen.fill(BLACK)
        display.flip()
        time.delay(500)
        drawTextCenter('Game Over',font, screen, WIDTH // 2, HEIGHT // 2, WHITE)
        display.flip()
        time.delay(500)
        screen.fill(BLACK)
        display.flip()
        time.delay(500)
        drawTextCenter('Game Over',font, screen, WIDTH // 2, HEIGHT // 2, WHITE)
        time.delay(500)

        lvl1 =True
        lvl2 = False
        lvl3 = False
        lvl4 = False
        lvl5 = False
        infinite = False
        gameOver = False
        checkForQuit()

# ============================ level 4 begins ================================ #
    while lvl4:
        ctr += 1
        projectileCtr += 1
        scoreZero = False
        baddieImage = image.load('enemy4.png')

        # Checking For Input - returns (slowCheat, reverseCheat, moveLeft, moveRight, moveUp, moveDown, playerRect, projectileCtr)
        boolList = takeInput(slowCheat, reverseCheat, moveLeft, moveRight, moveUp, moveDown, playerRect, projectileCtr, addProjectile, scoreZero, playerImage)
        slowCheat = boolList[0]
        reverseCheat = boolList[1]
        moveLeft = boolList[2]
        moveRight = boolList[3]
        moveUp = boolList[4]
        moveDown = boolList[5]
        playerRect = boolList[6]
        projectileCtr = boolList[7]
        addProjectile = boolList[8]
        scoreZero = boolList[9]
        playerImage = boolList[10]


        # Add new baddies at the top of the screen, if needed.
        if not reverseCheat and not slowCheat and ctr % 12 == 0:
            enemySize = randint(15,45)
            newBaddie = {'rect': Rect(randint(0, WIDTH-enemySize), 0 - enemySize, enemySize, enemySize),
                        'speed': randint(SLOWEST, FASTEST),
                        'surface':transform.scale(baddieImage, (enemySize, enemySize)),
                        }
            enemies.append(newBaddie)

        # Move the player around.
        playerRect = movePlayer(playerRect, moveLeft, moveRight, moveUp, moveDown, playerSpeed)

        # add projectiles
        if addProjectile:
            projectiles.append({'x':playerRect.centerx, 'y':playerRect.top})
            addProjectile = False
            shotSound.play()
        # Move the mouse cursor to match the player.
        mouse.set_pos(playerRect.centerx, playerRect.centery)

        # Move the baddies down.
        for b in enemies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
                decision = tf[randint(0,1)]
                if decision == True and ctr % randint(50,100) == 0:
                    enemyProjectiles.append({'x':b['rect'].centerx, 'y':b['rect'].top})
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

        # delete stuff out of bounds
        deleteEnemiesPastBottom(enemies)
        deleteEnemyProjectilesPastBottom(enemyProjectiles)
        deleteProjectilesPastTop(projectiles)


        for p in enemyProjectiles:
            if p['y'] > HEIGHT:
                enemyProjectiles.remove(p)

        if projectileToEnemy(projectiles, enemies):
            score += 10

        if scoreZero:
            score = 0


        drawEverything(score, hp, topScore, playerImage, playerRect, enemies, projectiles, enemyProjectiles, False)
        display.update()

        # Check if any of the baddies have hit the player.
        if collisionCheck(playerRect, enemies):
            if score > topScore:
                topScore = score # set new top score
            hp -= 10

        for p in enemyProjectiles:
            epRect = Rect(p['x']-2, p['y']-20, 4, 20)
            if epRect.colliderect(playerRect):
                hp -= 10
                enemyProjectiles.remove(p)



        if hp <= 0:
            gameOver = True
            break

        if score >= 100:
            cont = True
            break
        mainClock.tick(FPS) ##updates clock

    if cont:
        lvl1 = False
        lvl2 = False
        lvl3 = False
        lvl4 = False
        lvl5 = True
        infinite = False
        # reset values
        enemies = []    ##empty list to add to
        projectiles = []
        enemyProjectiles = []
        playerRect.center = (WIDTH / 2, HEIGHT - 50)
        score = 0
        moveLeft = moveRight = moveUp = moveDown = False
        scoreZero = False
        reverseCheat = slowCheat = False
        addProjectile = False
        projectileCtr = 0
        hp = 30
        ctr = 0
        cont = False
        screen.fill(BLACK)
        display.flip()
        time.delay(500)
        drawTextCenter('Level 5',font, screen, WIDTH // 2, HEIGHT // 2, WHITE)
        display.flip()
        time.delay(500)
        checkForQuit()

    elif gameOver:
        time.delay(500)
        screen.fill(BLACK)
        drawTextCenter('Game Over',font, screen, WIDTH // 2, HEIGHT // 2, WHITE)
        display.flip()
        time.delay(500)
        screen.fill(BLACK)
        display.flip()
        time.delay(500)
        drawTextCenter('Game Over',font, screen, WIDTH // 2, HEIGHT // 2, WHITE)
        display.flip()
        time.delay(500)
        screen.fill(BLACK)
        display.flip()
        time.delay(500)
        drawTextCenter('Game Over',font, screen, WIDTH // 2, HEIGHT // 2, WHITE)
        time.delay(500)

        lvl1 =True
        lvl2 = False
        lvl3 = False
        lvl4 = False
        lvl5 = False
        infinite = False
        gameOver =  False
        checkForQuit()
# ============================= level 5 begins =============================== #

    while lvl5:
        ctr += 1
        projectileCtr += 1
        scoreZero = False

        # Checking For Input - returns (slowCheat, reverseCheat, moveLeft, moveRight, moveUp, moveDown, playerRect, projectileCtr)
        boolList = takeInput(slowCheat, reverseCheat, moveLeft, moveRight, moveUp, moveDown, playerRect, projectileCtr, addProjectile, scoreZero, playerImage)
        slowCheat = boolList[0]
        reverseCheat = boolList[1]
        moveLeft = boolList[2]
        moveRight = boolList[3]
        moveUp = boolList[4]
        moveDown = boolList[5]
        playerRect = boolList[6]
        projectileCtr = boolList[7]
        addProjectile = boolList[8]
        scoreZero = boolList[9]
        playerImage = boolList[10]


        # Add new baddies at the top of the screen, if needed.
        if not reverseCheat and not slowCheat and ctr % 6 == 0:
            enemySize = randint(15,45)
            newBaddie = {'rect': Rect(randint(0, WIDTH-enemySize), 0 - enemySize, enemySize, enemySize),
                        'speed': randint(SLOWEST, FASTEST),
                        'surface':transform.scale(enemyImageList[randint(0,3)], (enemySize, enemySize)),
                        }
            enemies.append(newBaddie)

        # Move the player around.
        playerRect = movePlayer(playerRect, moveLeft, moveRight, moveUp, moveDown, playerSpeed)

        # add projectiles
        if addProjectile:
            projectiles.append({'x':playerRect.centerx, 'y':playerRect.top})
            addProjectile = False
            shotSound.play()
        # Move the mouse cursor to match the player.
        mouse.set_pos(playerRect.centerx, playerRect.centery)

        # Move the baddies down.
        for b in enemies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
                decision = tf[randint(0,1)]
                if decision == True and ctr % randint(50,100) == 0:
                    enemyProjectiles.append({'x':b['rect'].centerx, 'y':b['rect'].top})
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

        # delete stuff out of bounds
        deleteEnemiesPastBottom(enemies)
        deleteEnemyProjectilesPastBottom(enemyProjectiles)
        deleteProjectilesPastTop(projectiles)


        for p in enemyProjectiles:
            if p['y'] > HEIGHT:
                enemyProjectiles.remove(p)

        if projectileToEnemy(projectiles, enemies):
            score += 10

        if scoreZero:
            score = 0


        drawEverything(score, hp, topScore, playerImage, playerRect, enemies, projectiles, enemyProjectiles, False)
        display.update()

        # Check if any of the baddies have hit the player.
        if collisionCheck(playerRect, enemies):
            if score > topScore:
                topScore = score # set new top score
            hp -= 10

        for p in enemyProjectiles:
            epRect = Rect(p['x']-2, p['y']-20, 4, 20)
            if epRect.colliderect(playerRect):
                hp -= 10
                enemyProjectiles.remove(p)



        if hp <= 0:
            gameOver = True
            break
        if score >= 100:
            cont = True
            break
        mainClock.tick(FPS) ##updates clock
    # Stop the game and show the "Game Over" screen.

    if cont:
        lvl1 = False
        lvl2 = False
        lvl3 = False
        lvl4 = False
        lvl5 = False
        infinite = True
        # reset values
        enemies = []    ##empty list to add to
        projectiles = []
        enemyProjectiles = []
        playerRect.center = (WIDTH / 2, HEIGHT - 50)
        score = 0
        moveLeft = moveRight = moveUp = moveDown = False
        scoreZero = False
        reverseCheat = slowCheat = False
        addProjectile = False
        projectileCtr = 0
        hp = 30
        ctr = 0
        cont = False
        screen.fill(BLACK)
        display.flip()
        time.delay(500)
        drawTextCenter('Infinite Mode',font, screen, WIDTH // 2, HEIGHT // 2, WHITE)
        display.flip()
        time.delay(500)
        checkForQuit()

    elif gameOver:
        time.delay(500)
        screen.fill(BLACK)
        drawTextCenter('Game Over',font, screen, WIDTH // 2, HEIGHT // 2, WHITE)
        display.flip()
        time.delay(500)
        screen.fill(BLACK)
        display.flip()
        time.delay(500)
        drawTextCenter('Game Over',font, screen, WIDTH // 2, HEIGHT // 2, WHITE)
        display.flip()
        time.delay(500)
        screen.fill(BLACK)
        display.flip()
        time.delay(500)
        drawTextCenter('Game Over',font, screen, WIDTH // 2, HEIGHT // 2, WHITE)
        time.delay(500)

        lvl1 =True
        lvl2 = False
        lvl3 = False
        lvl4 = False
        lvl5 = False
        infinite = False
        checkForQuit()
# =========================== infinite mode begins =========================== #
    while infinite:
        ctr += 1
        projectileCtr += 1
        scoreZero = False
        # Checking For Input - returns (slowCheat, reverseCheat, moveLeft, moveRight, moveUp, moveDown, playerRect, projectileCtr)
        boolList = takeInput(slowCheat, reverseCheat, moveLeft, moveRight, moveUp, moveDown, playerRect, projectileCtr, addProjectile, scoreZero, playerImage)
        slowCheat = boolList[0]
        reverseCheat = boolList[1]
        moveLeft = boolList[2]
        moveRight = boolList[3]
        moveUp = boolList[4]
        moveDown = boolList[5]
        playerRect = boolList[6]
        projectileCtr = boolList[7]
        addProjectile = boolList[8]
        scoreZero = boolList[9]
        playerImage = boolList[10]



        # Add new baddies at the top of the screen, if needed.
        if not reverseCheat and not slowCheat and ctr % 6 == 0:
            enemySize = randint(15,45)
            newBaddie = {'rect': Rect(randint(0, WIDTH-enemySize), 0 - enemySize, enemySize, enemySize),
                        'speed': randint(SLOWEST, FASTEST),
                        'surface':transform.scale(enemyImageList[randint(0,3)], (enemySize, enemySize)),
                        }
            enemies.append(newBaddie)

        # Move the player around.
        playerRect = movePlayer(playerRect, moveLeft, moveRight, moveUp, moveDown, playerSpeed)

        # add projectiles
        if addProjectile:
            projectiles.append({'x':playerRect.centerx, 'y':playerRect.top})
            addProjectile = False
            shotSound.play()
        # Move the mouse cursor to match the player.
        mouse.set_pos(playerRect.centerx, playerRect.centery)

        # Move the baddies down.
        for b in enemies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
                decision = tf[randint(0,1)]
                if decision == True and ctr % randint(50,100) == 0:
                    enemyProjectiles.append({'x':b['rect'].centerx, 'y':b['rect'].top})
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

        # delete stuff out of bounds
        deleteEnemiesPastBottom(enemies)
        deleteEnemyProjectilesPastBottom(enemyProjectiles)
        deleteProjectilesPastTop(projectiles)


        for p in enemyProjectiles:
            if p['y'] > HEIGHT:
                enemyProjectiles.remove(p)

        if projectileToEnemy(projectiles, enemies):
            score += 10

        if scoreZero:
            score = 0


        drawEverything(score, hp, topScore, playerImage, playerRect, enemies, projectiles, enemyProjectiles, False)
        display.update()

        # Check if any of the baddies have hit the player.
        if collisionCheck(playerRect, enemies):
            if score > topScore:
                topScore = score # set new top score
            hp -= 10

        for p in enemyProjectiles:
            epRect = Rect(p['x']-2, p['y']-20, 4, 20)
            if epRect.colliderect(playerRect):
                hp -= 10
                enemyProjectiles.remove(p)



        if hp <= 0:
            break
        mainClock.tick(FPS) ##updates clock

    mixer.music.stop()
    gameOverSound.play()
    # Draw the score and top score.
    time.delay(500)
    drawText('Press a key to play again.', font, screen, (WIDTH / 3) - 80, (HEIGHT / 3) + 50, WHITE)
    display.update()
    time.delay(750)
    checkForQuit()

    gameOverSound.stop()
