# %%
import threading
import keyboard
import os
import time
from rich.console import Console
from rich.text import Text
from rich.table import Table
import _thread

console = Console()

black_pieces_raw = {"K": "♔", "Q": "♕", "R": "♖", "B": "♗", "N": "♘", " ": "♙"}
black_pieces_r = {"K": "♔", "Q": "♕", "R": "♖", "B": "♗", "N": "♘", " ": "♙"}
white_pieces_raw = {"K": "♚", "Q": "♛", "R": "♜", "B": "♝", "N": "♞", " ": "♟"}

# %%
def conversion(Initial, Turn):
    if Initial in white_pieces_raw:
        if ((Turn + 2) % 2) == 0:
            return white_pieces_raw[Initial]
        else:
            return black_pieces_raw[Initial]
    else:
        return 'Incorrect Initial.'


# %%
class chess_pieces:
    def __init__(self, symbol, color, Initial):
        self.symbol = symbol
        self.initial = Initial
        self.color = color
        if Initial is None:
            self.First = True
    def check_moves(self, x):
        for elem in x:
            if (elem < 1) or (elem > 8):
                return True
        return False
    def moves(self, current_pos, main_pos = None, sec_pos = None,  Initial="Default", dangerZones = []):
        possible_moves = []
        if Initial == "Default":
            Initial = self.initial
        x, y = current_pos
        a1, a2, a3, a4 = 1, 1, 1, 1
        if Initial == "K":
            for i in [-1, 1, 0]:
                for j in [-1, 1, 0]:
                    if i == 0 and j == 0:
                        pass
                    else:
                        pos = (x + i, y + j)
                        if (pos not in main_pos) and (pos not in dangerZones):
                            possible_moves.append(pos)
        elif Initial == "R":
            for i in range(1, 8):
                pos1 = ((x - i)*a1, y*a1)
                pos2 = (x*a1, (y - i)*a2)
                pos3 = ((x + i)*a3, y*a3)
                pos4 = (x*a4, (y + i)*a4)
                if pos1 in main_pos:
                    pos1 = (0, 0)
                    a1 = 0
                elif pos1 in sec_pos:
                    a1 = 0
                if pos2 in main_pos:
                    pos2 = (0, 0)
                    a2 = 0
                elif pos1 in sec_pos:
                    a2 = 0
                if pos3 in main_pos:
                    pos3 = (0, 0)
                    a3 = 0
                elif pos3 in sec_pos:
                    a3 = 0
                if pos4 in main_pos:
                    pos4 = (0, 0)
                    a4 = 0
                elif pos3 in sec_pos:
                    a4 = 0
                possible_moves.append(pos1)
                possible_moves.append(pos2)
                possible_moves.append(pos3)
                possible_moves.append(pos4)
        elif Initial == "B":
            for i in range(1, 8):
                pos1 = ((x + i)*a1, (y + i)*a1)
                pos2 = ((x - i)*a2, (y + i)*a2)
                pos3 = ((x + i)*a3, (y - i)*a3)
                pos4 = ((x - i)*a4, (y - i)*a4)
                if pos1 in main_pos:
                    pos1 = (0, 0)
                    a1 = 0
                elif pos1 in sec_pos:
                    a1 = 0
                if pos2 in main_pos:
                    pos2 = (0, 0)
                    a2 = 0
                elif pos2 in sec_pos:
                    a2 = 0
                if pos3 in main_pos:
                    pos3 = (0, 0)
                    a3 = 0
                elif pos3 in sec_pos:
                    a3 = 0
                if pos4 in main_pos:
                    pos4 = (0, 0)
                    a4 = 0
                elif pos3 in sec_pos:
                    a4 = 0
                possible_moves.append(pos1)
                possible_moves.append(pos2)
                possible_moves.append(pos3)
                possible_moves.append(pos4)
        elif Initial == "Q":
            possible_moves.extend(self.moves(current_pos, main_pos, sec_pos, "B"))
            possible_moves.extend(self.moves(current_pos, main_pos, sec_pos, "R"))
        elif Initial == "N":
            corners = []
            for i in [1, -1]:
                pos1 = (x + 2 * i, y - i)
                pos2 = (x + i, y - 2 * i)
                pos3 = (x + 2 * i, y + i)
                pos4 = (x + i, y + 2 * i)
                if pos1 not in main_pos: corners.append(pos1)
                if pos2 not in main_pos: corners.append(pos2)
                if pos3 not in main_pos: corners.append(pos3)
                if pos4 not in main_pos: corners.append(pos4)
            possible_moves.extend(corners)
        elif Initial is None:
            factor = 1 if self.color == "white" else -1
            pos1 = (x - 1*factor, y)
            if pos1 not in main_pos and pos1 not in sec_pos: possible_moves.append(pos1)
            if self.First:
                pos2 = (x - 2*factor, y)
                if pos2 not in main_pos and pos2 not in sec_pos: possible_moves.append(pos2)
            pos2 = (x - 1*factor, y+1)
            pos3 = (x - 1*factor, y-1)
            if pos2 in sec_pos : possible_moves.append(pos2)
            if pos3 in sec_pos: possible_moves.append(pos3)
        count = 0
        possible_moves = [pos for pos in possible_moves if pos != (0,0)]
        possible_moves = list(set(possible_moves))
        index_list = [possible_moves.index(pos) for pos in possible_moves if self.check_moves(pos)]
        print("possible moves: ", possible_moves, "\nindex_list: ", index_list)
        for index in index_list:
            print(index - count)
            possible_moves.pop(index - count)
            count += 1
        print(sorted(possible_moves, reverse = True))
        return possible_moves

