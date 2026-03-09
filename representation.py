

from enum import IntEnum


class Square(IntEnum):
    A1=0;  B1=1;  C1=2;  D1=3;  E1=4;  F1=5;  G1=6;  H1=7
    A2=8;  B2=9;  C2=10; D2=11; E2=12; F2=13; G2=14; H2=15
    A3=16; B3=17; C3=18; D3=19; E3=20; F3=21; G3=22; H3=23
    A4=24; B4=25; C4=26; D4=27; E4=28; F4=29; G4=30; H4=31
    A5=32; B5=33; C5=34; D5=35; E5=36; F5=37; G5=38; H5=39
    A6=40; B6=41; C6=42; D6=43; E6=44; F6=45; G6=46; H6=47
    A7=48; B7=49; C7=50; D7=51; E7=52; F7=53; G7=54; H7=55
    A8=56; B8=57; C8=58; D8=59; E8=60; F8=61; G8=62; H8=63



bitboards = [0] * 12 # creates a list of 12  integers(0)
occupancies = [0] * 3


# a piece enum class to map with bitboard
class Piece(IntEnum):
    WHITE_PAWN = 0
    WHITE_KNIGHT = 1
    WHITE_BISHOP = 2
    WHITE_ROOK = 3
    WHITE_QUEEN = 4
    WHITE_KING = 5
    BLACK_PAWN = 6
    BLACK_KNIGHT = 7
    BLACK_BISHOP = 8
    BLACK_ROOK = 9
    BLACK_QUEEN = 10
    BLACK_KING = 11
    

piece_map_white = {
    "P": Piece.WHITE_PAWN,
    "N": Piece.WHITE_KNIGHT,
    "B": Piece.WHITE_BISHOP,
    "R": Piece.WHITE_ROOK,
    "Q": Piece.WHITE_QUEEN,
    "K": Piece.WHITE_KING
}


piece_map_black = {
    "P": Piece.BLACK_PAWN,
    "N": Piece.BLACK_KNIGHT,
    "B": Piece.BLACK_BISHOP,
    "R": Piece.BLACK_ROOK,
    "Q": Piece.BLACK_QUEEN,
    "K": Piece.BLACK_KING
}



class Board(IntEnum):
    WHITE_PIECES=0
    BLACK_PIECES=1
    FULL_BOARD=2    
    
    
WHITE = 0
BLACK = 1

side_to_move = WHITE   

"--------------------------------------------------------------------------------------"
#function for updating occupancies

def update_occupancies():
    white = 0
    for p in range(Piece.WHITE_PAWN, Piece.WHITE_KING + 1):
        white |= bitboards[p]
    
    black = 0
    for p in range(Piece.BLACK_PAWN, Piece.BLACK_KING + 1):
        black |= bitboards[p]
    
    occupancies[Board.WHITE_PIECES] = white
    occupancies[Board.BLACK_PIECES] = black
    occupancies[Board.FULL_BOARD] = white | black 
 

"--------------------------------------------------------------------------------------"

#to get the piece at a particular square
def get_piece_at(square):
    for index,bb in enumerate(bitboards):
        if(bb & 1<<square):
            return Piece(index)
    return None


"--------------------------------------------------------------------------------------"
#setting up the next position
# user passes the next position  

# the user will pass something like qc6=>Q C6
#previous square will be set while runnung the game probably using do while or something  

def set_bits(next_position, previous_square=None):
   
    
    global side_to_move
    move = next_position.upper()
    piece_info = move[0]
    position = move[1:]
    
    if len(move) < 3:
        print(f"[Error] Invalid input '{next_position}' — expected format like 'PA2' or 'NF3'")
        return
    
  

    if side_to_move == WHITE:
        piece = piece_map_white[piece_info]
    else:
        piece = piece_map_black[piece_info]

    square = Square[position]

    #handling capture
    target_piece = get_piece_at(square)
    if target_piece is not None:
        bitboards[target_piece] &= ~(1 << square)  # clear enemy piece

    #handling previous bit
    if previous_square is not None:
        bitboards[piece] &= ~(1 << previous_square)

    # Setting up new bit
    bitboards[piece] |= 1 << square

    update_occupancies()
    side_to_move ^= 1
    

"--------------------------------------------------------------------------------------"
     
 
"--------------------------------------------------------------------------------------"       
def print_board_unicode():
    symbol_map = {
        Piece.WHITE_PAWN: "♙", Piece.WHITE_KNIGHT: "♘", Piece.WHITE_BISHOP: "♗",
        Piece.WHITE_ROOK: "♖", Piece.WHITE_QUEEN: "♕", Piece.WHITE_KING: "♔",
        Piece.BLACK_PAWN: "♟", Piece.BLACK_KNIGHT: "♞", Piece.BLACK_BISHOP: "♝",
        Piece.BLACK_ROOK: "♜", Piece.BLACK_QUEEN: "♛", Piece.BLACK_KING: "♚"
    }

    print("  a b c d e f g h")
    print()
    for row in range(7, -1, -1):
        print(8 - row, end="  ")  # Rank numbers
        for col in range(8):
            sq = row * 8 + col
            piece_found = False
            for piece_index, bb in enumerate(bitboards):
                if bb & (1 << sq):
                    print(symbol_map[Piece(piece_index)], end=" ")
                    piece_found = True
                    break
            if not piece_found:
                print("·", end=" ")  # Empty square
        print(" ", 8 - row)  # Rank numbers again
    print()    
    print("  a b c d e f g h\n")  # File letters at bottom    

"--------------------------------------------------------------------------------------"    
   
#creating    intital bits and running the play

    
"""        

FEN (Forsyth-Edwards Notation) -A single line sting notation for a chess board

example-
"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" 
Right now we only use parts 1 and 2. The rest will matter later.

w refers to the side which is going to move

and fen[0] represents all the positions



"""



def load_fen(fen: str):
    global side_to_move, bitboards, occupancies

    #reset everything will probably remove this later or have to find some solution
    bitboards[:] = [0] * 12
    occupancies[:] = [0] * 3

    fen_parts = fen.strip().split()
    if len(fen_parts) < 2:
        print("[Error] Invalid FEN — too short")
        return

    board_part = fen_parts[0]
    turn = fen_parts[1]

    #this is for the ones where fen[0][i] is actually a piece(Char)
    fen_piece_map = {
        "P": Piece.WHITE_PAWN,   "N": Piece.WHITE_KNIGHT,
        "B": Piece.WHITE_BISHOP, "R": Piece.WHITE_ROOK,
        "Q": Piece.WHITE_QUEEN,  "K": Piece.WHITE_KING,
        "p": Piece.BLACK_PAWN,   "n": Piece.BLACK_KNIGHT,
        "b": Piece.BLACK_BISHOP, "r": Piece.BLACK_ROOK,
        "q": Piece.BLACK_QUEEN,  "k": Piece.BLACK_KING,
    }


    rank = 7
    file = 0

    for char in board_part:
        if char == "/":
            rank -= 1
            file = 0
        elif char.isdigit():
            file += int(char)       # skip empty squares
        elif char in fen_piece_map:
            square = rank * 8 + file
            bitboards[fen_piece_map[char]] |= 1 << square
            file += 1
        else:
            print(f"[Error] Unknown FEN character '{char}'")
            return

    side_to_move = WHITE if turn == "w" else BLACK
    update_occupancies()
    print(f" FEN loaded. {'White' if side_to_move == WHITE else 'Black'} to move.")


"--------------------------------------------------------------------------------------"    

load_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
print_board_unicode()