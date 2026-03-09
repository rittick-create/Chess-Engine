

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

occupancies = [0] * 3

class Board(IntEnum):
    WHITE_PIECES=0
    BLACK_PIECES=1
    FULL_BOARD=2    
    
    
WHITE = 0
BLACK = 1

side_to_move = WHITE    
 
"""-------------------------"""
#setting up the next position
# user passes the next position    

def set_bits(next_position, previous_square=None):
    global side_to_move
    move = next_position.upper()
    piece_info = move[0]
    position = move[1:]
    
    if side_to_move == WHITE:
        piece = piece_map_white[piece_info]
    else:
        piece = piece_map_black[piece_info]
    
    square = Square[position]

    # Remove previous bit if given
    if previous_square is not None:
        bitboards[piece] &= ~(1 << previous_square)

    # Set new bit
    bitboards[piece] |= 1 << square
    
    # Update occupancies
    occupancies[Board.WHITE_PIECES] = sum(bitboards[Piece.WHITE_PAWN:Piece.WHITE_KING + 1])
    occupancies[Board.BLACK_PIECES] = sum(bitboards[Piece.BLACK_PAWN:Piece.BLACK_KING + 1])
    occupancies[Board.FULL_BOARD] = occupancies[Board.WHITE_PIECES] | occupancies[Board.BLACK_PIECES]

    side_to_move ^= 1
    

     
        
def print_board_unicode():
    symbol_map = {
        Piece.WHITE_PAWN: "♙", Piece.WHITE_KNIGHT: "♘", Piece.WHITE_BISHOP: "♗",
        Piece.WHITE_ROOK: "♖", Piece.WHITE_QUEEN: "♕", Piece.WHITE_KING: "♔",
        Piece.BLACK_PAWN: "♟", Piece.BLACK_KNIGHT: "♞", Piece.BLACK_BISHOP: "♝",
        Piece.BLACK_ROOK: "♜", Piece.BLACK_QUEEN: "♛", Piece.BLACK_KING: "♚"
    }

    print("  a b c d e f g h")
    for row in range(7, -1, -1):
        print(8 - row, end=" ")  # Rank numbers
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
    print("  a b c d e f g h\n")  # File letters at bottom    
    
   
    
    
    
    
 
    
    
        







