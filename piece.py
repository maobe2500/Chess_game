import pygame
import pylab

class Piece(pygame.sprite.Sprite):
    def __init__(self, pos, color, fen_name, path):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.color = color
        self.fen_name = fen_name
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(center=pos)

    def draw(self, screen):
        self.rect.centerx, self.rect.centery = self.pos
        screen.blit(self.image, self.rect)
    
    def is_pressed(self, event_pos):
        return self.rect.collidepoint(event_pos)