# %%
w_pieces = {}
b_pieces = {}

for b_i, b_s in white_pieces_raw.items():
    if b_i == " ":
        b_i = None
    piece = chess_pieces(b_s, "black", b_i)
    if (piece.initial is not None):
        b_pieces[piece.initial] = piece
    else:
        b_pieces["p"] = piece

for w_i, w_s in black_pieces_raw.items():
    if w_i == " ":
        w_i = None
    piece = chess_pieces(w_s, "white", w_i)
    if (piece.initial is not None):
        w_pieces[piece.initial] = piece
    else:
        w_pieces["p"] = piece
# %%
class Square():
    def __init__(self, pos, state, piece = None):
        self.state = state
        self.states_ = {0: "Empty", 1: "Occupied"}
        self.styles = {"chosen": "on blue", "valid" : "on green", "eliminate" : "on red"}
        self.style_ = "on white" if (sum(pos)%2 == 0) else "on black"
        self.style = self.style_
        self.pos = pos
        if(state == 0):
            self.symbol = ""
            self.piece = None
        elif(state == 1):
            self.symbol = piece.symbol
            self.piece = piece
    def set_state(self, state, piece = None):
        if (state == self.state):
            pass
        elif(state == 0):
            self.state = 0
            self.symbol = self.symbol_
            self.piece = None
        elif(state == 1):
            self.state = 1
            self.symbol = piece.symbol
            self.piece = piece
    def return_square(self, x = 1):
        if (self.state == 1):  
            return Text(f"\n   {self.symbol}\n", style = self.piece.color + " " + self.style)
        else:
            return Text(f"\n    \n", style = self.style)
    def return_style(self, x = 1):
        return self.style_
    def return_pos(self, x):
        return self.pos
    def reset_style(self):
        self.style = self.style_
    def set_style(self, type):
        self.reset_style()
        self.style = self.styles[type]
    def set_piece(self, piece):
        self.state = 1
        self.piece = piece
        print(f"piece set is: {piece.symbol}")
    def remove_piece(self):
        self.state = 0
        self.piece = None
    

