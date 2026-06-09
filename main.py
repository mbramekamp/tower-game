import pygame
import random
from enemy import Enemy
from player import Player


#---- CONSTANTS -----#

HEIGHT = 800
WIDTH = 800
SPAWNING_COOLDOWN = 500



#-------------------#

#---- SPAWN POSITIONS -----#

SPAWN_POINT_LIST = [
    (random.randint(0, WIDTH), 0),
    (random.randint(0, WIDTH), HEIGHT),
    (0, random.randint(0, HEIGHT)),
    (WIDTH, random.randint(0, HEIGHT))
    ]


#-------------------#


pygame.init()
pygame.mixer.pre_init(44100,-16,2, 1024)
pygame.mixer.init()

pygame.font.init()


screen = pygame.display.set_mode((HEIGHT, WIDTH))
clock = pygame.time.Clock()

running = True
dt = 0


enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
player = Player("gunshot sound.mp3", "Player.png")
player.rect.centerx = screen.get_width() / 2
player.rect.centery = screen.get_height() / 2

last_enemy_spawn = 0
last_difficulty_increase = 0
background = pygame.image.load("cobble.png")

HEALTH_HUD = pygame.font.SysFont(None, 30,False, False)
COIN_HUD = pygame.font.SysFont(None, 30, False, False)
ARMOUR_HUD = pygame.font.SysFont(None, 30, False, False)
DAMAGE_HUD = pygame.font.SysFont(None, 30, False, False)
TIMER = pygame.font.SysFont(None, 30, False, False)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # screen.fill("black")
    screen.blit(background, (0, 0))

    GAME_TIME = pygame.time.get_ticks() // 1000
    GAME_DIFFICULTY = pygame.time.get_ticks() // 30000


    if GAME_TIME - last_difficulty_increase >= 30:
        SPAWNING_COOLDOWN = max(SPAWNING_COOLDOWN - 10, 100)
        print(SPAWNING_COOLDOWN)
        last_difficulty_increase = pygame.time.get_ticks() // 1000

    if(pygame.time.get_ticks() - last_enemy_spawn) > SPAWNING_COOLDOWN:

        SPAWN_POINT_LIST = [
            (random.randint(0, WIDTH), 0),
            (random.randint(0, WIDTH), HEIGHT),
            (0, random.randint(0, HEIGHT)),
            (WIDTH, random.randint(0, HEIGHT))
        ]

        spawn_point = random.choice(SPAWN_POINT_LIST)

        enemy = Enemy("bubble pop.mp3", "enemy.png", GAME_DIFFICULTY)
        enemy.rect.x = spawn_point[0]
        enemy.rect.y = spawn_point[1]
        enemy_group.add(enemy)
        last_enemy_spawn = pygame.time.get_ticks()


    screen.blit(HEALTH_HUD.render("HEALTH:" + str(f"{player.health:.1f}"), antialias=True, color="white"), (0, 0))
    screen.blit(ARMOUR_HUD.render("ARMOUR:" + str(f"{player.armour:.1f}"), antialias=True, color="white"), (0, 40))
    screen.blit(COIN_HUD.render("COINS:" + str(player.coins), antialias=True, color="white"), (0, 80))
    screen.blit(DAMAGE_HUD.render("DAMAGE:" + str(f"{player.damage:.1f}"), antialias=True, color="white"), (0, 120))
    screen.blit(TIMER.render(str(GAME_TIME), antialias=True, color="white"),(750, 0))

    screen.blit(player.image, player.rect)
    running = player.update()
    player.shoot(enemy_group, bullet_group)

    enemy_group.draw(screen)
    enemy_group.update(player)

    bullet_group.draw(screen)
    bullet_group.update()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_h]:
        player.upgrade_health()
    if keys[pygame.K_a]:
        player.upgrade_armour()
    if keys[pygame.K_d]:
        player.upgrade_damage()

    clock.tick(120)

    pygame.display.flip()


pygame.quit()