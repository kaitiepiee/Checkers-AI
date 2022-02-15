import pygame
from .constants import BLACK, WHITE, COLS, ROWS, RED, AQUAMARINE, WHITE, SQUARE_SIZE
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()

    def draw_blocks(self, win):
        win.fill(AQUAMARINE)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, WHITE,(row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[col][row], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS or row == 0:
            piece.make_King()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.black_kings += 1
                
    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3: # first 3 rows
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4: # last 3 rows
                        self.board[row].append(Piece(row, col, BLACK))
                    else:
                        self.board[row].append(0) # blank seperator
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_blocks(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

 

    def get_valid_moves(self, piece):
        moves = {} # directionary
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == BLACK or piece.king:
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row -1, min(row-3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row -1, min(row-3, ROWS), 1, piece.color, right))

        return moves


    # ALGO to determine base on spiece
    def _traverse_left(self, start, stop, step, color, left, skipped = []):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            current = self.board[r][left](r, left)
            if current == 0: # found empty square
                if skipped and not last:
                    break;
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last: 
                    if step == -1:
                        row = max(-3, 0)
                    else:
                        row = min( r+ 3, ROWS)

                    # double/tripple  jump
                    moves.update(self._traverse_left(r+step, row, step, color, left-1, skipped = last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1, skipped = last))
                    break

            # not empty square
            elif current.color == color:
                break
            else: # jump on top of opposite color
                last = [current]
            left -= 1
            
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped = []):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right < 0:
                break
            current = self.board[r][right](r, right)
            if current == 0: # found empty square
                if skipped and not last:
                    break;
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last: 
                    if step == -1:
                        row = max(-3, 0)
                    else:
                        row = min( r+ 3, ROWS)

                    # double/tripple  jump
                    moves.update(self._traverse_left(r+step, row, step, color, right-1, skipped = last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1, skipped = last))
                    break

            # not empty square
            elif current.color == color:
                break
            else: # jump on top of opposite color
                last = [current]
            right += 1

        return moves