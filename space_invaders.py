import pygame, random, math
from pygame import mixer

# initialize pygame
pygame.init()
# initialize the music mixer
pygame.mixer.init()

# game screen
GAME_SCREEN = pygame.display.set_mode((800, 600))
background_image = pygame.transform.scale(pygame.image.load("./background.jpg"), (800, 600))

# icon, title
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("./ufo.png")
pygame.display.set_icon(icon)

# Player spaceship
PLAYER = pygame.transform.scale(pygame.image.load("./space.png"), (50,50))
playerX = 375
playerY = 550
playerX_change = 0.4
playerY_change = 0.4

# bullet
BULLET = pygame.image.load("./bullet.png")
bulletX = 0
bulletY = playerY - 24
bulletY_change = 1
bullet_state = "ready"

# UFO spaceship
ENEMY = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
side = []
num_of_enemies = 6

for i in range(num_of_enemies):
    ENEMY.append(pygame.transform.scale(pygame.image.load("./ufo.png"), (50, 50)))
    enemyX.append(random.randint(0, 750))
    enemyY.append(random.randint(0, 500))
    enemyX_change.append(0.5)
    enemyY_change.append(1)
    side.append("right")

# Score
score = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

# Music and sound effects
mixer.music.load("./background.wav")
mixer.music.play(-1)
mixer.music.set_volume(0.05)

def show_score(x, y):
    score_text = font.render("Score: " + str(score), True, (255,255,255))
    GAME_SCREEN.blit(score_text, (x,y))

# show Player and Enemy PNG on screen
def show_player(x, y):
    GAME_SCREEN.blit(PLAYER, (x, y))

def show_enemy(x, y, enemy):
    GAME_SCREEN.blit(enemy, (x, y))

# fire bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    GAME_SCREEN.blit(BULLET, (x, y))

# collision functions
def is_collision(enemyX, enemyY, bulletX, bulletY, bullet_state):
    distance = math.sqrt((enemyX - bulletX)**2 + (enemyY - bulletY)**2)
    # the bullet PNG is 24x24 so we have to use 24 to compare the distance
    if distance < 24:
        print(f"enemyX={enemyX} enemyY={enemyY} bulletX={bulletX} bulletY={bulletY}") 
        return True
    return False

def ship_collision(enemyX, enemyY, shipX, shipY):
    distance = math.sqrt((enemyX - shipX)**2 + (enemyY - shipY)**2)
    if distance < 50:
        return True
    return False

# Game Over
game_over_font = pygame.font.Font("freesansbold.ttf", 40)
game_overX = 280
game_overY = 280
def game_over_text(x, y):
    over_text = game_over_font.render("GAME OVER!!", True, (255,255,255))
    GAME_SCREEN.blit(over_text, (x,y))

# game loop
game_active = True 
# side = "right"
while game_active:
    GAME_SCREEN.blit(background_image, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_active = False

    # Player spaceship movement 
    # used as if and not if..elif to allow multiple directions at the same time
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        if playerX < 750:
            playerX += playerX_change
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        if playerX > 0:
            playerX -= playerX_change
    if pygame.key.get_pressed()[pygame.K_UP]:
        if playerY > 0:
                playerY -= playerY_change
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        if playerY < 550:
            playerY += playerY_change 
    
    # enemy movement
    for i in range(num_of_enemies):
        # Game over when enemy crashes with spaceship or gets to the bottom of screen
        if enemyY[i] > 500 or ship_collision(enemyX[i], enemyY[i], playerX, playerY):
            print("game over") 
            # remove the enemies
            for j in range(num_of_enemies):
                # all enemies goes below the screen for hiding
                enemyY[j] = 700
            # show game over and exit loop
            game_over_text(game_overX, game_overY)
            break
        # moving the enemies on screen from left to right and top to bottom
        if enemyX[i] < 750 and side[i] == "right":
            enemyX[i] += enemyX_change[i]
        if enemyX[i] >= 750 and side[i] == "right":
            enemyY[i] += enemyY_change[i]
            side[i] = "left"
        if enemyX[i] > 0 and side[i] == "left":
            enemyX[i] -= enemyX_change[i]
        if enemyX[i] <= 0 and side[i] == "left":
            enemyY[i] += enemyY_change[i]
            side[i] = "right"
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY, bullet_state)
        if collision and bullet_state == "fire":
            # resets the bullet
            bulletY = playerY - 24
            bullet_state = "ready"
            collision_sound = mixer.Sound("./explosion.wav")
            collision_sound.set_volume(0.05)
            collision_sound.play()
            score += 1
            # resets the enemy
            enemyX[i] = random.randint(0, 750)
            enemyY[i] = random.randint(0, 500)
        # show enemies
        show_enemy(enemyX[i], enemyY[i], ENEMY[i])
    # shoot when space is pressed
    if pygame.key.get_pressed()[pygame.K_SPACE] and bullet_state == "ready":
        # capture the playerX when space is pressed so the bullet does not move along with the spaceship
        bulletX = playerX + 13
        bullet_sound = mixer.Sound("./laser.wav")
        bullet_sound.set_volume(0.05)
        bullet_sound.play()
        fire_bullet(bulletX, bulletY)
    if bullet_state == "fire":
        bulletY -= bulletY_change
        fire_bullet(bulletX, bulletY)
    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = playerY - 24

    # show player
    show_score(textX, textY)
    show_player(playerX, playerY)
    pygame.display.update()