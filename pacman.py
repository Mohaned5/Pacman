import pygame
from pygame.locals import *
import os
from collections import deque


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


class Pacman(pygame.sprite.Sprite):
    
    def __init__(self, start_pos):
        super().__init__() 
        #loads pacman facing right image - initial direction
        self.image = pygame.image.load(os.path.join(asset_path, sprites_path, 'pacman_roo.png'))
        self.rect = self.image.get_rect()
        self.start_pos = start_pos
        self.direction = 1
        #maps the direction which pacman moves depending on the integer 'direction' stores
        #moves according to the speed defined globally
        self.move_map = {
            0 : (0, -PACMAN_SPEED),
            1 : (PACMAN_SPEED, 0),
            2 : (0, PACMAN_SPEED),
            3 : (-PACMAN_SPEED, 0),
        }
        
        #maps the pac-man sprite which is displayed depending on direction
        #cycle of mouth opening and closing
        #sprite: pacman_(direction)(mouth wideness), i.e uoo = up open open
        self.sprite_map = {
            0 : ('pacman_uoo.png', 'pacman_uo.png', 'pacman_uc.png', 'pacman_uo.png'),
            1 : ('pacman_roo.png', 'pacman_ro.png', 'pacman_rc.png', 'pacman_ro.png'),
            2 : ('pacman_doo.png', 'pacman_do.png', 'pacman_dc.png', 'pacman_do.png'),
            3 : ('pacman_loo.png', 'pacman_lo.png', 'pacman_lc.png', 'pacman_lo.png'),
        }
        
        self.count = 0
        #creates double ended queue which stores change in direction - next direction which player requests
        self.next_dir = deque()
        self.max_queue_len = 1
        
        
        self.reset()
        
    '''Resets pacman - puts him back in spawn position and sets initial direction'''
    def reset(self):
        #left edge of sprite aligns with x coordinate of start position
        self.rect.left = self.start_pos[0]
        #top edge of sprite aligns with y coordinate of start position
        self.rect.top = self.start_pos[1]
        #sets initial direction to 1 = right
        self.direction = 1
        self.next_dir.clear()


    '''Finds and returns the values from world array stored in the coordinate ahead of pacman and behind pacman
    Takes in (x,y) of block Pacman is moving into.
    Returns the blocks array - block ahead and block containing pacman'''
    def check_ahead(self, new_x, new_y, world):
        #coordinate according to world matrix which pacman is moving into
        ix, iy = new_x//BLOCK_SIZE, new_y//BLOCK_SIZE 
        #how far into block pacman is
        rx, ry = new_x % BLOCK_SIZE, new_y % BLOCK_SIZE 
        blocks = [world[iy][ix]]
        #if moving along x axis, gets the block to the right
        if rx: blocks.append(world[iy][ix+1]) 
        #if moving along y axis, gets block below
        if ry: blocks.append(world[iy+1][ix])        
        return blocks
    
    
    '''Controls what happens if arrow key is pressed
    Loads next direction pacman will change to into a queue    
    Takes in key pressed by user'''
    def on_key_down(self, key): 
        self.next_dir.clear()
        if key == pygame.K_UP:
            self.next_dir.append(0)
        elif key == pygame.K_LEFT:
            self.next_dir.append(3)
        elif key == pygame.K_DOWN:
            self.next_dir.append(2)
        elif key == pygame.K_RIGHT:
            self.next_dir.append(1) 

    '''Updates Pacmans direction depending on blocks around.
    Prevents pacman from changing direction into wall/solid block.
    Controls animation cycle of Pacmans mouth widening and closing
    
    Takes in world matrix'''        
    def update(self, world): 
        if self.next_dir: 
            #if the new direction is in the same direction or opposite current direction, direction change can happen immediately
            #pacman doesnt need to be in center of block in order to reverse direction
            #recieves the blocks ahead depending on next direction
            if (self.direction % 2 != 0 and self.next_dir[0] % 2 != 0) or (self.direction % 2 == 0 and self.next_dir[0] % 2 == 0):
                self.direction = self.next_dir.popleft()
            else: 
                #if pacman is changing axis, from moving in x plane to y plane, needs to be in middle of block before move can be carried out
                #ensures pacman moves in the grid - otherwise would move into wall if not perfectly aligned with centre of block
                if self.check_center(): 
                    block_ahead = self.check_ahead(self.rect.x + self.move_map[self.next_dir[0]][0], self.rect.y + self.move_map[self.next_dir[0]][1], world)
                    #if the block ahead doesn't contain wall or gate in the level array, new direction can be dequeued and set
                    if '1' not in block_ahead and '3' not in block_ahead and '5' not in block_ahead:
                        self.direction = self.next_dir.popleft()
        #implements sprite map - causes pac-man mouth opening and closing animation
        #changes sprite after every 4 counts/frames
        if self.count % 5 == 0:
            self.image = pygame.image.load(os.path.join(asset_path, sprites_path, self.sprite_map[self.direction][self.count//5]))

        #gets value stored at the current block and next block from coordinate in matrix
        block_ahead = self.check_ahead(self.rect.x + self.move_map[self.direction][0], self.rect.y + self.move_map[self.direction][1], world)

        #if next block does not contain wall or gate, pacman can move into the block
        if '1' not in block_ahead and '3' not in block_ahead and '5' not in block_ahead:
            self.rect.x += self.move_map[self.direction][0]
            self.rect.y += self.move_map[self.direction][1]

        self.count += 1 
        if self.count == 20: 
            self.count = 0 
        
    '''Checks if pacman is in centre of the block containing Pacman'''
    def check_center(self):  
        #checks if the pacman sprite is in the center of its block
        return self.rect.x % 25 == 0 and self.rect.y % 25 == 0

