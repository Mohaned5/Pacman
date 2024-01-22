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


class main_menu:
    def __init__(self) -> None:
        self.WIDTH = WORLD_SIZE*BLOCK_SIZE
        self.HEIGHT = WORLD_SIZE*BLOCK_SIZE  
        #name initially is not taken
        self.taken_check = False   

    '''Takes in text, font, size and colour wanted and converts the text to this format'''
    def text_format(self, message, textFont, textSize, textColor):    
        #template for text
        self.newFont=pygame.font.Font(textFont, textSize)
        self.newText=self.newFont.render(message, 0, textColor)
        return self.newText
    
    '''Displays and controls main menu.
        Observes which option is being hovered over - changes its colour.
        Controls what happens when each option in menu is selected
        Takes in display'''
    def main_menu(self, display):
        menu=True
        #player initially hovers over start option
        self.selected="start"
        self.option=0
        
        while menu:
            for event in pygame.event.get():
                #quits if X button pressed
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type==pygame.KEYDOWN:
                    #plays sound when moving 
                    pygame.mixer.music.load(os.path.join(asset_path, sounds_path, 'button_press.mp3'))
                    pygame.mixer.music.play(0)
                    #if up key pressed, the option above is hovered over
                            #if player is already hovering over top option, will remain hovering over that option
                    if event.key == pygame.K_UP:
                        if self.option > 0:
                            self.option -= 1
                    #if down key is pressed, the option below is hovered over
                            #if player is already hovering over bottom option, will remain hovering over that option
                    elif event.key == pygame.K_DOWN:
                        if self.option < 2:
                            self.option += 1
                            
                #maps each option number to its corresponding selection
                if self.option == 0:
                    self.selected="start"
                elif self.option == 1:
                    self.selected="leaderboard"
                elif self.option == 2:
                    self.selected="quit"

                if event.type==pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.selected=="start":
                            menu = False

                        #if quit is selected, quits from game
                        elif self.selected=="quit":
                            pygame.quit()
                            quit()

                        #if player selects leaderboard, leaderboard screen is displayed
                        elif self.selected=="leaderboard":
                            self.leaderboard_screen = True
                            self.leaderboard(display)
                            
        
            #main menu UI
            self.DISPLAYSURF = display
            #loads main menu background
            self.mainbg = pygame.image.load(os.path.join(asset_path, sprites_path, 'mainbg.png'))
            #displays the background image on screen
            self.DISPLAYSURF.blit(self.mainbg, (0,0))
            self.title=self.text_format("Pac-Man", font, 60, yellow)
            #if hovering over option, colour changes to yellow
            if self.selected=="start":
                self.text_start=self.text_format("START", font, 45, yellow)
            #otherwise remains white
            else:
                self.text_start = self.text_format("START", font, 40, white)
            if self.selected=="quit":
                self.text_quit = self.text_format("QUIT", font, 45, yellow)
            else:
                self.text_quit = self. text_format("QUIT", font, 40, white)
            if self.selected=="leaderboard":
                self.text_leaderboard = self.text_format("LEADERBOARD", font, 45, yellow)
            else:
                self.text_leaderboard = self. text_format("LEADERBOARD", font, 40, white)
    
            #gets box around each text
            self.title_rect = self.title.get_rect()
            self.start_rect = self.text_start.get_rect()
            self.quit_rect = self.text_quit.get_rect()
            self.leaderboard_rect = self.text_leaderboard.get_rect()
            #displays menu text
            #centres each option text
            self.DISPLAYSURF.blit(self.title, (self.WIDTH/2 - (self.title_rect[2]/2), 80))
            self.DISPLAYSURF.blit(self.text_start, (self.WIDTH/2 - (self.start_rect[2]/2), 240))
            self.DISPLAYSURF.blit(self.text_quit, (self.WIDTH/2 - (self.quit_rect[2]/2), 360))
            self.DISPLAYSURF.blit(self.text_leaderboard, (self.WIDTH/2 - (self.leaderboard_rect[2]/2), 300))
            pygame.display.update()
    
    '''Displays and controls the pause menu.
        Changes the colour of the option being hovered over by the user.
        Controls what happens when each of the options are selected
        
        Takes in display
        Returns 'END' or RESUME'''
    def pause_menu(self, display):
        #player initially hovering over resume button
        self.pause=True
        self.selected="resume"

        while self.pause:                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type==pygame.KEYDOWN:
                    #if up key pressed, the option above is hovered over
                    #if player is already hovering over top option, will remain hovering over that option
                    if event.key == pygame.K_UP:
                        if self.option > 0:
                            self.option -= 1
                    #if down key is pressed, the option below is hovered over
                    #if player is already hovering over bottom option, will remain hovering over that option
                    elif event.key == pygame.K_DOWN:
                        if self.option < 2:
                            self.option += 1

                #maps each option number to its corresponding selection
                if self.option == 0:
                    self.selected="resume"
                elif self.option == 1:
                    self.selected="main menu"
                elif self.option == 2:
                    self.selected="quit"

                if event.type==pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.pause = False
                    elif event.key == pygame.K_RETURN:
                        #if player selects resume, pause menu closes and game continues
                        if self.selected=="resume":
                            self.pause = False
                            return 'RESUME'
                        elif self.selected=="quit":
                            pygame.quit()
                            quit()
                        #if main menu is selected, function returns 'END'
                        elif self.selected=="main menu":
                            return 'END'
    
            #pause menu UI
            self.DISPLAYSURF = display
            #loads pause screen background
            self.bg = pygame.image.load(os.path.join(asset_path, sprites_path, 'pausebg.png'))
            display.blit(self.bg, (0,0))
            
            #if hovering over option, colour changes to yellow
            if self.selected=="resume":
                self.text_resume=self.text_format("RESUME", font2, 30, yellow)
            #otherwise remains white
            else:
                self.text_resume = self.text_format("RESUME", font2, 30, white)

            if self.selected=="quit":
                self.text_quit = self.text_format("QUIT", font2, 30, yellow)
            else:
                self.text_quit = self. text_format("QUIT", font2, 30, white)
    
            if self.selected=="main menu":
                self.text_main_menu = self.text_format("MAIN MENU", font2, 30, yellow)
            else:
                self.text_main_menu = self. text_format("MAIN MENU", font2, 30, white)
                
            #gets box around text
            self.resume_rect = self.text_resume.get_rect()
            self.quit_rect = self.text_quit.get_rect()
            self.main_menu_rect = self.text_main_menu.get_rect()     

            #centres each option text
            #displays text
            self.DISPLAYSURF.blit(self.text_resume, (self.WIDTH/2 - (self.resume_rect[2]/2), 210))
            self.DISPLAYSURF.blit(self.text_quit, (self.WIDTH/2 - (self.quit_rect[2]/2), 275))
            self.DISPLAYSURF.blit(self.text_main_menu, (self.WIDTH/2 - (self.main_menu_rect[2]/2), 242))
            pygame.display.update()
        
    '''Displays and controls the input name screen. 
        Displays the text inputted by the user. 
        Sets max character length. 
        Saves the string as players name once 'enter' key is pressed
        
        Takes in display'''
    def input_name(self, display):
        self.name_screen = True
        self.base_font = pygame.font.Font(None, 32)
        self.user_text = '' 
        self.input_rect = pygame.Rect(100, 200, 150, 32)
        self.color = pygame.Color(89, 86, 0)
        self.max_length = 20
        screen = pygame.display.set_mode([WORLD_SIZE*BLOCK_SIZE, WORLD_SIZE*BLOCK_SIZE])
            
        while self.name_screen == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    #if user backspaces, last character of inputted text is removed
                    if event.key == pygame.K_BACKSPACE:
                        self.user_text = self.user_text[:-1]
                    #if user presses enter key, name input screen closes and game starts
                    elif event.key == pygame.K_RETURN:
                        #the minimum character length is 4   
                        if len(self.user_text) > 3:
                            #checks if name enterred is taken
                            self.taken_check = self.check_name(self.user_text)
                            #if name is taken, end screen is not set to false
                            if self.taken_check == True:
                                pass
                            else:
                                self.name_screen = False

                    #if user presses space key, the key is not recognised so does not input
                    elif event.key == pygame.K_SPACE:
                        pass

                    #adds any key inputs to the user text
                    else:
                        self.user_text += event.unicode

                #if the input exceeds user text, no more characters can be inputted
                if len(self.user_text) > self.max_length:
                    self.user_text = self.user_text[0:self.max_length]
            
            self.DISPLAYSURF = display
            
            #displays input name background image
            self.bg = pygame.image.load(os.path.join(asset_path, sprites_path, 'input_name.png'))
            display.blit(self.bg, (0,0))
            #draws rectangle text box
            pygame.draw.rect(screen, self.color, self.input_rect)
  
            #makes sure name isnt taken
            if self.taken_check == True:
                under_limit_text = self.text_format("This name is taken.", font3, 15, red)
                self.DISPLAYSURF.blit(under_limit_text, (185, 430))
                
            #if text is less than 4 characters, message displayed to the user
            if len(self.user_text) < 4:
                under_limit_text = self.text_format("Your name must contain more than 4 characters.", font3, 15, red)
                self.DISPLAYSURF.blit(under_limit_text, (75, 400))
                
            #displays what the user is typing on the screen
            text_surface = self.base_font.render(self.user_text, True, white)
            screen.blit(text_surface, (self.input_rect.x+5, self.input_rect.y+5))
            #sets box size for input text
            self.input_rect.w = max(100, 330)
            pygame.display.flip()
            
        return self.user_text
    
    def check_name(self, user_text):
        #opens leaderboard text file as variable 'names'
        #splits text file on new line char and returns list
        #ignores index 0 record - empty line
        with open(os.path.join(player_files_path, f'leaderboard.txt'), 'r') as names:
            lines = names.read().splitlines()[1:]
        
        #converts each key to its lowercase format and returns the names as a list
        names_list = [name.lower() for name in self.parse_sort_scores(lines).keys()]

        #if the user text already exists in list, returns True
        if user_text.lower() in names_list:
            return True
        
    '''Displays the leaderboard screen.
        Allows user to return to main menu
        
        Takes in display'''  
    def leaderboard(self, display):
        self.leaderboard_screen = True
        self.leaderboard_bg = pygame.image.load(os.path.join(asset_path, sprites_path, 'leaderboard_bg.png'))
        #displays background
        display.blit(self.leaderboard_bg, (0,0))
        #opens leaderboard text file as variable 'leaderboard;'
        #splits text file on new line char and returns list
        #ignores index 0 record - empty line
        with open(os.path.join(player_files_path, f'leaderboard.txt'), 'r') as leaderboard:
            lines = leaderboard.read().splitlines()[1:]
        #stores sorted scores returned by parse_sort_scores
        sorted_scores = self.parse_sort_scores(lines)
        #y coordinate of top score
        self.text_y = 200
        #displays top score
        self.top_score = list(sorted_scores.items())[0]
        self.top_score_text = self.text_format(f'{self.top_score[0]} - {self.top_score[1]}', font3, 30, green)
        self.top_score_text_rect = self.top_score_text.get_rect()
        self.DISPLAYSURF.blit(self.top_score_text, ((self.WIDTH/2) - (self.top_score_text_rect.width)/2, 150))

        for entry in list(sorted_scores.items())[1:10]:
            #sets difference in y coordinate between each score
            self.text_y += 20
            score_line = self.text_format(f'{entry[0]}    {entry[1]}', font3, 20, yellow)
            score_line_rect = score_line.get_rect()
            self.DISPLAYSURF.blit(score_line, ((self.WIDTH/2) + 90 - (score_line_rect.width), self.text_y))            
        
        while self.leaderboard_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.leaderboard_screen = False
                        #if backspace button pressed, returns to main menu
            pygame.display.update()
        pygame.display.update()

    '''Parses scores list of strings into player name, integer score dictionary
            e.g scores = ['name,80'] -> {'name':80}'''
    def parse_sort_scores(self, scores):
        score_dict = {}
        for score in scores:
            #splits string on comma and returns list of two entries: name and score
            parsed_inp = score.split(',')
            #append dict entry of name: score while converting str score to int
            score_dict.update({parsed_inp[0]:int(parsed_inp[1])})
        #returns sorted dictionary by dict value which is scores in descending order
        return {k: v for k, v in sorted(score_dict.items(), key=lambda item: item[1], reverse=True)}
                       