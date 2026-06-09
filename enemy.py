import pygame
from player import Player


class Enemy(pygame.sprite.Sprite):

    health: float
    speed: float
    damage: float
    # dying_sound: pygame.mixer.Sound
    x: int
    y: int
    last_attack: int
    attack_cooldown: int

    def __init__(self, dying_sound, image, GAME_DIFFICULTY):

        super().__init__()

        self.health = 3 * (1.003 **  GAME_DIFFICULTY)
        self.speed = 1.9 * (1.003 **  GAME_DIFFICULTY)
        self.damage = 1.69 * (1.003 **  GAME_DIFFICULTY)
        self.last_attack = 0
        self.attack_cooldown = 1500
        # self.dying_sound = pygame.mixer.Sound(dying_sound)

        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()

        # pygame.draw.rect(self.image, "red", ((0,0),(25, 25)))

    def update(self, player: Player):

        # Differenz der Position von Player und der Gegner Entity bestimmt die Richtung
        x_direction = player.rect.centerx - self.rect.x
        y_direction = player.rect.centery - self.rect.y


        # normalisierter richtungs vektor welcher in richtung player zeigt
        # normalisierter vektor hat immer die länge 1

        directional_vector = pygame.math.Vector2(x_direction, y_direction)

        if directional_vector.length() == 0:
            self.deal_damage(player)
        else:
            directional_vector.normalize_ip()

            directional_vector *= self.speed

            self.rect.x += directional_vector.x
            self.rect.y += directional_vector.y


    def take_damage(self, amount):
        if amount > self.health:
            self.health = 0
            self.kill()
            return True
        else:
            self.health -= amount
            return False

    
    def deal_damage(self, player: Player):
        if(pygame.time.get_ticks() - self.last_attack) > self.attack_cooldown:
            player.take_damage(self.damage)
            self.last_attack = pygame.time.get_ticks()
