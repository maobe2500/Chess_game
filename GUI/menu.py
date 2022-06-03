import pygame
from GUI.button import Button

# This is just a wrapper class for organisation and made for easy buildout
#
# To do:
#   Automate the placing of the buttons
#   Automate the settings and add functions for drawing pregame selections menues
#
class Menu:
    def __init__(self, screen, width, height, menu_area):
        self.screen = screen
        self.res_width = width
        self.res_height = height
        self.menu_area = menu_area

        self.black, self.white = (0,0,0), (255,255,255)

        pygame.init()


    # Draws the buttons and the inputs, this is made for future building purposes and not
    def draw(self):
        self.draw_buttons()

    # Gathers all the buttons
    # In the future this will be done automatically
    def draw_buttons(self):
        pass