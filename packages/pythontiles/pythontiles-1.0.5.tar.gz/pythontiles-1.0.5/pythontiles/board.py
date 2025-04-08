from . import nmedecode as nme

class Board:
    # Setting Up Board
    def __init__(self):
        self.height = None
        self.width = None
        self.board = None

    def board_size(self, height, width):
        self.height = height
        self.width = width

    def reset_to_empty(self):
        self.board = [["empty" for j in range(0, self.height)] for i in range(0, self.width)]

    def import_from_nme(self, filename):
        file = nme.NME_Decode_File(filename)
        self.board = file
        self.board_size(len(file), len(file[0]))

    #Information Checks
    def value_at_tile(self, x, y):
        return self.board[y - 1][x - 1]

    def is_legal_tile(self, x, y):
        return not (x < 1 or y < 1 or x > self.width or y > self.height)

    # Moving Pieces
    def change_tile(self, x, y, text):
        self.board[y - 1][x - 1] = text

    def move_piece(self, x1, y1, x2, y2):
        if not self.is_legal_tile(x1, y1) or not self.is_legal_tile(x2, y2):
            print("Error Not Legal Tile")
            quit()
        text = self.value_at_tile(x1, y1)
        self.change_tile(x1, y1, "empty")
        self.change_tile(x2, y2, text)
