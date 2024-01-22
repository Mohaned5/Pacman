import pygame
from pygame.locals import *
import os
import random

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


class Ghost(pygame.sprite.Sprite):
    def __init__(self, start_pos, path):
        super().__init__() 
        self.image = pygame.image.load(path)
        #holds ghosts original sprite to allow ghost to return to former appearance after power up had expired
        self.backup_image = self.image 
        self.rect = self.image.get_rect()
        self.start_pos = start_pos
        self.direction = random.randint(0,3)
        #maps the value stored by 'direction' to corresponding movement
        #number of pixels ghost moves each frame controlled by GHOST_SPEED
        self.move_map = {
            0 : (0, -GHOST_SPEED),
            1 : (GHOST_SPEED, 0),
            2 : (0, GHOST_SPEED),
            3 : (-GHOST_SPEED, 0),
        }
        #when power up is active, ghost flashes between 2 sprites - stored in this variable
        self.ghost_flash = ('ghost_edible1.png', 'ghost_edible2.png')
        self.count = 0
        self.reset()
        
    '''Resets ghosts - puts them back in spawn position'''
    def reset(self):        
        self.rect.left = self.start_pos[0]
        self.rect.top = self.start_pos[1]
        
    '''Randomises direction when ghost reaches wall or junction.
        If pacman powered up, ghosts sprites flash.
        Stops ghost from moving upon reaching wall block'''
    def update(self, world, power_up_bool):
        if self.check_center():
            #when ghost is in centre of block, block_around empty array is created
            blocks_around = []
            for d in self.move_map.keys():
                #obtains value stored at coordinate of block ghost will move into from world array according to this direction
                next_block = world[self.rect.y // BLOCK_SIZE + self.move_map[d][1]][self.rect.x // BLOCK_SIZE + self.move_map[d][0]]
                #puts the next block into blocks_around array if there is no wall in that direction
                if next_block not in ['1', '3']:
                    blocks_around.append((next_block, d))
            #gets value stored at the current block and next block from coordinate in matrix
            block_ahead = self.check_ahead(self.rect.x + self.move_map[self.direction][0], self.rect.y + self.move_map[self.direction][1], world)
            #checks if there are 3 or 4 possible directions or more than 1 with wall in front
            if (len(blocks_around) > 2) or (len(blocks_around) > 1 and '1' in block_ahead) or (len(blocks_around) > 1 and '3' in block_ahead):
                valid_dir = [d[1] for d in blocks_around]
                self.direction = random.choice(valid_dir)
                block_ahead = self.check_ahead(self.rect.x + self.move_map[self.direction][0], self.rect.y + self.move_map[self.direction][1], world)
                #prevents pacman from moving back into spawn chamber
                if self.direction == 2:
                    while '5' in block_ahead:
                        self.direction = random.choice(valid_dir)
                        block_ahead = self.check_ahead(self.rect.x + self.move_map[self.direction][0], self.rect.y + self.move_map[self.direction][1], world)        
                    
                    
        #if pacman is powered up, the ghost change between flashed sprites every 4 frames
        if power_up_bool:
            if self.count % 5 == 0:
                self.image = pygame.image.load(os.path.join(asset_path, sprites_path, self.ghost_flash[self.count//10]))
        
        #gets coordinates of the next block ghost is moving into
        block_ahead = self.check_ahead(self.rect.x + self.move_map[self.direction][0], self.rect.y + self.move_map[self.direction][1], world)

        #if there is not a wall in the block ahead, move into the block
        if block_ahead not in ['1', '3']:
            self.rect.x += self.move_map[self.direction][0]
            self.rect.y += self.move_map[self.direction][1]

        self.count += 1
        if self.count == 20:
            self.count = 0
    
    '''After power up ends, resets ghosts back to original sprites'''
    def reset_sprite(self):        
        self.image = self.backup_image
        #resets the sprite of ghosts to their original sprites
    
    '''Checks if ghost is in the centre of the block containing ghost'''
    def check_center(self):        
        return self.rect.x % BLOCK_SIZE == 0 and self.rect.y % BLOCK_SIZE == 0
    
    '''Returns value of the block ahead and behind ghost according to world array
        
        Takes in (x,y) of next block Ghost moving into
        Returns the blocks array - block ahead and block containing ghost'''
    def check_ahead(self, new_x, new_y, world):
        #coordinate according to world matrix which ghost is moving into
        ix, iy = new_x//BLOCK_SIZE, new_y//BLOCK_SIZE
        #how far into the block ghost is
        rx, ry = new_x % BLOCK_SIZE, new_y % BLOCK_SIZE

        blocks = [ world[iy][ix] ]
        #if moving along x axis, gets the block to the right
        if rx: 
            blocks.append(world[iy][ix+1]) 
        #if moving along y axis, gets block below
        if ry: 
            blocks.append(world[iy+1][ix]) 
        
        return blocks
