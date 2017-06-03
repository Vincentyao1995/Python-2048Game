# -*-coding:utf-8-*-  
#import curses
import  msvcrt
from random import randrange, choice
from collections import defaultdict
actions = ['Up','Left','Down','Right','Restart','Exit']
letterCodes = [ord(ch) for ch in 'WASDRQwasdrq']
actionsDict = dict(zip(letterCodes,actions*2))
#Def mat operations, transpose() return transposing matrix, while invert() return its reverse index matrix [(5,2),(1,3)]--[(2,5),(3,1)] this operation could save great efforts. And if we want move right, we could moveLeft(invert(mat))
#input a mat, which is field.
def getUserAction():
        char = 'None'
        while char not in actionsDict:
            char = ord(msvcrt.getch())
        return actionsDict[char]
def transpose(field):
        return [list(row) for row in zip(*field)]
def invert(field):
        return [row[::-1] for row in field]
# Current chessBoard class. All judging operations are wrote here. 
class GameField(object):
    def __init__(self,height=4,width=4, win=2048):
        self.height = height
        self.width = width
        self.winValue = win
        self.score = 0
        self.highscore = 0
        self.reset()
	#Create a new field
    def spawn(self):
        newElement = 4 if randrange(100) > 89 else 2 
        (i,j) = choice([(i,j) for i in range(self.width) for j in range(self.height)
                        if self.field[i][j] == 0])# : choice 函数
        self.field[i][j] = newElement
	#Reset the gameField
    def reset(self):
        if self.score > self.highscore:
            self.highscore = self.score
        self.score = 0
        self.field = [[0 for i in range(self.width)] for j in range(self.height)]
        self.spawn()
        self.spawn()
	#Through tighten, merge, tighten, we got operated field.
	#other movement could be realized by input transposd and inverted field. This is defined in this function too, see the def of dict var.
    def move(self, direction):
        #def moveRowLeft(row):
        def moveRowLeft(row):
            def tighten(row):
                newRow = [i for i in row if i != 0]
                newRow += [0 for i in range(len(row) - len(newRow))]
                return newRow
            def merge(row):
                pair = False
                newRow = []
                for i in range(len(row)):
                    if pair:
                        newRow.append(2 * row[i])
                        self.score += 2 * row[i]
                        pair = False
                    else:
                        if i + 1 < len(row) and row[i] == row[i + 1]:
                            pair = True 
                            newRow.append(0)
                        else:
                            newRow.append(row[i])
                assert len(newRow) == len(row)
                return newRow
            return tighten(merge(tighten(row)))
		# this dict defined moving operations, through indexing this dict we got what we should do.
        moves = {}
        moves['Left'] = lambda field : [moveRowLeft(row) for row in field]
        moves['Right'] = lambda field : invert(moves['Left'](invert(field))) # 
        moves['Up'] = lambda field : transpose(moves['Left'](transpose(field)))
        moves['Down'] = lambda field : transpose(moves['Right'](transpose(field)))
		# moving operation 
        if direction in moves:
            if self.moveIsPossible(direction):
                self.field = moves[direction](self.field)
                self.spawn()
                return True
            else:
                return False
    def isWin(self):
        return any(any(i >= self.winValue for i in row) for row in self.field)
    def isGameover(self):
        return not any(self.moveIsPossible(move) for move in actions)
    def moveIsPossible(self,direction):
        def rowIsLeftMovable(row):
            def change(i):
                if row[i] == 0 and row[i + 1] != 0:
                    return True
                if row[i] != 0 and row[i + 1] == row[i]:
                    return True
            return any(change(a) for a in range(len(row) - 1))
        check = {}
        # : lambda的语法结合transpose、invert两个操作函数实现了极大的精简。
        check['Left'] = lambda field : any(rowIsLeftMovable(row) for row in field)#循环应该是没进去，error
        check['Right'] = lambda field : check['Left'](invert(field))
        check['Up'] = lambda field : check['Left'](transpose(field))
        check['Down'] = lambda field : check['Right'](transpose(field))
        if direction in check:
            return check[direction](self.field)
        else:
            return False
    def draw(self):
        helpString1 = '(W)Up (S)Down (A)Left (D)Right'
        helpString2 = '     (R)Restart (Q)Exit'
        gameoverString = '           GAME OVER'
        winString = '          YOU WIN!'
        def cast(string):
            print(string + '\n')
        def drawHorSeparator():
            line = '+' + ('+------' * self.width + '+')[1:]
            separator = defaultdict(lambda: line)
            if not hasattr(drawHorSeparator,"counter"):
                drawHorSeparator.counter = 0
            cast(separator[drawHorSeparator.counter])
            drawHorSeparator.counter +=1
        def drawRow(row):
            cast(''.join('|{: ^5} '.format(num) if num > 0 else '|      ' for num in row) + '|')
        import os
        os.system('cls')
        cast('SCORE: ' + str(self.score))
        if 0 != self.highscore:
            cast('HIGHSCORE: ',str(self.highscore))
        for row in self.field:
            drawHorSeparator()
            drawRow(row)
        drawHorSeparator()

        if self.isWin():
            cast(winString)
        else:
            if self.isGameover():
                cast(gameoverString)
            else:
                cast(helpString1)
            cast(helpString2)
if __name__ == '__main__':
    def init():
        #重置棋盘
        game_field.reset()
        return 'Game'
    def notGame(state):
        #画出Gameover or win界面
        game_field.draw()# : game_field 的制定类型、以及stdscr、以及

        #读取用户输入的action，判断重启or结束游戏
        action = getUserAction()
        responses = defaultdict(lambda: state)#默认是当前状态，没有行为就会一直在当前界面循环；这句没懂 
        responses['Restart'],responses['Exit']= 'Init','Exit'
        return responses[action]#此action为用户输入的action
    def game():
        #画出棋盘的当前状态
        game_field.draw()
        #读取用户输入得到的action
        action = getUserAction()
        if action == 'Restart':
            return 'Init'
        if action == 'Exit':
            return 'Exit'
        if game_field.move(action):
            if game_field.isWin():
                return 'Win'
            if game_field.isGameover():
                return 'Gameover'
        return 'Game'
    stateActions = {
        'Init': init, # : not init()
        'Win':lambda:notGame('Win'),
        'Gameover':lambda:notGame('Gameover'),
        'Game':game
        }

    #curses,use_default_colors()
    game_field = GameField(win = 2048)

    state = 'Init'
    #循环状态机
    while state != 'Exit':
        state = stateActions[state]()

#curses.wrapper(main)
    
    


    






