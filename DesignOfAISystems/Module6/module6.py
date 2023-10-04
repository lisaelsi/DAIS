import math
import random as rand
import time
import random

def print_board(board):
    print('  a b c')
    j = 1
    for i in range(0, len(board), 3):
        print(j, *board[i:i+3], sep=' ')
        j += 1


def transform_input(input):
    switcher = {
        'a1': 0,
        'a2': 3,
        'a3': 6,
        'b1': 1,
        'b2': 4,
        'b3': 7,
        'c1': 2,
        'c2': 5,
        'c3': 8
    }
    
    return switcher.get(input)
    
def has_won(board):
    
    for i in range(0, len(board), 3):
        row = board[i:i+3]
        if len(set(row)) == 1 and '.' not in set(row):
            return True
        
    for i in range(0, 3):
        column = board[i::3]
        if len(set(column)) == 1 and '.' not in set(column):
            return True
    
    diag1 = list(board[0] + board[4] + board[8])
    diag2 = list(board[2] + board[4] + board[6])
    if len(set(diag1)) == 1 and '.' not in set(diag1) or len(set(diag2)) == 1 and '.' not in set(diag2):
        return True    
    
    return False

def get_possible_moves(current_board, current_player):
    possible_moves = []

    for i in range(len(current_board)):
        if current_board[i] == '.':
            possible_board = current_board.copy()
            possible_board[i] = current_player
            possible_moves.append(possible_board)
            
    return possible_moves
    
def get_user_move(board):
    move = input('Enter your move (or type exit to quit game): ')
    if move == 'exit':
        exit()

    if move not in ['a1', 'a2', 'a3', 'b1', 'b2', 'b3', 'c1', 'c2', 'c3']:
        print('Not a valid move')
        get_user_move(board)

    if board[transform_input(move)] == '.':
        board[transform_input(move)] = player

    else:
        print('Not a valid move')
        get_user_move(board)

def uct(node):
    node_visits = node.n_visits
    exploration_factor = math.sqrt(2)
    exploitation_score = 0
    exploration_score = 0
    best_node = None
    best_score = -math.inf
    for child_node in node.children:
        if child_node.n_visits == 0:
            exploration_score = math.inf
            return child_node
        else:
            exploitation_score = child_node.total_reward / child_node.n_visits
            exploration_score = exploration_factor * math.sqrt(math.log(node_visits) / child_node.n_visits)
        uct_score = exploitation_score + exploration_score
        if uct_score > best_score:
            best_node = child_node
            best_score = uct_score
    
    return best_node

def simulate(node):
    sim_board = node.board.copy()

    while not has_won(sim_board):
        possible_moves = get_possible_moves(sim_board, node.current_player)
        if not possible_moves:
            break
        sim_board = rand.choice(possible_moves)
        node.current_player = get_opponent(node.current_player)    
        
    if has_won(sim_board):
        if node.current_player == computer:
            return -1
        else:
            return 1
    else:
        return 0

def expand(node):
    possible_moves = get_possible_moves(node.board, node.current_player)
    for move in possible_moves:
        child_node = Node(move, get_opponent(node.current_player), node)
        node.children.append(child_node)
    
def backpropagate(node, reward):
    node.n_visits += 1
    node.total_reward += reward
    if node.parent:
        backpropagate(node.parent, reward)

class Node:
    def __init__(self, board, current_player, parent):
        self.board = board
        self.current_player = current_player
        self.children = []
        self.parent = parent
        self.n_visits = 0
        self.total_reward = 0
    
    def select(self):
        node = self
        while(len(node.children) != 0):
            node = uct(node)
        return node

def get_opponent(player):
    return 'X' if player == 'O' else 'O'

def get_winner_node(node):
    best_node = None
    best_score = -math.inf
    for child_node in node.children:

        if child_node.n_visits > best_score:
            best_node = child_node
            best_score = child_node.n_visits
        
    return best_node

def get_computer_move(board, current_player):
    n_simulations = 1000
    root_node = Node(board, current_player, parent=None)

    for i in range(n_simulations):
        node = root_node.select()

        if not has_won(node.board):
            expand(node)
        
        node_to_explore = node
        if node_to_explore.children:
            node_to_explore = random.choice(node_to_explore.children)
        
        reward = simulate(node)
        backpropagate(node_to_explore, reward)

    best_node = get_winner_node(root_node)

    return best_node.board

def is_tie(board):
    if '.' not in board:
        return True
    return False

def game(board, current_player):
    while not has_won(board):
        print_board(board)
        print('\n')

        if current_player == player:
            get_user_move(board)
        
        else: 
            time.sleep(0.8)
            print('Computers move')
            board = get_computer_move(board, computer)
    
        current_player = get_opponent(current_player)

        if is_tie(board):
            print_board(board)
            print('\n GAME IS TIED')
            print_board(board)
            exit()
    
    print_board(board)

board = ['.', '.', '.', '.', '.', '.', '.', '.', '.']

computer = 'O'
player = 'X'

players = [computer, player]

game(board, computer)


