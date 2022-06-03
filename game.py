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
        self.num_squares = 8
        self.rect_size = self.height/self.num_squares

        # Pygame objects
        self.screen = pygame.display.set_mode((self.width, self.height))
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
        self.pieces = {}
        self.held_piece = None
        self.old_place = None
        self.turn = 1
        self.taken_pieces = {'black': [], 'white': []}
        self.get_pngs()
        print(f'\n\nself.pieces: {self.pieces}\n')
        print(f'\nself.board.positions: {self.board.positions}\n\n')

    def event_check(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN: 
                self.hold_piece(event)
            if event.type == pygame.MOUSEBUTTONUP:
                #Drop the piece if empty square is pressed while holding
                self.drop_piece(event)
    
    # A helper function that finds the clicked piece and saves it and its
    # old position in two flags named "held_piece" and "old_piece"
    def hold_piece(self, event):
        x, y = self.convert_event_pos(event)
        # Check every piece
        for piece in self.pieces.values():
            # If a piece is pressed and we arent holding anything
            if piece.is_pressed(event.pos) and not self.held_piece:
                # Save the clicked piece and its old position
                self.held_piece = self.pieces[(x, y)]
                self.old_place = (x, y)
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
            print('Dropping')
            
            is_legal_move = True # Change when the time comes
            #is_legal_move = self.board.legal_move(self.held_piece, self.old_place, (x, y))
            if self.old_place != (x, y) and is_legal_move: 
                print('Different' + f'{(x, y)}      {self.old_place}')
                self.held_piece.pos = (x, y)
                self.pieces[(x, y)] = self.held_piece
                
                del self.pieces[self.old_place]
                self.old_place = None
                self.held_piece = None
            else:
                print('Same')
                self.held_piece.pos = (x, y)
                self.old_place = None
                self.held_piece = None

    def draw(self):
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
                if pos in self.pieces:
                    piece = self.pieces[pos]
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
    
    # Goes through the pngs, makes a Piece object and adds it to the self.pieces dict
    def get_pngs(self):
        directory = './GUI/pngs'
        for filename in os.listdir(directory):
            name = filename[:-4]
 #           print(name)
            pos_list = self.board.get_starting_pos(name)
            for pos in pos_list:
                piece = Piece(pos, directory + '/' + filename)
                self.pieces[pos] = piece

g = Game()
g.main_loop()
