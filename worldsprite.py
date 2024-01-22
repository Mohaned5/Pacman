import pygame
from pygame.locals import *
import os


asset_path = r'assets' 
levels_path = r'levels'
sprites_path = r'sprites'
sounds_path = r'sounds'
fonts_path = r'fonts'
player_files_path = r'player_files'

#sets number of blocks across world
WORLD_SIZE = 21
#sets number of pixels across each block
BLOCK_SIZE = 25


pygame.init()
pygame.font.init()
pygame.mixer.init()


white=(255, 255, 255)
black=(0, 0, 0)
gray=(50, 50, 50)
red=(255, 0, 0)
green=(0, 255, 0)
blue=(0, 0, 255)
yellow=(255, 216, 0)
pink=(255, 0, 212)

font = os.path.join(asset_path, fonts_path, 'PAC-FONT.ttf')
font2 = os.path.join(asset_path, fonts_path, 'TS-BLOCK-BOLD.ttf')
font3 = os.path.join(asset_path, fonts_path, 'UPHEAVTT.ttf')

#number of pixels pacman moves per frame
PACMAN_SPEED = 1
#number of pixels ghosts move per frame
GHOST_SPEED = 1


class WorldSprite(pygame.sprite.Sprite):
    '''Takes in start position of sprite, path to image'''
    def __init__(self, start_pos, path):        
        super().__init__() 
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()
        self.rect.left = start_pos[0]
        self.rect.top = start_pos[1]