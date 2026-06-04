import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from enemy import Enemy

class Bullet(pygame.sprite.Sprite):

    damage: float 
    speed: float
    x: int
    y: int
    

    def __init__(self, target, x, y):

        super().__init__()
        self.damage = 5
        self.speed = 13
        self.target = target
        
        self.image = pygame.Surface((5,5))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


        pygame.draw.rect(self.image, "white", ((0, 0),(5, 5)), 0)



# Also in update():

# Prüfen ob target noch alive ist — sonst self.kill()
# Richtungsvektor berechnen und normalisieren
# Bewegen

    def update(self):
        # Differenz der Position von Player und der Gegner Entity bestimmt die Richtung
        x_direction = self.target.rect.centerx - self.rect.x
        y_direction = self.target.rect.centery - self.rect.y

        # normalisierter richtungs vektor welcher in richtung player zeigt
        # normalisierter vektor hat immer die länge 1

        directional_vector = pygame.math.Vector2(x_direction, y_direction)

        if directional_vector.length() < self.speed:
            if self.target.alive():
                self.target.take_damage(self.damage)

            self.kill()
        elif not self.target.alive():
            self.kill()
        else:
            directional_vector.normalize_ip()

            directional_vector *= self.speed

            self.rect.x += directional_vector.x
            self.rect.y += directional_vector.y
            