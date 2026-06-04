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
player = Player("freesound_community-laser-45816.mp3")
player.rect.centerx = screen.get_width() / 2
player.rect.centery = screen.get_height() / 2

last_enemy_spawn = 0


HEALTH_HUD = pygame.font.SysFont(None, 20, False, False)
COIN_HUD = pygame.font.SysFont(None, 20, False, False)
ARMOUR_HUD = pygame.font.SysFont(None, 20, False, False)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    if(pygame.time.get_ticks() - last_enemy_spawn) > SPAWNING_COOLDOWN:

        SPAWN_POINT_LIST = [
            (random.randint(0, WIDTH), 0),
            (random.randint(0, WIDTH), HEIGHT),
            (0, random.randint(0, HEIGHT)),
            (WIDTH, random.randint(0, HEIGHT))
        ]

        spawn_point = random.choice(SPAWN_POINT_LIST)

        enemy = Enemy("bubble pop.mp3")
        enemy.rect.x = spawn_point[0]
        enemy.rect.y = spawn_point[1]
        enemy_group.add(enemy)
        last_enemy_spawn = pygame.time.get_ticks()


    screen.blit(HEALTH_HUD.render(str(player.health), antialias=True, color="white"), (0, 0))

    screen.blit(player.image, player.rect)
    player.shoot(enemy_group, bullet_group)

    enemy_group.draw(screen)
    enemy_group.update(player)

    bullet_group.draw(screen)
    bullet_group.update()

    clock.tick(60)

    pygame.display.flip()


pygame.quit()