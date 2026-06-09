import pygame
from bullet import Bullet


SHOT_COOLDOWN = 300


class Player(pygame.sprite.Sprite):

    coins: int 
    health: float 
    armour: float
    damage: float
    last_shot:  int
    radius: int
    shoot_sound: pygame.mixer.Sound
    shot_cooldown: int


    def __init__(self, sound_file, image):

        # Konstruktor Aufruf 
        super().__init__()

        self.coins = 0
        self.health = 10
        self.armour = 1
        self.last_shot = 0
        self.radius = 350
        self.damage = 3
        self.shoot_sound = pygame.mixer.Sound(sound_file)
        self.shot_cooldown = 300
        
        # Bestimmt die Oberfläche bzw. quasi die Hitbox des Sprites
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (100, 100))
        # Bestimmt wie es angezeigt wird.
        self.rect = self.image.get_rect()

        # pygame.draw.rect(self.image, "green", ((0, 0),(50, 50)), 0)
        
    def update(self):
        if self.health <= 0:
            self.kill()
            return False
        return True

    def upgrade_health(self):
        if self.coins > 20:
            self.health = self.health + (self.health * 0.035)
            self.coins -= 20
        else:
            print("[INFO]: INSUFFICIENT FUNDS")

    def upgrade_armour(self):

        # min nimmt im falle, das self.armour größer als 100 ist, immer die 100

        if self.coins > 25:
            self.armour = min(self.armour + (self.armour * 0.012), 100)
            self.coins -= 25
        else:
            print("[INFO]: INSUFFICIENT FUNDS")

    def upgrade_damage(self):
        if self.coins > 10:
            self.damage *= 1.15
            self.coins -= 10
        else:
            print("[INFO]: INSUFFICIENT FUNDS")

    def upgrade_attack_speed(self):
        if self.coins > 25:
            self.shot_cooldown -= 10
            self.coins -= 25
        else:
            print("[INFO]: INSUFFICIENT FUNDS")

    def take_damage(self, amount):
        damage_taken =  amount - (amount * (self.armour / 100))
        if damage_taken > self.health:
            self.health = 0
            return False
        print("Damage taken")
        self.health -= damage_taken
        return True

    def shoot(self, enemy_group, bullet_group):
        nearest_enemy = self.check_nearest_enemy(enemy_group)
        if nearest_enemy is not None:
            if(pygame.time.get_ticks() - self.last_shot) > self.shot_cooldown:
                bullet = Bullet(nearest_enemy, self, self.rect.centerx, self.rect.centery, self.damage)
                self.shoot_sound.play()
                bullet_group.add(bullet)
                self.last_shot = pygame.time.get_ticks()

    def check_nearest_enemy(self, enemy_group):
        nearest_enemy = None
        min_dist = float('inf')

        enemies_in_range = pygame.sprite.spritecollide(self, enemy_group, False, collided=pygame.sprite.collide_circle)
        if enemies_in_range:
            for enemy in enemies_in_range:
                x_direction = enemy.rect.x - self.rect.x
                y_direction = enemy.rect.y - self.rect.y

                directional_vector = pygame.math.Vector2(x_direction, y_direction)

                if directional_vector.length() < min_dist:
                    nearest_enemy = enemy
                    min_dist = directional_vector.length()

            return nearest_enemy
                