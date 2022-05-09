import pygame
import pygame.gfxdraw
import os
import chess

pygame.font.init()
pygame.mixer.init()

def load_images():
    "Zwraca słownik ze wszyskimi obrazami używanymi w programie"
    IMAGES = {}
    IMAGES["r"] = pygame.transform.scale(pygame.image.load(os.path.join('Assets','b-rook.png')),(BOARD_WIDTH//8,BOARD_HEIGHT//8))
    IMAGES["R"] = pygame.transform.scale(pygame.image.load(os.path.join('Assets','w-rook.png')),(BOARD_WIDTH//8,BOARD_HEIGHT//8))
    IMAGES["n"] = pygame.transform.scale(pygame.image.load(os.path.join('Assets','b-knight.png')),(BOARD_WIDTH//8,BOARD_HEIGHT//8))
    IMAGES["N"] = pygame.transform.scale(pygame.image.load(os.path.join('Assets','w-knight.png')),(BOARD_WIDTH//8,BOARD_HEIGHT//8))
    IMAGES["b"] = pygame.transform.scale(pygame.image.load(os.path.join('Assets','b-bishop.png')),(BOARD_WIDTH//8,BOARD_HEIGHT//8))
    IMAGES["B"] = pygame.transform.scale(pygame.image.load(os.path.join('Assets','w-bishop.png')),(BOARD_WIDTH//8,BOARD_HEIGHT//8))
    IMAGES["q"] = pygame.transform.scale(pygame.image.load(os.path.join('Assets','b-queen.png')),(BOARD_WIDTH//8,BOARD_HEIGHT//8))
    IMAGES["Q"] = pygame.transform.scale(pygame.image.load(os.path.join('Assets','w-queen.png')),(BOARD_WIDTH//8,BOARD_HEIGHT//8))
    IMAGES["k"] = pygame.transform.scale(pygame.image.load(os.path.join('Assets','b-king.png')),(BOARD_WIDTH//8,BOARD_HEIGHT//8))
    IMAGES["K"] = pygame.transform.scale(pygame.image.load(os.path.join('Assets','w-king.png')),(BOARD_WIDTH//8,BOARD_HEIGHT//8))
    IMAGES["p"] = pygame.transform.scale(pygame.image.load(os.path.join('Assets','b-pawn.png')),(BOARD_WIDTH//8,BOARD_HEIGHT//8))
    IMAGES["P"] = pygame.transform.scale(pygame.image.load(os.path.join('Assets','w-pawn.png')),(BOARD_WIDTH//8,BOARD_HEIGHT//8))
    IMAGES["K-danger"] = pygame.transform.scale(pygame.image.load(os.path.join('Assets','w-king-danger.png')),(BOARD_WIDTH//8,BOARD_HEIGHT//8))
    IMAGES["k-danger"] = pygame.transform.scale(pygame.image.load(os.path.join('Assets','b-king-danger.png')),(BOARD_WIDTH//8,BOARD_HEIGHT//8))
    
    return IMAGES

def draw_display():
    "to co się wyświetla na ekranie"

    def draw_board():
        "rysujemy szachownice i wszystkie wyróżnione pola"
        bx,by,bw,bh = BOARD_START_X,BOARD_START_Y,BOARD_WIDTH,BOARD_HEIGHT
        color = COLOR1
        print
        for i in range(8):
            for j in range(8):
                    pygame.draw.rect(WIN,color,pygame.Rect( bx+j*bw//8,by+i*bh//8,bw//8,bh//8))
                    if i*8+j in highlighted_squares: 
                        if gra.board[i*8+j]=="o":pygame.gfxdraw.filled_circle(WIN, bx+j*bw//8+bw//16,by+i*bh//8+bh//16,bh//64, (0,0,0,127))
                        else: 
                            pygame.gfxdraw.filled_trigon(WIN, bx+j*bw//8,by+i*bh//8,bx+j*bw//8+bw//32,by+i*bh//8,bx+j*bw//8,by+i*bh//8+bh//32,(0,0,0,127))
                            pygame.gfxdraw.filled_trigon(WIN, bx+j*bw//8,by+(i+1)*bh//8,bx+j*bw//8+bw//32,by+(i+1)*bh//8,bx+j*bw//8,by+(i+1)*bh//8-bh//32,(0,0,0,127)) 
                            pygame.gfxdraw.filled_trigon(WIN, bx+(j+1)*bw//8,by+i*bh//8,bx+(j+1)*bw//8-bw//32,by+i*bh//8,bx+(j+1)*bw//8,by+i*bh//8+bh//32,(0,0,0,127))
                            pygame.gfxdraw.filled_trigon(WIN, bx+(j+1)*bw//8,by+(i+1)*bh//8,bx+(j+1)*bw//8-bw//32,by+(i+1)*bh//8,bx+(j+1)*bw//8,by+(i+1)*bh//8-bh//32,(0,0,0,127))
                    if i*8+j == start_square: pygame.gfxdraw.box(WIN, pygame.Rect(bx+j*bw//8,by+i*bh//8,bw//8,bh//8), (0,0,0,127))   
                    if i*8+j in trace_squares: pygame.gfxdraw.box(WIN, pygame.Rect(bx+j*bw//8,by+i*bh//8,bw//8,bh//8), (203,203,0,127))              
                    if color == COLOR1 : color = COLOR2
                    else: color = COLOR1
            if color == COLOR1 : color = COLOR2
            else: color = COLOR1
    def draw_pieces():
        bx,by,bw,bh = BOARD_START_X,BOARD_START_Y,BOARD_WIDTH,BOARD_HEIGHT
        board = gra.board
        "przyjmuje tablice z rozmieszczeniem bierek, rysuje je na szachownicy"
        for i in range(8):
            for j in range(8):
                if board[i*8+j]!="o":
                    if board[i*8+j]=="K" and gra.kings_attacked[0] : WIN.blit( IMAGES["K-danger"], (bx+j*bw//8,by+i*bh//8))
                    elif board[i*8+j]=="k" and gra.kings_attacked[1] : WIN.blit( IMAGES["k-danger"], (bx+j*bw//8,by+i*bh//8))
                    else: WIN.blit( IMAGES[board[i*8+j]], (bx+j*bw//8,by+i*bh//8))
        if moving_piece!="o": 
            WIN.blit( IMAGES[moving_piece], (mx+offsetx,my+offsety) )
    def draw_text():
        "rysuje wszystkie napisy na ekranie"
        bx,by,bw,bh = BOARD_START_X,BOARD_START_Y,BOARD_WIDTH,BOARD_HEIGHT

        #eysujemy współrzene na szachownicy
        color = COLOR2
        for i in range(8):
            WIN.blit(COORDS_FONT.render(str(8-i),1,color),(bx,by+i*bh//8))
            if color==COLOR1 : color=COLOR2
            else: color=COLOR1
        color=COLOR1
        for i in range(8):
            WIN.blit(COORDS_FONT.render(chr(97+i),1,color),(bx+(i+1)*bw//8-10,by+bh-16))
            if color==COLOR1 : color=COLOR2
            else: color=COLOR1

        if gra.turn : color1,color2 = (255,153,153),(255,255,255)
        else : color1,color2 = (255,255,255),(255,153,153)            
        WIN.blit(NAME_FONT.render("Gracz 2",1,color2 ),(bx+bw-100,by-40))
        WIN.blit(NAME_FONT.render("Gracz 1",1,color1 ),(bx+bw-100,by+bh))
        
    WIN.fill((64,64,64))
    draw_board()
    draw_text()
    draw_pieces()
    pygame.display.update()

def mouse_pos_to_square(x,y):
    "na którym polu planszy znajduje się teraz mysz"
    bx,by,bw,bh=BOARD_START_X,BOARD_START_Y,BOARD_WIDTH,BOARD_HEIGHT
    if x>bx and x<bx+bw and y>by and y<by+bh:
        return (y-by)//(bh//8)*8+(x-bx)//(bw//8)
    else: return -1   
def get_offset_from_square(x,y,sq):
    "zwraca przesunięcie od pozycji myszy do początku pola sq "
    bx,by,bw,bh=BOARD_START_X,BOARD_START_Y,BOARD_WIDTH,BOARD_HEIGHT
    if sq==-1: return 0,0
    else: return bx+sq%8*bw//8-x,by+sq//8*bh//8-y 

#parametry szachownicy
COLOR1 = 	(118,150,86)
COLOR2 = (238,238,210)
WIDTH = 800
HEIGHT = 800
BOARD_WIDTH = 600
BOARD_HEIGHT = 600
BOARD_START_X = 100
BOARD_START_Y = 100

#parametry napisów
NAME_FONT = pygame.font.SysFont('arial',30)
COORDS_FONT = pygame.font.SysFont('arial',15)

#parametry dzwięków
MOVE_SOUND = pygame.mixer.Sound(os.path.join('Assets','move.wav'))
MOVE_SOUND.set_volume(0.2)
CAPTURE_SOUND = pygame.mixer.Sound(os.path.join('Assets','capture.wav'))
CAPTURE_SOUND.set_volume(0.2)

FPS = 60
clock = pygame.time.Clock()
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Szachy")

IMAGES = load_images()
gra = chess.Game_of_Chess()
gra.fill_board()

run = True
highlighted_squares=[]
trace_squares = []
moving_piece = "o"
start_square=-1
offsetx,offsety = 0,0

while run:
    clock.tick(FPS)
    mx,my = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: run = False
        if event.type == pygame.MOUSEBUTTONDOWN: 
            start_square = mouse_pos_to_square(mx,my)
            highlighted_squares = gra.get_moves(start_square)
            if start_square!=-1: moving_piece = gra.board[start_square]
            offsetx,offsety = get_offset_from_square(mx,my,start_square)


        if event.type == pygame.MOUSEBUTTONUP: 
            end_square = mouse_pos_to_square(mx,my)
            if mouse_pos_to_square(mx,my) in highlighted_squares : 
                if gra.board[end_square]=="o": MOVE_SOUND.play()
                else: CAPTURE_SOUND.play()
                gra.move_piece(start_square,end_square)
                trace_squares = [start_square,end_square]

            highlighted_squares=[]
            start_square=-1
            moving_piece = "o"
            offsetx,offsety = 0,0
    
    draw_display()
    


pygame.quit()