# %%
class Board:
    def __init__(self):
        self.updates = 1
        self.board_ = Table.grid()
        black_piece_positions = []
        for i in range(1, 3):
            for j in range(1, 9):
                black_piece_positions.append((i, j))
        self.black_piece_positions = black_piece_positions
        white_piece_positions = []
        for i in range(7, 9):
            for j in range(1, 9):
                white_piece_positions.append((i, j))
        self.white_piece_positions = white_piece_positions
        self.board = {}
        up_pieces = ["R", "N", "B", "Q", "K", "B", "N", "R", "p", "p", "p", "p", "p", "p", "Q", "p"]
        down_pieces = ["p", "p", "p", "p", "p", "p", "p", "p", "R", "N", "B", "Q", "K", "B", "N", "R",]
        for i in range(3, 7):
            for j in range(1, 9):
                self.board.setdefault(i, []).append(Square((i, j), 0))
        for pos, piece in zip(black_piece_positions, up_pieces):
            b_piece = b_pieces[piece]
            self.board.setdefault(pos[0], []).append(Square(pos, 1, chess_pieces(b_piece.symbol,b_piece.color, b_piece.initial)))
        for pos, piece in zip(white_piece_positions, down_pieces):
            w_piece = w_pieces[piece]
            self.board.setdefault(pos[0], []).append(Square(pos, 1, chess_pieces(w_piece.symbol, w_piece.color, w_piece.initial)))
        print(self.board)
        self.board[2][3].remove_piece()
        self.board[7][4].remove_piece()
        self.board[7][3].remove_piece()
        #self.board[8][3].set_piece(chess_pieces(w_pieces["R"].symbol, w_pieces["R"].color, w_pieces["R"].initial))
        self.black_piece_positions.remove((2,4))
        self.white_piece_positions.remove((7,5))
        self.white_piece_positions.remove((7,3))
        self.checkTurn()
        self.scan()
        self.set_table()
        print("black pieces: ", black_piece_positions)
        print("white pieces: ", white_piece_positions)
    def set_table(self):
        self.board_ = Table.grid()
        for i in range(8):
            self.board_.add_column(header = None, width = 8)
        for row in sorted(self.board.keys()):
            self.board_.add_row(*[x.return_square() for x in self.board[row]])
    def display_table(self):
        console.print(self.board_)
    def checkTurn(self):
        self.turn = "white" if (self.updates % 2 == 1) else "black"
        self.curr_team = self.black_piece_positions if self.turn == "black" else self.white_piece_positions
        self.opp_team = self.black_piece_positions if self.turn == "white" else self.white_piece_positions
    def scan(self, visualize = False):
        self.dangerPositions = []
        for positions in self.opp_team:
            square = self.board[positions[0]][positions[1] -1]
            moves = square.piece.moves(positions, main_pos = self.opp_team, sec_pos = self.curr_team)
            if(visualize):
                for pos in moves:
                    self.board[pos[0]][pos[1] - 1].set_style("eliminate")
            self.dangerPositions.extend(moves)
    def choose(self, pos : tuple):
        print("choose function: " , pos)
        if pos is None:
            return 0
        if sum(pos) < 17:
            square = self.board[pos[0]][pos[1]-1]
            square.set_style("chosen")
            self.turn = "white" if (self.updates % 2 == 1) else "black"
            if ((square.state == 1) and (square.piece.color == self.turn)):
                moves = square.piece.moves(pos, main_pos = self.curr_team, sec_pos = self.opp_team, dangerZones = self.dangerPositions if square.piece.initial == "K" else None)
                for positions in moves:
                    currentSquare= self.board[positions[0]][positions[1]-1]
                    currentSquare.set_style("valid") if positions not in self.opp_team else currentSquare.set_style("eliminate")
                self.set_table()
                for positions in moves: self.board[positions[0]][positions[1]-1].reset_style()
            else:
                self.set_table()
            square.reset_style()
        else:
            print("Error: out of range.")
    def snap(self, dir : str, curr_pos : tuple):
        c_pos = curr_pos
        print(dir, "direction to snap", curr_pos)
        if dir == "left":
            add = (0,-1)
        elif dir == "right":
            add = (0, 1)
        elif dir == "up":
            add = (-1, 0)
        elif dir == "down":
            add = (1, 0)
        pos_list = []
        while (True):
            curr_pos = ((curr_pos[0] + add[0]), (curr_pos[1] + add[1]))
            if (curr_pos[0] > 8 or curr_pos[1] > 8) or (curr_pos[0] < 1 or curr_pos[1] < 1):
                break
            pos_list.append(curr_pos)
        print(pos_list)
        if self.turn == "white":
            valid_values = sorted([pos for pos in self.white_piece_positions if pos in pos_list])
        else:
            valid_values = sorted([pos for pos in self.black_piece_positions if pos in pos_list])
        print(valid_values)
        if valid_values:
            for value in valid_values:
                moves = self.board[value[0]][value[1]].piece.moves(value, main_pos = self.black_piece_positions if self.turn == "black" else self.white_piece_positions, sec_pos = self.black_piece_positions if self.turn == "white" else self.white_piece_positions)
                print(moves)
                if len(moves) != 0:
                    return value
        else:
            return c_pos


