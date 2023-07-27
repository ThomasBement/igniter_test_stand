# ---------------------------------------- #
# game_gui [Python File]
# Written By: Thomas Bement
# Created On: 2023-06-22
# ---------------------------------------- #

"""
IMPORTS
"""
from cgitb import reset
import pygame

"""
CONSTANTS
"""
logo_path           = './IMG/rocket_logo_32.png'
background_path     = './IMG/PnID_GUI.png'
background_color    = '#FFFFFF'

fps                 = 60
resolution          = (1389, 781)

relay_states = [False,  False,  False,  False,  False,  False,  False,  False] # Relay states 0 - nominal, 1 - inverted

"""
CLASSES
"""
class button:
    def __init__(self, name, position, size, color, relay_pointers, btn_type = 'valve', text = None):
        # Determine types for variables inside the button class
        type_list = [[name,             str,    'name'],
                    [position,         tuple,  'position'],
                    [size,             tuple,  'size'], 
                    [color,            str,    'color'], 
                    [relay_pointers,   list,   'relay_pointers'],
                    [btn_type,          str,   'btn_type']]
        # Perform type check and assign nan/inf for all variables that don't comply 
        for i in range(len(type_list)):
            variable            =   type_list[i][0]
            variable_type       =   type_list[i][1]
            variable_name       =   type_list[i][2]
            if type(variable) != variable_type:
                print('Type error, button %s expected to recive a %s for variable %s, but got %s instead' %(self, variable_type, variable_name, type(variable)))
                type_list[i][0] = float('NAN')
        # Assign basic init variables to button object
        self.name               = type_list[0][0]
        self.x_pos              = type_list[1][0][0]
        self.y_pos              = type_list[1][0][1]
        self.width              = type_list[2][0][0]
        self.height             = type_list[2][0][1]
        self.color              = type_list[3][0]
        # Assign button type specific variables to button boject
        if (btn_type == 'valve'):
            self.active         = True
            self.relay_pointers = type_list[4][0]
        elif (btn_type == 'driven valve'):
            self.active         = False
            self.relay_pointers = type_list[4][0]
        elif (btn_type == 'state'):
            self.active         = True
            self.relay_pointers = type_list[4][0]
        elif (btn_type == 'display box'):
            self.active         = False
            self.relay_pointers = None
        else:
            print('Button type error, expected a btn_type of (valve, driven valve,state or display box) got %s instead' %(btn_type))
            self.active         = None
            self.relay_pointers = None
        # Pygame specific attributes
        self.font           = pygame.font.SysFont('Arial', 14)
        self.button_surface = pygame.Surface((self.width, self.height))
        self.button_rect    = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
    
    def process(self, screen):
        mouse_position = pygame.mouse.get_pos()
        self.button_surface.fill(self.color)
        if self.active:
            if self.button_rect.collidepoint(mouse_position):
                lighter_color = color_shift(self.color, 1.2)
                self.button_surface.fill(lighter_color)
                if pygame.mouse.get_pressed(num_buttons=3)[0]:
                    darker_color = color_shift(self.color, 0.8)
                    self.button_surface.fill(darker_color)
                    # Invert states when clicked
                    for i in self.relay_pointers:
                        relay_states[i] = not(relay_states[i])
                    #self.onclickFunction() <- add serial stuff here
                else:   
                    self.alreadyPressed = False
        # Determine button state
        total = 0
        for i in self.relay_pointers:
            total += relay_states[i]
        if (total == 0):
            display_text = 'X'
            print(total, 'first', relay_states)
        elif (total == len(self.relay_pointers)):
            display_text = 'O'
            print(total, 'secc', relay_states)
        else:
            display_text = 'ERR'
        # Combine all surfaces into one
        self.text_surface   = self.font.render(display_text, True, (20, 20, 20))
        self.button_surface.blit(self.text_surface, [self.button_rect.width/2     -  self.text_surface.get_rect().width/2, 
                                                     self.button_rect.height/2    -  self.text_surface.get_rect().height/2])
        screen.blit(self.button_surface, self.button_rect)

"""
FUNCTIONS
"""
def button_text(b):
    text = b.text

def color_shift(hex_color, brightness_scale = 1):
    if len(hex_color) != 7:
        raise Exception("Passed %s into color_variant(), needs to be in #87c95f format." % hex_color)
    hex = hex_color.lstrip('#')
    rgb = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
    new_rgb = []
    for rgb_value in rgb:
        if int(brightness_scale*rgb_value) <= 255:
            new_rgb.append(int(brightness_scale*rgb_value))
        else:
            new_rgb.append(255)
    new_rgb = tuple(new_rgb)
    return '#%02x%02x%02x' % new_rgb

"""
MAIN
"""
def main():     
    # Initialization and setup
    pygame.init()
    pygame.display.set_icon(pygame.image.load(logo_path))
    pygame.display.set_caption('Test Stand GUI')
     
    # Window screen
    flags = pygame.RESIZABLE|pygame.SCALED#|pygame.FULLSCREEN 
    screen = pygame.display.set_mode(resolution, flags, vsync=1)
    screen.fill(background_color)
    pygame.display.update()

    # Create objects to be loaded by default 
    background  = pygame.image.load(background_path)

    valve_size  = (40, 40)
    # Define buttons,   (name,          position,       size,           color,          relay_pointers, btn_type,       text)
    PR_SV_001   = button('PR_SV_001',   (481, 100),     valve_size,     '#FFC336',      [0],            'valve') 
    PR_SV_002   = button('PR_SV_002',   (484, 0),       valve_size,     '#FFC336',      [1],            'valve') 
    PR_SV_003   = button('PR_SV_003',   (610, 361),     valve_size,     '#FFC336',      [2],            'valve') 
    PR_SV_004   = button('PR_SV_004',   (610, 247),     valve_size,     '#FFC336',      [3],            'valve') 
    PG_SV_001   = button('PG_SV_001',   (406, 382),     valve_size,     '#FFC336',      [4],            'valve') 
    K_PV_001    = button('K_PV_001',    (1026, 101),    valve_size,     '#FF2424',      [3],            'driven valve')
    O2_PV_001   = button('O2_PV_001',   (350, 621),     valve_size,     '#2C9E10',      [2],            'driven valve') 

    buttons     = [PR_SV_001, PR_SV_002, PR_SV_003, PR_SV_004, PG_SV_001, K_PV_001, O2_PV_001]
    
    # Loop variables
    clock = pygame.time.Clock()
    running = True
     
    # Main loop
    while running:
        """
        GRAPHICS
        """
        screen.fill(background_color)                   # Fill screen background with default color
        screen.blit(background, (0, 0))                 # Draw background image onto screen surface
        for b in buttons:
            b.process(screen)
        pygame.display.update()                         # Apply updates on screen surface
        """
        EVENTS
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        """
        TIMING
        """
        clock.tick(fps)
     
# Only run main when program is run locally     
if __name__=="__main__":
    main()