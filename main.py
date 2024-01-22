import pygame, sys
from pygame.locals import *
import os
import time
from ghost import Ghost
from main_menu import main_menu
from pacman import Pacman
from worldsprite import WorldSprite


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

class Game:
    '''Constructor method - initialises objects attributes'''
    def __init__(self) -> None:
        self.WIDTH = WORLD_SIZE*BLOCK_SIZE
        self.HEIGHT = WORLD_SIZE*BLOCK_SIZE     
        self.TITLE = 'PacMan'
        self.SCORE = 0
        self.LIVES = 3
        self.NAME = None
        self.counter = None
        self.power_up = False
        self.level_number = 1
        self.new_load = False
        self.duration = 5        
        
        pygame.init()
        self.init_game(self.WIDTH, self.HEIGHT, self.TITLE)
        
        #assigns FPS a value
        self.FPS = pygame.time.Clock()
        self.FPS_limit = 150
        
        #maps each value from world array into sprite
        self.char_to_image = {
            '0' : 'dot2.png',
            '1' : 'wall.png',
            '2' : 'power2.png',
            '3' : 'wall2.png',
            '4' : 'black.png',
            '5' : 'gate.png',
            'r' : 'ghost_rr.png',
            'b' : 'ghost_bl.png',
            'p' : 'ghost_pr.png',
            'y' : 'ghost_yl.png',
        }
        
        self.pacman_obj = Pacman((self.WIDTH//2, self.HEIGHT - 4*BLOCK_SIZE))
        #creates layer for sprites
        self.all_sprites = pygame.sprite.LayeredUpdates()
        #creates layer for world
        self.world_layer = pygame.sprite.LayeredUpdates()
        #creates empty array to store sprites when loaded
        self.current_level_base = []
        self.ghosts = []
        self.menu = main_menu()        
        self.game_handler()
    
    '''Initialises the game
    Takes in width, height of window; title of game'''
    def init_game(self, width, height, title):
        self.new_game = True
        #creates display with width and height
        self.DISPLAYSURF = pygame.display.set_mode((width, height))
        #sets colour of background to black
        self.DISPLAYSURF.fill(pygame.Color(0,0,0))
        pygame.display.set_caption(title)
        self.font = pygame.font.SysFont(font3, 25)
        
    '''Controls what occurs when game finishes'''
    def game_handler(self):        
        while True:
            #value returned by run_game function stored as exit code
            exit_code = self.run_game(self.level_number)
            self.reset(exit_code)

    '''Initialises all attributes and objects  
    Takes in exit code'''
    def reset(self, exit_code):
        #sets all to default values when game is reset
        if exit_code == 'RESET':
            self.SCORE = 0
            self.LIVES = 3
            self.level_number = 1
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.world_layer = pygame.sprite.LayeredUpdates()
        self.current_level_base = []
        self.ghosts = []
        self.reset_game_state()
        
    '''Runs the game. Displays main menu, loads world and sprites.
        Stops game after the lives have reached 0, or moves on to the next level once number of pellets in world reach 0.
        Checks if the user requests to pause the game - displays the pause screen.
        Sets layers for objects and world.
        Activates power up when power pellet consumed.
        Displays name, score, power up lives on screen.
        Saves players name and score to leaderboard file
        
        Takes in level number
        
        Returns exit code'''
    def run_game(self, level_number):
        if self.new_game:
            self.menu.main_menu(self.DISPLAYSURF)
            self.NAME = self.menu.input_name(self.DISPLAYSURF)
            self.new_game = False

        #gets list of level array and stores it
        world = self.load_level(level_number)
        self.convert_world_to_sprite(world)
        self.pellet_count(world)

        #adds the base layer - world
        for base in self.current_level_base:
            self.world_layer.add(base, layer=1)

        #adds each ghost to all sprites group
            #sets layer
        for ghost in self.ghosts:
            self.all_sprites.add(ghost, layer=3)

        self.all_sprites.add(self.pacman_obj, layer=2)
        self.all_sprites.move_to_front(self.pacman_obj)
        
        #game will stop when lives reach 0 or number of pellets in world reaches 0
        while self.LIVES > 0 and self.pellet_counter > 0:
            for event in pygame.event.get(): 
                #if quit button selected, close window
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    #if space bar is pressed, game is paused and pause screen shown
                    #returned value stored
                    if event.key == pygame.K_SPACE:
                        pause_option = self.menu.pause_menu(self.DISPLAYSURF)
                        #if main menu option selected, lives set to 0 so game concludes
                        if pause_option == 'END':
                            self.LIVES = 0
                    #otherwise passes inputted key into said function
                    self.pacman_obj.on_key_down(event.key)
            
            #updates pacman object each frame
            self.pacman_obj.update(world)
            #updates each ghost each frame
            for ghost in self.ghosts: ghost.update(world, self.power_up) 

            #displays the world and sprites
            self.world_layer.draw(self.DISPLAYSURF)
            self.all_sprites.draw(self.DISPLAYSURF)

            #checks for pellet and replaces with black block if present
            #increases score by 10
            self.pellet_check(self.pacman_obj, world)
            #checks if pacman enters a block containing a power pellet
            #increases score by 50
            self.power_pellet_check(self.pacman_obj, world)
            
            #when pacman eats a power pellet, counter starts
            if self.power_up:
                self.counter+=1
                #when counter reaches end point, pacman power up disabled
                if self.counter == self.end_counter:
                    self.counter = None
                    self.power_up = False
                    #plays power down sound
                    pygame.mixer.music.load(os.path.join(asset_path, sounds_path, 'power_down.mp3'))
                    pygame.mixer.music.play(0)
                    #sets ghost sprite back to initial colours
                    for ghost in self.ghosts:
                        ghost.reset_sprite()
            
            #checks for contact between ghost and Pacman
            self.ghost_collision_check()        
            
            #displays score
            score_text = self.text_format("Score: "+str(self.SCORE), font3, 20, yellow)
            self.DISPLAYSURF.blit(score_text, (5, 3))
            
            #displays lives
            lives_text = self.text_format("Lives: "+str(self.LIVES), font3, 20, yellow)
            self.DISPLAYSURF.blit(lives_text, (430, 3))

            #displays level number
            level_text = self.text_format("Level: "+str(self.level_number), font3, 20, white)
            self.DISPLAYSURF.blit(level_text, (430, 502))

            #displays player name
            name_text = self.text_format("Name: "+(self.NAME), font3, 20, yellow)
            self.DISPLAYSURF.blit(name_text, (8, 502))
            
            #if pacman is powered up, text displays 'ACTIVE' in pink
            if self.power_up:
                self.power_up_active=self.text_format("ACTIVE", font3, 20, pink)
            #if pacman is not powered, text displays 'inactive' in white
            else:
                self.power_up_active = self.text_format("inactive", font3, 20, white)
            
            self.power_up_active_rect = self.power_up_active.get_rect()
            #centres text
            self.DISPLAYSURF.blit(self.power_up_active, (self.WIDTH/2 - (self.power_up_active_rect[2]/2), 3))
            
            pygame.display.update()
            if self.new_load:
                time.sleep(2)
                self.new_load = False
            self.FPS.tick(self.FPS_limit)
            
            self.pellet_count(world)
        
        #if game breaks out of loop because lives reach 0, score is saved
        #game over screen is displayed
        #new game is set
        if self.LIVES == 0:
            self.save_score()
            self.game_over(self.DISPLAYSURF)
            self.new_game = True
            return 'RESET'
        
        #if game breaks out of loop because all pellets have been eaten, player moves on to next level
        #once player reaches level 5, maps loop back to level 1
        elif self.pellet_counter == 0:
            self.level_number += 1
            if self.level_number == 5:
                self.level_number = 1
            return 'NEXT'

    
    '''Takes in text, font, size and colour wanted and converts the text to this format
        
        Takes in message, font, size, colour
        Returns converted text'''
    def text_format(self, message, textFont, textSize, textColor):
        self.newFont=pygame.font.Font(textFont, textSize)
        self.newText=self.newFont.render(message, 0, textColor)
        return self.newText
    
    '''Runs when lives reach 0. 
        Displays the game over screen, players name and score
        
        Takes in display'''
    def game_over(self, display):
        end_screen = True
        self.DISPLAYSURF = display
        #displays game-over screen
        self.game_over_bg = pygame.image.load(os.path.join(asset_path, sprites_path, 'game_over.png'))
        display.blit(self.game_over_bg, (0,0))
        
        #displays name of player
        #centres x coordinate
        self.name_print=self.text_format("Name:"+self.NAME, font2, 20, yellow)
        self.name_print_rect = self.name_print.get_rect()
        self.DISPLAYSURF.blit(self.name_print,(self.WIDTH/2 - self.name_print_rect.width/2, 230)) 

        #displays score which player achieved
        #centres x coordinate
        self.score_print=self.text_format("Score:"+str(self.SCORE), font2, 20, yellow)
        self.score_print_rect = self.score_print.get_rect()
        self.DISPLAYSURF.blit(self.score_print,(self.WIDTH/2 - self.score_print_rect.width/2, 260))        
        
        pygame.display.update()
        
        while end_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type==pygame.KEYDOWN:
                    #if player presses enter key, game over screen closes - game will start again
                    if event.key == pygame.K_RETURN:
                        end_screen = False
                    
        
    '''Checks if pacman has collided with a ghost. 
         If Pac-man powered up, score increases and ghosts respawn in spawn point. 
         If not powered up, lives decremented by 1 - pacman and ghosts put in their spawn positions.'''
    def ghost_collision_check(self):
        for ghost in self.ghosts:
            #returns true is centre of pacman object is in ghost rectangle
            if ghost.rect.collidepoint(self.pacman_obj.rect.center):
                #if pacman is powered up, ghost respawns and players score increases by 200
                if self.power_up:
                    ghost.reset()
                    self.SCORE += 200
                    #plays eating ghost sound
                    pygame.mixer.music.load(os.path.join(asset_path, sounds_path, 'pacman_eat_ghost.mp3'))
                    pygame.mixer.music.play(0)
                #if pacman is not powered up, player loses a life and game state is reset
                    #pacman reset to spawn position
                    #ghosts reset to spawn position
                else:
                    self.LIVES -= 1
                    self.reset_game_state()
                    #plays pacman dies sound
                    pygame.mixer.music.load(os.path.join(asset_path, sounds_path, 'pacman_dies.mp3'))
                    pygame.mixer.music.play(0)                    
                break
        
    '''Acts as a timer - uses number of frames which have passed rather than time.
        
        Takes in the requested duration in seconds.'''
    def power_up_time(self, duration):
        #counter initially set to 0
        #end counter is equal to duration multiplied by number of frames per second
        #duration in seconds
        #counter increases by FPS_limit each second
        self.counter = 0
        self.end_counter = duration*self.FPS_limit
        
    '''Resets pacman and ghosts to their initial spawn positions'''
    def reset_game_state(self):
        #indicates that game needs to be frozen briefly
        self.new_load = True
        #resets pacman to initial spawn position
        self.pacman_obj.reset()
        #resets ghosts to initial start positions
        for ghost in self.ghosts:
            ghost.reset()
        
        
    '''Checks if pacman is completely in block containing pellet.
        Pellet block is replaced by a black block.
        Increases score for each pellet eaten.
        Plays pacman eating pellet sound
        
        Takes in pacman object, world array'''
    def pellet_check(self, pacman, world):
        #only checks for pellet if pacman is in centre of block
        if not pacman.check_center():
            return
        
        #gets block coordinate of pacman
        ix, iy = pacman.rect.x//BLOCK_SIZE, pacman.rect.y//BLOCK_SIZE
        
        #if the block coordinate contains a pellet in world array, the pellet is replaced with black sprite
            #score increases by 10
        if world[iy][ix] == '0':
            world[iy][ix] = '4'
            self.SCORE += 10
            #plays pacman eating pellet sound
            pygame.mixer.music.load(os.path.join(asset_path, sounds_path, 'chomp.mp3'))
            pygame.mixer.music.play(0)
            
            #loads the black square sprite instead of pellet
            pellet_obj = self.world_layer.get_sprite(iy*len(world[0]) + ix)
            pellet_obj.image = pygame.image.load(os.path.join(asset_path, sprites_path, self.char_to_image['4']))
            
    '''Checks if pacman is completely in block containing power pellet.
        Power pellet replaced by a black block.
        Powers up pacman and starts timer. 
        Increases score. 
        Plays pacman eating power pellet sound
        
        Takes in pacman object, world array'''
    def power_pellet_check(self, pacman, world):    
        #only checks for power pellet if pacman is in centre of block
        if not pacman.check_center():
            return
        
        #gets block coordinate of pacman
        ix, iy = pacman.rect.x//BLOCK_SIZE, pacman.rect.y//BLOCK_SIZE
        
        #if the block coordinate contains a pellet in world array, the pellet is replaced with black sprite
        #score increases by 10
        if world[iy][ix] == '2':
            world[iy][ix] = '4'
            self.SCORE += 50
            self.power_up = True
            if self.level_number == 2:
                self.duration = 3
            elif self.level_number == 3:
                self.duration = 2
            elif self. level_number > 3:
                self.duration = 1
            #timer
            self.power_up_time(self.duration)
            #plays pacman eating pellet sound
            pygame.mixer.music.load(os.path.join(asset_path, sounds_path, 'power_chomp.mp3'))
            pygame.mixer.music.play(0)
            
            #loads the black square sprite instead of pellet
            power_pellet_obj = self.world_layer.get_sprite(iy*len(world[2]) + ix)
            power_pellet_obj.image = pygame.image.load(os.path.join(asset_path, sprites_path, self.char_to_image['4']))
            
    '''Converts 2D array of level into map.
        Scans through each item of each row of the array - 
        Passes each value into dictionary which converts it to corresponding sprite.
        Ghost block added to a ghost array - acts as an object and replaced by black block
        
        Takes in world array'''
    def convert_world_to_sprite(self, world):
        #clear old world incase reloading
        self.current_level_base.clear()
        
        for i, row in enumerate(world):
            for j, item in enumerate(row):
                if item in self.char_to_image:
                    #gets path to correct sprite
                    path_to_img = os.path.join(asset_path, sprites_path, self.char_to_image[item])
                    if item in ['r', 'b', 'p', 'y']:
                        #if item corresponds to ghosts, add ghost to array
                        self.ghosts.append(Ghost((BLOCK_SIZE*j, BLOCK_SIZE*i), path_to_img))
                        #replace ghost with black block
                        world[i][j] = '4'
                        #appends the world to change sprite to black block
                        self.current_level_base.append(WorldSprite((BLOCK_SIZE*j, BLOCK_SIZE*i), os.path.join(asset_path, sprites_path, self.char_to_image['4'])))
                        continue

                    #saves sprite in correct position
                    self.current_level_base.append(WorldSprite((BLOCK_SIZE*j, BLOCK_SIZE*i), path_to_img))
    
    '''Loads level text file depending on level the player is on. 
        Splits the level into rows and stores each row in 2D array.
        
        Takes in level number.
        Returns level as list'''
    def load_level(self, level_number):
        file_path = os.path.join(asset_path, levels_path, f'level_{level_number}.txt')
        #creates empty array to store level
        level_elements = []
        
        with open(file_path) as f:
            #imports each line of level into array
            for line in f:
                level_elements.append(list(line.strip('\n')))
        
        return level_elements
    
    '''Counts number of pellets in the world
    Takes in world'''
    def pellet_count(self, world):
        self.pellet_counter = 0
        #counts the number of pellets in the world
        for i, row in enumerate(world):
            self.pellet_counter += world[i].count('0') 
            
    '''Saves the players name and score to a leaderboard file'''
    def save_score(self):        
        with open (os.path.join(player_files_path, f'leaderboard.txt'),'a') as leaderboard:
            leaderboard.write(f'\n{self.NAME},{str(self.SCORE)}')
            leaderboard.close()
        

if __name__ == '__main__':
    game = Game()



