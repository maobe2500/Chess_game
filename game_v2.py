#!/usr/bin/env python3
from fnmatch import translate
from matplotlib.pyplot import draw
import pygame
import os
from GUI.menu import Menu
from board import Board
from piece import Piece

class Game:
    def __init__(self):
        pygame.init()
        # Size values
        self.width = 1000
        self.height = 1000
        self.info_panel_width = 200
        self.num_squares = 8
        self.rect_size = self.height/self.num_squares

        # Pygame objects
        self.screen = pygame.display.set_mode((self.width + self.info_panel_width, self.height))
        self.running = True
        self.clock = pygame.time.Clock()
        self.fps = 20
        self.menu_area = 200

        # Colors
        self.black = (50, 50, 50)
        self.white = (230, 230, 230)

        # Game objects and methods
        self.board = Board(self.rect_size)
        #self.menu = Menu(self.screen, self.width, self.height, self.menu_area)
        self.held_piece = None
        self.old_square = None
        self.turn = 1
        self.taken_pieces = {'b': [], 'w': []}
        self.moves = []
        self.current_move = ''
        #print(f'\n\nself.board.positions: {self.board.positions}\n')
        # 2eprint(f'\nself.board.positions: {self.board.positions}\n\n')



    def event_check(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pos()[0] < self.width: 
                self.hold_piece(event)
            if event.type == pygame.MOUSEBUTTONUP:
                #Drop the piece if empty square is pressed while holding
                if pygame.mouse.get_pos()[0] < self.width:
                    self.drop_piece(event)
                
    
    # A helper function that finds the clicked piece and saves it and its
    # old position in two flags named "held_piece" and "old_piece"
    def hold_piece(self, event):
        x, y = self.convert_event_pos(event)
        # Check every piece
        for piece in self.board.positions.values():
            # If a piece is pressed and we arent holding anything
            if piece.is_pressed(event.pos) and not self.held_piece:
                # Save the clicked piece and its old position
                if piece.color == self.board.active_color:
                    self.held_piece = self.board.positions[(x, y)]
                    self.old_square = (x, y)
                break



    # A helper function that converts event position to center square position
    def convert_event_pos(self, event):
        x, y = event.pos
        x = x // self.rect_size * self.rect_size + self.rect_size/2
        y = y // self.rect_size * self.rect_size + self.rect_size/2
        return (x, y)
    

    # A helper function that drops the piece and resets flags and checks legality of move
    # Set position to center of current square if different legal square
    # Delete the old place from the dict and reset flags
    def drop_piece(self, event):
        x, y = self.convert_event_pos(event)
        if self.held_piece is not None:
            is_legal_move = True # Change when the time comes
            #is_legal_move = self.board.legal_move(self.held_piece, self.old_square, (x, y))
            current_square = (x, y)
            # if moved to different square, check if its legal and make the move,
            # otherwise just drop back to starting square 
            if is_legal_move: 
                occupied = current_square in self.board.positions

                if occupied:
                    self.take(current_square)
                else:
                    self.move(current_square)
                print(self.moves)
            else:
                self.move(self.old_square)
            #print(self.taken_pieces)
    

    # Moves a piece to a given locaiton and adds to turn, if location is the same as old location it doesnt add a turn
    def move(self, location):
        self.held_piece.pos = location
        if self.old_square != location:
            self.board.positions[location] = self.held_piece
            del self.board.positions[self.old_square]
            self.turn += 1
            print(self.turn)
        self.old_square = None
        self.held_piece = None
        self.board.active_color = 'b' if self.turn % 2 == 0 else 'w'


    # Takes a piece at a given location
    def take(self, location):
        if self.board.active_color == self.board.positions[location].color:
            self.move(self.old_square)
        else:
            self.taken_pieces[self.board.active_color].append(self.board.positions[location]) 
            del self.board.positions[location]
            self.move(location)



    def draw_text(self, text, text_size, centerx, centery):
        font = pygame.font.SysFont(pygame.font.get_default_font(), int(text_size))
        t_surface = font.render(text, True, self.white)
        t_rect = t_surface.get_rect()
        t_rect.center = (centerx, centery)
        self.screen.blit(t_surface, t_rect)



    def draw_info_panel(self):
        current_player_text = f'{self.board.active_color.title()} player\'s move' 
        moves_text = '\n'
        
        i = 2
        for move in self.moves:
            self.draw_text(move, 32, self.width + self.info_panel_width/2, i*self.height/30)
            i += 1
        
        self.draw_text(current_player_text, 28, self.width + self.info_panel_width/2, self.height/30)



    def draw(self):
        self.draw_info_panel()
        for j in range(0, self.num_squares):
            for i in range(0, self.num_squares):
                # Quick fix since posistion of sprites is drawn from center but the squares are not FIX LATER!!!
                pos = (i*self.rect_size + self.rect_size/2, j*self.rect_size + self.rect_size/2)
                j_is_even = j % 2 == 0
                i_is_even = i % 2 == 0
                rect = pygame.Rect(pos[0] - self.rect_size/2, pos[1] - self.rect_size/2, self.rect_size, self.rect_size)

                # Calculate color of square
                color = self.black if j_is_even and not i_is_even or not j_is_even and i_is_even else self.white

                pygame.draw.rect(self.screen, color, rect)
                # Draw the square and the pieces
                if pos in self.board.positions:
                    piece = self.board.positions[pos]
                    piece.draw(self.screen)

                # Draw the held piece at mouse position
                if self.held_piece is not None:
                    mx, my = pygame.mouse.get_pos()
                    self.held_piece.pos = (mx, my)
                    self.held_piece.draw(self.screen)


    def main_loop(self):
        while self.running:
            self.clock.tick(self.fps)
            self.event_check()
            #self.menu.draw()
            self.screen.fill(self.black)
            self.draw()
            pygame.display.flip()


g = Game()
g.main_loop()
