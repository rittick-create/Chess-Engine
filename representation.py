"""
Using bitboard for tracking ,a 64 bit (idea from={https://healeycodes.com/visualizing-chess-bitboards})
There are 64 positions on a chessboard so we can use bit as on/off

We will use bitwise operators as they are faster cpu operations and 
bitboards are cache friendly since they pack data into fewer memory 
locations.



Board Representation

A board representation encodes a chess position. It needs to record which piece is where, which player is next to move, and if anything can be taken by en passant (as this is not always obvious from the position of the pieces). There are two main approaches to board representations: a board-centric view and a piece-centric-view.


A board-centric view stores a list or set containing each board square, and associates with it an identifier for any piece that occupies it.

A piece-centric view approaches this the other way around. Instead, we allocate a memory location to each piece, and in it, store the square that the piece resides on.


These structures differ in the way they can be accessed. With a board-centric view, it is quite efficient to find the piece located on a square, but it is less straightforward to find the square given a specific piece. The opposite is true for a piece-centric structure



A bitboard is just a 64-bit binary number. We use one bit of this number to represent each square on the board. The bit is set to 1 if that specific piece type occupies the square, and a 0 otherwise. Hence, this is a variation of 1-hot encoding.


a8 b8 c8 d8 e8 f8 g8 h8
a7 b7 c7 d7 e7 f7 g7 h7
a6 b6 c6 d6 e6 f6 g6 h6
a5 b5 c5 d5 e5 f5 g5 h5
a4 b4 c4 d4 e4 f4 g4 h4
a3 b3 c3 d3 e3 f3 g3 h3
a2 b2 c2 d2 e2 f2 g2 h2
a1 b1 c1 d1 e1 f1 g1 h1


56 57 58 59 60 61 62 63
48 49 50 51 52 53 54 55
40 41 42 43 44 45 46 47
32 33 34 35 36 37 38 39
24 25 26 27 28 29 30 31
16 17 18 19 20 21 22 23
 8  9 10 11 12 13 14 15
 0  1  2  3  4  5  6  7



"""

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


"""lets understand the bitboard first using some bitwise functions on it"""
"""
def print_bitboard(bb):
    for row in range(7,-1,-1):
        for col in range(8):
            sq=row*8+col
            if bb & (1<<sq):
                print("1", end=" ")
            else:
                print("0", end=" ")
        print()# to move to new line
        
        
bb = 0
bb |= 1 << Square.F5
bb |= 1 << Square.A1
bb |= 1 << Square.H8

print_bitboard(bb)  

0 0 0 0 0 0 0 1 
0 0 0 0 0 0 0 0 
0 0 0 0 0 0 0 0 
0 0 0 0 0 1 0 0 
0 0 0 0 0 0 0 0 
0 0 0 0 0 0 0 0 
0 0 0 0 0 0 0 0 
1 0 0 0 0 0 0 0 


this was board centric representation to understand what a bitboard is and
how it works but the problem is it does not tell us about the piece which is occupying the position


-------------
To solve this problem we will be using 12 piece centric representation 
6 for whites and 6 for blacks

white_pawns
white_knights
white_bishops
white_rooks
white_queens
white_king

black_pawns
black_knights
black_bishops
black_rooks
black_queens
black_king

we will also keep a 3 board centric ones

white_pieces
black_pieces
all_pieces

where all_pieces=white_pieces|black_pieces

the idea behind having these 3 are:-
•	collision detection
•	sliding piece attacks
•	move legality

"""  

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
def set_bits(next_position):
    global side_to_move
    move = next_position.upper()
    piece_info=move[0]
    position=move[1:]
    
    if(side_to_move==0):
        piece=piece_map_white[piece_info]
        square=Square[position]
        bitboards[piece] |= 1<<square
    else:
        piece=piece_map_black[piece_info]
        square=Square[position]
        bitboards[piece] |= 1<<square
    side_to_move^=1
    
    
    
    
    
    
    
    
    
    
 
    
    
        







