from hand_of_the_king import getvalidmoves
import math
import random


COLS = 6
ROWS = 6

def get_computer_move(board, cards, banners):
    #search the board for the piece we are moving aka the index with a value of 1
    #this will be the start- start will be a tuple of the two  indexes (i, j)
    
    return minimax(board, cards,banners)
    
    


def minimax(board,cards,banners):
    turn = 0
    
    # if the terminal condition is reached
    # the terminal condition means there are no more valid moves
    actions = getvalidmoves(board)
    random.shuffle(actions)
    if len(getvalidmoves(board)) == 1:
        return getvalidmoves(board)[0]
    best = actions[0]
    
    if turn == 0:
        value = maxvalue(board,cards,banners,turn, actions[0],)
    else:
        value = minvalue(board,cards,banners,turn, actions[0],)
    for action in actions[1:]:
        if turn == 0:
            v = maxvalue(board,cards,banners,turn,action,)
        else:
            v = minvalue(board,cards,banners,turn,action,)
        if v > value:
            best = action
            value = v
    return best



def minvalue(board,cards,banners,turn,action):
    state = board.copy()
    otherPlayer = 0
    if turn == 0:
        otherPlayer = 1
    
    new, color, pickedUp = simulate(state,action, turn,cards)
    

    #the heurisic is the number of banners collected and the chance to get another banner
    if cards[turn][color-2] >= cards[abs(1-turn)][color-2]:
        banners[turn][color-2] = 1
        banners[abs(1-turn)][color-2] = 0
    
    amount = pickedUp/ color
    utility = utility1(board,action, otherPlayer,cards,amount)

    heuris = 0 
    for i in banners[turn]:
        heuris += 1

    V = heuris + utility

 
    
    # check if we are in a terminal state
    if len(getvalidmoves(new)) == 0:
        return V
        
    value = math.inf

    for action in getvalidmoves(new):
       
        value = max(V,maxvalue(board,cards,banners,otherPlayer, action))

    return value
  


def maxvalue(board,cards,banners,turn,action):
    state = board.copy()
    otherPlayer = 0
    if turn == 0:
        otherPlayer = 1
    new, color, pickedUp= simulate(state,action, turn,cards)
    
    amount = pickedUp/ color
    #the heurisic is the number of banners collected and the chance to get another banner
    if cards[turn][color-2] >= cards[abs(1-turn)][color-2]:
        banners[turn][color-2] = 1
        banners[abs(1-turn)][color-2] = 0

    utility = utility1(board,action, otherPlayer,cards,amount)
    heuris = 0 
    for i in banners[turn]:
        heuris += 1

    V = heuris + utility

  
    
    # check if we are in a terminal state
    if len(getvalidmoves(new)) == 0:
        return V
        
    value = -math.inf
  
    for action in getvalidmoves(new):
        
        value = max(V,minvalue(board,cards,banners,otherPlayer, action))

    return value
  

# greatest chance to get a banner
def utility1(board,action, turn,cards, amount):

   
    cardChosen = action
   

    color = board[cardChosen]    #the index of this color is  the value of the color - 2
    indexColor = color -2
    value = 0
    otherPlayer = 0
    if turn == 0:
        otherPlayer = 1
    #is there even a possibility to get the banner???
    #if the other player has half or less than half there is a chance
    # there is a chance
    if cards[otherPlayer][indexColor] <= (color/2):
        value = 100 * amount
    #NO CHANCE
    else:
        value = 1

    return value
    


def simulate(board, move, turn,cards):
   
    pickedUp = 1
    
    x1 = board.index(1)  # index of the 1-card on the board
    # print(f'moving from {x1} to {x}')

    color = board[move]  # color of the main captured card
    
    board[move] = 1  # the 1-card moves here
 
    cards[turn][color - 2] += 1

    if abs(move - x1) < COLS:  # move is either left or right
      
        if move < x1:  # left
            possible = range(move + 1, x1)
        else:  # right
            possible = range(x1 + 1, move)
    else:  # move is either up or down
        
        if move < x1:  # up
            possible = range(move + COLS, x1, COLS)
        else:  # down
            possible = range(x1 + COLS, move, COLS)

    for i in possible:
        if board[i] == color:
            pickedUp +=1
            board[i] = 0  # there is no card in this position anymore
            cards[turn][color - 2] += 1

    # Move the 1-card to the correct position
    
    board[x1] = 0
    print(cards)
    #I want it to return the number of cards picked up and the board
    return board, pickedUp, color