# %%
# current_pos = (5, 4)
# moves = w_pieces[3].moves(current_pos)
# print(moves)

# for i in range(1, 9):
#     for j in range(1, 9):
#         if (i, j) == current_pos:
#             print("I", end="  ")
#         elif (i, j) not in moves:
#             print("O  ", end="")
#         else:
#             print("X  ", end="")
#     print()

# %%
table = Table.grid()
table.add_column(width = 8)
table.add_column(width = 8)
table.add_column(width = 8)
console.print(table)
king = Text("\n   \n", style = "black on white")
queen = Text("\n   \n", style = "black on black")
pawn = Text("\n   ♟\n", style = "black on white")
pieces = [king, queen, pawn]
pieces_table = []
# for i in range(0, 8):
#     pieces_table.append(pieces)
# for piece in pieces_table:
#     table.add_row(*piece)
#table.add_row(*[king, queen, pawn])
#table.add_row(*[queen, king, queen])
#table.add_row(*[king, queen, king])
#table.add_row(*[queen, king, queen])
# table.add_row(*[king, king, king])
# table.add_row(*[king, king, king])
# table.add_row(*[king, king, king])
# table.add_row(*[king, king, king])
# count = 1
# while(True):
#     if (count%2 == 1):
#         table.add_row(*[queen, king, queen])
#     else:
#         table.add_row(*[king, queen, king])
#     console.print(table)
#     time.sleep(0.5)
#     os.system("cls")
#     count += 1
#     if (count == 10):
#         break
toggle = False
def toggle_state():
    global toggle
    while True:
        keyboard.wait("q")
        keyboard.press_and_release("backspace")
        if not toggle:
            keyboard.press_and_release("enter")
        toggle = not toggle

threading.Thread(target = toggle_state, daemon= True).start()

test_board = Board()
pos = (1,1)

test_board.display_table()
prev_time = 0
prev_event = ""
flag = False
checked = [False, ""]
while(True):
    if not toggle:
        print("In standard input mode, enter position to navigate board.")
        print("Press q to switch to keyboard input mode.")
        try:
            pos = tuple(map(int, input("Enter position to choose(comma separated): ").split(",")))
        except ValueError:
            os.system("cls")
            test_board.display_table()
            continue
        if(pos == (0, 0)):
            test_board.set_table()
    if toggle:
        if not checked[0]:
            print("In keyboard input mode, use arrow keys to navigate board.")
            print("Press q to switch to standard input mode.")
        event = keyboard.read_event(suppress=True)
        if(event.event_type == keyboard.KEY_DOWN):
            current_time = event.time - prev_time
            prev_time = event.time
            flag = False
            if event.name == "q":
                toggle = not toggle
                os.system("cls")
                test_board.display_table()
                continue
            elif event.name == "left":
                flag = True
                pos = (pos[0], pos[1]-1 if pos[1] > 1 else 8)
            elif event.name == "right":
                flag = True
                pos = (pos[0], pos[1]+1 if pos[1] < 8 else 1)
            elif event.name == "up":
                flag = True
                pos = (pos[0] - 1 if pos[0] > 1 else 8, pos[1])
            elif event.name == "down":
                flag = True
                pos = (pos[0] + 1 if pos[0] < 8 else 1, pos[1])
            if (flag):
                if (current_time < 0.25) and (prev_event == event.name):
                    print(f"{event.name} pressed twice quickly.")
                    prev_event = ""
                    checked[0] = True
                    checked[1] = event.name
                else:
                    checked[0] = False
                    prev_event = event.name
                if checked[0]:
                    os.system("cls")
                    pos = test_board.snap(checked[1], pos)
                    test_board.choose(pos)
                    test_board.display_table()
                    print("snapped")
                    continue
    if not checked[0]:
        os.system("cls")   
        print(pos)
        test_board.choose(pos)
        test_board.display_table()
    print(checked)



# %%
