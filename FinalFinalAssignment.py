# Amanda Souriyamath
# 11/29/2018
# Final Assignment 


from tkinter import * 

# initializing window properties
DIAMETER = 75
FOOTER = 25


initialColor = "white"

class Board:
    
    def __init__(self, col, row, window):  
        self.row = row
        self.col = col
        self.data = []     
        
        for r in range(self.row):
            boardRow = []
            for c in range(self.col):
                boardRow += [' ']
            self.data += [boardRow]              
            
    
        self.gameOver = False                  
        self.window = window
        self.frame = Frame(window)
        self.frame.pack()
        
        height = (DIAMETER*row)+50
        self.draw = Canvas(window, width=((DIAMETER)*col), height=((DIAMETER)*row)+50,bg="yellow", highlightbackground="black", highlightthickness=5)
        # Mouse input
        self.draw.bind("<Button-1>", self.mouse)
        self.draw.pack()                

        
        # Buttons
        self.qButton = Button(self.frame, text="QUIT", fg="red", command=self.quitGame)
        self.qButton.pack(side=RIGHT)          
        self.cButton = Button(self.frame, text="NEW GAME", fg="black", command=self.clear)
        self.cButton.pack(side=RIGHT)    
        
        
        self.circles = []
        self.colors = []
        # creating our GUI board
        
        y = 0
        for r in range(row):
            x = 0
            circleRow = []
            colorRow = []
            for c in range(col):
                circleRow += [self.draw.create_oval(x+5, y+5, x+DIAMETER, y+DIAMETER, fill=initialColor)]
                colorRow += [initialColor]
                x += DIAMETER
            self.circles += [circleRow]
            self.colors += [colorRow]
            y += DIAMETER
    
        # text
        self.message = self.draw.create_text(FOOTER,height-FOOTER,text="CONNECT FOUR GAME: Choose Your Move!", font="Arial 15", anchor="w")    
        
        
    def quitGame(self):
        self.window.destroy()
            
    def playGUI(self,aiPlayer):
        self.aiPlayer = aiPlayer        
            
        
    def mouse(self, event):    
        if self.gameOver:
            return
            
        xo = 'X'
        x = int(event.x/DIAMETER)     
        y = self.addMove(x, xo)
        self.draw.itemconfig(self.circles[y][x], fill="red")
            
        # Prompt
        myMessage = "Choose Your Next Move!"
        self.draw.itemconfig(self.message, text=myMessage) # Modifies the previous message to new message
            
        # Check WinsFor Player
        if self.winsFor('X'):
            myMessage = "Congrats!! You Won!"
            self.draw.itemconfig(self.message, text=myMessage) # Modifies the previous message to new message
            self.gameOver = True
            return
                
        # AiPlayer Move
        xo = 'O'
        x = self.aiPlayer.nextMove(self)
        y = self.addMove(x,xo)
        self.draw.itemconfig(self.circles[y][x], fill="black")
            
        # Check WinsFor AiPlayer
        if self.winsFor('O'):
            myMessage = "AI Player won..."
            self.draw.itemconfig(self.message, text=myMessage) # Modifies the previous message to new message            
            self.gameOver = True        
                
        # Check for full board or a tie.    
        if self.isFull():
            myMessage = "Game was a tie!!!"
            self.draw.itemconfig(self.message, text=myMessage)
            self.gameOver = True
            return
            
        
    def addMove(self,col,ox):
        """
        Allows player to add move
        """
        if self.allowsMove(col):
            for r in range(self.row):
                if self.data[r][col] != ' ':
                    self.data[r-1][col] = ox
                    return r-1
            self.data[self.row-1][col] = ox
            return self.row-1
        
    def allowsMove(self, col):
        """
        Checks to see if player inputs valid move
        """
        if 0 <= col < self.col:
            return self.data[0][col] == ' '
        else:
            return False     
            
    
    def clear(self):
        """
        clears the board
        """
        self.gameOver = False
        
        for r in range(self.row):
            for c in range(self.col):
                self.data[r][c] = ' '
        self.circles = []
        self.colors = []
        # creating our GUI board
        y = 0
        for r in range(self.row):
            x = 0
            circleRow = []
            colorRow = []
            for c in range(self.col):
                circleRow += [self.draw.create_oval(x+5, y+5, x+DIAMETER, y+DIAMETER, fill=initialColor)]
                colorRow += [initialColor]
                x += DIAMETER
            self.circles += [circleRow]
            self.colors += [colorRow]
            y += DIAMETER
                
        myMessage = "CONNECT FOUR GAME: Choose your move!!"
        self.draw.itemconfig(self.message, text=myMessage)
           
                    
    def delMove(self, c):
        for r in range(self.row):
            if self.data[r][c] != ' ':
                self.data[r][c] = ' '
                return
        
        
    def isFull(self):
        """
        Checks to see if the board is full
        """
        for r in range(self.row):
            for c in range(self.col):
                if self.data[r][c] == ' ':
                    return False
        else:
            return True
            
            
    def winsFor(self, ox):
        """
        Checks for wins
        """
        # checks horizontal wins
        for r in range(0, self.row):
            for c in range(0, self.col-3):
                if self.data[r][c] == ox and self.data[r][c+1] == ox and self.data[r][c+2] == ox and self.data[r][c+3] == ox:
                    return True
        # checks vertical wins
        for r in range(0, self.row-3):
            for c in range(0, self.col):
                if self.data[r][c] == ox and self.data[r+1][c] == ox and self.data[r+2][c] == ox and self.data[r+3][c] == ox:
                    return True
        # checks diagonal wins from top to bottom
        for r in range(0, self.row-3):
            for c in range(0, self.col-3):        
                if self.data[r][c] == ox and self.data[r+1][c+1] == ox and self.data[r+2][c+2] == ox and self.data[r+3][c+3] == ox:
                    return True
        # checks diagonal wins from bottom to top
        for r in range(3, self.row):
            for c in range(0, self.col-3):
                if self.data[r][c] == ox and self.data[r-1][c+1] == ox and self.data[r-2][c+2] == ox and self.data[r-3][c+3] == ox:
                    return True     
    
                    
class Player:
    
    def __init__(self, ox, tbt, ply):
        """
        Main container to store class attributes 
        """
        self.ox = 'O'
        self.tbt = 'RANDOM'
        self.ply = 4
        
    def up(self, ply):
        if ply >= 5:
            ply = 5
        else:
            ply = ply + 1
            
    def down(self, ply):
        if ply <= 0:
            ply = 1
        else:
            ply = ply - 1
        
    def nextMove(self, board):
        """
        returns an integer with its desired move
        """
        
        r = self.scoresFor(board, self.ox, self.ply)
            
        best = max(r)
        for c in range(board.col):
            if r[c] == best:
                return c
    
    
    def scoresFor(self, board, ox, ply):
        """
        returns a list of scores, 
        one for each column you can choose to move next
        """
        score = []
        for col in range(board.col):
            if board.allowsMove(col) == True:
                board.addMove(col, ox)
                if board.winsFor(ox) == True:
                    score += [100]
                elif ply == 1:
                    score += [50]
                else:
                    if ox == 'X':
                        Opponent = 'O'
                    else:
                        Opponent = 'X'
                    t = self.scoresFor(board, Opponent, ply-1)
                    score += [100 - max(t)]
                board.delMove(col)
            else:
                score += [-1]
        return score
    

root = Tk()
root.title("Connect 4")
b = Board(7, 6, root)
#Calling our aiPlayer as our player class:
aiPlayer = Player('O', 'Random', 4)
b.playGUI(aiPlayer)
root.mainloop()    