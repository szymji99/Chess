import copy

class Game_of_Chess:

    def __init__(self):
        self.turn = True  #czyja jest tura
        self.move_counter = 0  #ile ruchów zostąło wykonanych
        self.enpassant = -1 #pole, które można bić w przelocie.
        self.castle = [True,True] #czy król białych i czarnych się ruszył
        self.board = ["o" for i in range(64)] #ustawienie bierek na szachownicy
        self.white=[] #pola na których stoją białe bierki
        self.black=[] #pola na których stoją czarne bierki
        self.kings = [-1,-1] #pola na których stoją króle
        self.kings_attacked=[False,False] #czy król danego kolru jest w szachu
    
    def fill_board(self):
        "ustawia bierki w startowej pozycji"
        fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
        i=0
        for x in fen:
            if x=="/":continue
            elif ord(x)<=57 and ord(x)>=48: 
                for j in range(ord(x)-48):
                    self.board[i]="o"
                    i+=1
                    
            else :
                self.board[i]=x
                if x.isupper(): 
                    self.white.append(i)
                    if x=="K": self.kings[0]=i
                else: 
                    self.black.append(i)
                    if x=="k":self.kings[1]=i
                i+=1
        self.kings_attacked = self.is_square_controlled(self.kings[0],False),self.is_square_controlled(self.kings[1],True)
    
    def get_moves_unsafeking(self,i,turn):
        "zwraca dostępne ruchy dla figury z danego pola nie biorąc pod uwagę bezpieczeństwa króla. Turn informuje czyja jest tura."
               
        def get_rook_moves(i,color):
            "Zwraca ruchy dla wieży koloru color"
            x =i%8
            y =i//8
            moves=[]
            squares = []
            squares.append([(j,y) for j in range(x+1,8)])
            squares.append([(j,y) for j in range(x-1,-1,-1)])
            squares.append([(x,j) for j in range(y+1,8)])
            squares.append([(x,j) for j in range(y-1,-1,-1)])

            for lines in squares:
                for sq in lines:
                    if self.board[sq[0]+8*sq[1]]=="o": moves.append(sq[0]+8*sq[1])
                    else : 
                        if self.board[sq[0]+8*sq[1]].isupper()!=color : moves.append(sq[0]+8*sq[1])
                        break
            return moves 
        def get_bishop_moves(i,color):
            "Zwraca ruchy dla gońca koloru color"   
            x = i%8
            y = i//8
            moves = []
            squares = []
            squares.append([(x+i,y+i) for i in range(1,8) if x+i<8 and y+i<8])
            squares.append([(x-i,y-i) for i in range(1,8) if x-i>=0 and y-i>=0])
            squares.append([(x+i,y-i) for i in range(1,8) if x+i<8 and y-i>=0])
            squares.append([(x-i,y+i) for i in range(1,8) if x-i>=0 and y+i<8])
            for lines in squares:
                for sq in lines:
                    if self.board[sq[0]+8*sq[1]]=="o": moves.append(sq[0]+8*sq[1])
                    else : 
                        if self.board[sq[0]+8*sq[1]].isupper()!=color : moves.append(sq[0]+8*sq[1])
                        break
            return moves 
        def get_queen_moves(i,color):
            "Zwraca ruchy dla królowej koloru color"
            moves = get_bishop_moves(i,color)+get_rook_moves(i,color)
            return moves
        def get_knight_moves(i,color):
            "Zwraca ruchy dla skoczka koloru color"   
            x = i%8
            y = i//8
            moves = []
            squares = []
            squares.extend([(x+2,y+1),(x+2,y-1),(x-2,y+1),(x-2,y-1),(x+1,y+2),(x+1,y-2),(x-1,y+2),(x-1,y-2)])
            for sq in squares[:]:
                if sq[0] in range(8) and sq[1] in range(8):
                    if self.board[sq[0]+sq[1]*8]=="o": moves.append(sq[0]+8*sq[1])
                    elif self.board[sq[0]+sq[1]*8].isupper()!=color: moves.append(sq[0]+8*sq[1])
            return moves

        def get_king_moves(i,color):
            "Zwraca ruchy dla króla koloru color"   
            x = i%8
            y = i//8
            moves = []
            squares = []
            squares.extend([(x+1,y+1),(x+1,y),(x+1,y-1),(x-1,y+1),(x-1,y),(x-1,y-1),(x,y+1),(x,y-1)])
            for sq in squares[:]:
                if sq[0] in range(8) and sq[1] in range(8):
                    if self.board[sq[0]+sq[1]*8]=="o": moves.append(sq[0]+8*sq[1])
                    elif self.board[sq[0]+sq[1]*8].isupper()!=color: moves.append(sq[0]+8*sq[1])
            
            return moves
        def get_pawn_moves(i,color):
            "Zwraca ruchy dla pionka koloru color"
            x = i%8
            y = i//8
            moves=[]
            if color:
                if self.board[i-8]=="o": 
                    moves.append(i-8)
                    if y==6 and self.board[i-16]=="o": moves.append(i-16)
                if x+1 in range(8) and (self.board[i-7]!="o" and not self.board[i-7].isupper()) or (i-7 == self.enpassant): moves.append(i-7)
                if x-1 in range(8) and (self.board[i-9]!="o" and not self.board[i-9].isupper()) or (i-9 == self.enpassant): moves.append(i-9)
            else:
                if self.board[i+8]=="o": 
                    moves.append(i+8)
                    if y==1 and self.board[i+16]=="o": moves.append(i+16)
                if x+1 in range(8) and ( (self.board[i+9]!="o" and self.board[i+9].isupper()) or (i+9 == self.enpassant) ): moves.append(i+9)
                if x-1 in range(8) and ( (self.board[i+7]!="o" and self.board[i+7].isupper()) or (i+7 == self.enpassant) ): moves.append(i+7)
            return moves
        moves=[]
        if self.board[i] != "o" and self.board[i].isupper() == turn:
            if self.board[i]=="r" or self.board[i]=="R": moves=get_rook_moves(i,turn)
            if self.board[i]=="b" or self.board[i]=="B": moves=get_bishop_moves(i,turn)
            if self.board[i]=="n" or self.board[i]=="N": moves=get_knight_moves(i,turn)
            if self.board[i]=="q" or self.board[i]=="Q": moves=get_queen_moves(i,turn)
            if self.board[i]=="k" or self.board[i]=="K": moves=get_king_moves(i,turn)
            if self.board[i]=="p" or self.board[i]=="P": moves=get_pawn_moves(i,turn)
        return moves
    def is_square_controlled(self,i,color):
        "zwraca prawdę, jesli dane pole jest atakowane przez bierki koloru color"
        if color: squares =self.white
        else: squares = self.black
        for sq in squares:
                if self.board[sq]=="p":
                    if sq%8>0 and sq+7==i: return True
                    if sq%8<7 and sq+9==i: return True
                elif self.board[sq]=="P":
                    if sq%8>0 and sq-9==i: return True
                    if sq%8<7 and sq-7==i: return True
                else:
                    if i in self.get_moves_unsafeking(sq,color): return True
        return False

    def move_piece(self,i,j):
        "przesuwa bierkę z pola i do pola j. Zakładamy, że wiemy już, że to jest poprawny ruch"
        self.turn = not self.turn
        self.move_counter+=1
        if (self.board[i] =="p" or self.board[i] =="P") and (abs(i-j)==16): self.enpassant=int((i+j)/2)
        else : self.enpassant = -1
        if self.board[i] =="k" : 
            self.castle[1]=False
            self.kings[1]=j
        if self.board[i] =="K" : 
            self.castle[0]=False
            self.kings[0]=j
        if self.board[i].isupper(): 
            self.white.remove(i)
            self.white.append(j)
            if j in self.black : self.black.remove(j)
        else:
            self.black.remove(i)
            self.black.append(j)
            if j in self.white : self.white.remove(j)      
       
        self.board[j]=self.board[i]
        self.board[i]="o"
        self.kings_attacked = self.is_square_controlled(self.kings[0],False),self.is_square_controlled(self.kings[1],True)
          
    def get_moves(self,i):
        "zwraca dostępne ruchy dla figury z danego pola biorąc pod uwagę bezpieczeństwo króla. Turn informuje czyja jest tura. "
        turn = self.turn
        if i==-1: return []
        moves = self.get_moves_unsafeking(i,turn)
        for sq in moves[:]:
            gra = copy.deepcopy(self)
            gra.move_piece(i,sq)
            if self.turn : king_square = gra.kings[0]
            else : king_square=gra.kings[1]
            if  gra.is_square_controlled(king_square,not turn): moves.remove(sq)
        return moves













