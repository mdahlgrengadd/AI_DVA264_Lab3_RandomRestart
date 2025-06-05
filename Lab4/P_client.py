# client to Mancala server. Lab4, DVA340, MDU.
# For students: you only need to fill out function decide_move(boardIn, playerTurnIn)
# it currently selects a random available move.
# To test your client: start Mancala_server.pyc, then your program and one bot in that order (server first, then clients)

import socket
import numpy as np
import time
from multiprocessing.pool import ThreadPool
import os
from datetime import date


# def decide_move_rnd(boardIn, playerTurnIn):
#     #CHANGE THIS FILE TO CODE INTELLIGENCE IN YOUR CLIENT.
#     # PLAYERMOVE IS '1'..'6'
#     # BOARDIN CONSISTS OF 14 INTS. BOARDIN[0-5] ARE P1 HOLES, BOARDIN[6] IS P1 STORE
#     # BOARDIN[7-12] ARE P2 HOLES, BOARDIN[13] IS P2 STORE
#     moves = [
#         '1',
#         '2',
#         '3',
#         '4',
#         '5',
#         '6']
#     if playerTurnIn == 1:
#         options = np.array(boardIn[0:6])
#         options = np.where(options > 0)
#         options = options[0]
#         position = options[np.random.randint(len(options), size=1)]
#         playerMove = moves[position[0]]
#     elif playerTurnIn == 2:
#         options = np.array(boardIn[7:13])
#         options = np.where(options > 0)
#         options = options[0]
#         position = options[np.random.randint(len(options), size=1)]
#         playerMove = moves[position[0]]
#     return playerMove, "randommove"


def ACTIONS(board, playerTurn):
    """
    Returns list of valid actions (moves 1-6) for the current player
    An action is valid if the corresponding pit has stones > 0
    """
    valid_actions = []

    if playerTurn == 1:
        # Player 1: check pits 0-5 (indices 0-5)
        for i in range(6):
            if board[i] > 0:
                valid_actions.append(i + 1)  # Convert to move number (1-6)
    else:
        # Player 2: check pits 7-12 (indices 7-12)
        for i in range(7, 13):
            if board[i] > 0:
                valid_actions.append(i - 6)  # Convert to move number (1-6)

    return valid_actions


def TERMINAL_TEST(board):
    """
    Check if the game state is terminal
    Game ends when all pits on one side are empty
    """
    # Check if Player 1's side (indices 0-5) is empty
    player1_empty = all(board[i] == 0 for i in range(6))

    # Check if Player 2's side (indices 7-12) is empty
    player2_empty = all(board[i] == 0 for i in range(7, 13))

    return player1_empty or player2_empty


def RESULT(board, action, playerTurn):
    """
    Apply an action to the board and return the new board state and next player
    Uses the existing play() function to simulate the move
    """
    # Create a copy of the board to avoid modifying the original
    new_board = board.copy()

    # Apply the move using the existing play function
    result = play(playerTurn, action, new_board)

    if result is None:
        # Invalid move, return original state
        return new_board, playerTurn

    new_board, next_player = result
    return new_board, next_player


def UTILITY(board, original_player):
    """
    Evaluate the utility of a terminal state from the perspective of original_player
    Higher values are better for original_player
    """
    # In terminal state, add remaining stones to respective stores
    final_board = board.copy()

    # Add remaining Player 1 stones to Player 1's store
    p1_remaining = sum(final_board[0:6])
    final_board[6] += p1_remaining

    # Add remaining Player 2 stones to Player 2's store
    p2_remaining = sum(final_board[7:13])
    final_board[13] += p2_remaining

    # Calculate score difference from original player's perspective
    if original_player == 1:
        return final_board[6] - final_board[13]  # P1 store - P2 store
    else:
        return final_board[13] - final_board[6]  # P2 store - P1 store


def EVALUATE(board, original_player, depth):
    """
    Heuristic evaluation function for non-terminal states
    Combines multiple strategic factors
    """
    if TERMINAL_TEST(board):
        return UTILITY(board, original_player)

    # Basic score difference (stones in stores)
    if original_player == 1:
        score_diff = board[6] - board[13]
    else:
        score_diff = board[13] - board[6]

    # Stone count advantage (total stones on our side vs opponent)
    if original_player == 1:
        our_stones = sum(board[0:6])
        opp_stones = sum(board[7:13])
    else:
        our_stones = sum(board[7:13])
        opp_stones = sum(board[0:6])

    stone_advantage = our_stones - opp_stones

    # Combine factors with weights
    evaluation = (
        10 * score_diff +      # Store difference (most important)
        1 * stone_advantage   # Stone count advantage
    )

    return evaluation


def MAX_VALUE(board, original_player, current_player, depth, max_depth):
    """
    MAX algorithm implementation
    Returns the utility value for maximizing player
    """
    if TERMINAL_TEST(board) or depth >= max_depth:
        return EVALUATE(board, original_player, depth)

    v = float('-inf')
    actions = ACTIONS(board, current_player)

    for action in actions:
        new_board, next_player = RESULT(board, action, current_player)
        v = max(v, MIN_VALUE(new_board, original_player,
                next_player, depth + 1, max_depth))

    return v


def MIN_VALUE(board, original_player, current_player, depth, max_depth):
    """
    MIN algorithm implementation  
    Returns the utility value for minimizing player
    """
    if TERMINAL_TEST(board) or depth >= max_depth:
        return EVALUATE(board, original_player, depth)

    v = float('inf')
    actions = ACTIONS(board, current_player)

    for action in actions:
        new_board, next_player = RESULT(board, action, current_player)
        v = min(v, MAX_VALUE(new_board, original_player,
                next_player, depth + 1, max_depth))

    return v


def MINIMAX(board, playerTurn, max_depth=3):
    """
    Main Minimax function that returns the best action
    playerTurn is the maximizing player (our player)
    """
    best_action = None
    best_value = float('-inf')

    actions = ACTIONS(board, playerTurn)

    if not actions:
        return None  # No valid moves

    for action in actions:
        new_board, next_player = RESULT(board, action, playerTurn)

        # Get the minimax value for this action
        if next_player == playerTurn:
            # We get another turn (landed in our store)
            action_value = MAX_VALUE(
                new_board, playerTurn, next_player, 1, max_depth)
        else:
            # Opponent's turn
            action_value = MIN_VALUE(
                new_board, playerTurn, next_player, 1, max_depth)

        # Keep track of best action
        if action_value > best_value:
            best_value = action_value
            best_action = action

    return best_action


def decide_move(boardIn, playerTurnIn):
    """
    Main decision function - uses Minimax algorithm to choose best move
    """
    # Use Minimax to find the best move
    best_move = MINIMAX(boardIn, playerTurnIn, max_depth=3)

    if best_move is None:
        # Fallback to random if no move found (shouldn't happen)
        moves = ['1', '2', '3', '4', '5', '6']
        if playerTurnIn == 1:
            options = np.array(boardIn[0:6])
            options = np.where(options > 0)
            options = options[0]
            if len(options) > 0:
                position = options[np.random.randint(len(options), size=1)]
                playerMove = moves[position[0]]
            else:
                playerMove = '1'  # Default fallback
        elif playerTurnIn == 2:
            options = np.array(boardIn[7:13])
            options = np.where(options > 0)
            options = options[0]
            if len(options) > 0:
                position = options[np.random.randint(len(options), size=1)]
                playerMove = moves[position[0]]
            else:
                playerMove = '1'  # Default fallback
        return playerMove, "fallback_random"

    # Convert best_move to string format expected by server
    playerMove = str(best_move)
    return playerMove, "minimax_ai"


def play(playerTurn: int, playerMove: int, boardGame):
    # playerTurn ar 1 eller 2
    # playerMove ar 1..6
    # boardGame ar en 1x14 vektor
    if not correctPlay(playerMove, boardGame, playerTurn):
        print("Illegal move! break")
        return

    # Determine starting index based on playerTurn and playerMove
    idx = playerMove - 1 + (playerTurn-1)*7  # -1 for p1, +6 for p2
    # grab stones from hole
    numStones: int = boardGame[idx]
    boardGame[idx] = 0
    hand: int = numStones
    while hand > 0:
        # idx next hole
        idx = (idx + 1) % 14
        # Skip opponent's store
        if idx == 13 - 7*(playerTurn-1):  # 13 for p1, 6 for p2
            continue
        # add stone in hole,
        boardGame[idx] += 1
        hand -= 1

    # end in store? get another turn. otherwise other players turn
    nextTurn = 3 - playerTurn
    if idx == 6 + 7*(playerTurn-1):
        nextTurn = playerTurn

    # end on own empty hole? score stone and opposite hole
    if boardGame[idx] == 1 and idx in range((playerTurn-1)*7, 6+(playerTurn-1)*7):
        boardGame[idx] -= 1  # score stone in last hole
        boardGame[6+(playerTurn-1)*7] += 1  # and remove it from the hole
        # also score stones from opposite hole
        boardGame[6+(playerTurn-1)*7] += boardGame[12 - idx]
        boardGame[12 - idx] = 0  # and remove them from the hole
    return (boardGame, nextTurn)


def correctPlay(playerMove: int, board, playerTurn):
    correct = 0
    if playerMove in range(1, 7) and board[playerMove-1 + (playerTurn-1)*7] > 0:
        correct = 1
    return correct


def countScorePlayer1(boardGame):
    (p1s, p2s) = countPoints(boardGame)
    return int(p1s - p2s)


def countPoints(boardGame):
    return (boardGame[6], boardGame[13])


def receive(socket):
    msg = ''.encode()

    try:
        data = socket.recv(1024)
        msg += data
    except:
        pass

    return msg.decode()


def send(socket, msg):
    socket.sendall(msg.encode())


# LET THE MAIN BEGIN


startTime = date(2025, 6, 4)
playerName = 'Martin_Dahlgren'
host = '127.0.0.1'
port = 30000
s = socket.socket()
pool = ThreadPool(processes=1)
gameEnd = False
MAX_RESPONSE_TIME = 20
print('The player: ' + playerName + ' starts!')
s.connect((host, port))
print('The player: ' + playerName + ' connected!')
while not gameEnd:
    asyncRetult = pool.apply_async(receive, (s,))
    startTime = time.time()
    currentTime = 0
    received = 0
    data = []
    while received == 0 and currentTime < MAX_RESPONSE_TIME:
        time.sleep(0.01)
        if asyncRetult.ready():
            data = asyncRetult.get()
            received = 1
        currentTime = time.time() - startTime
    if received == 0:
        print('No response in ' + str(MAX_RESPONSE_TIME) + ' sec')
        gameEnd = 1
    if data == 'N':
        send(s, playerName)
    if data == 'E':
        gameEnd = 1
    if len(data) > 1:
        board = [0,            0,            0,            0,            0,            0,            0,
                 0,            0,            0,            0,            0,            0,            0]
        playerTurn = int(data[0])
        i = 0
        j = 1
        while i <= 13:
            board[i] = int(data[j]) * 10 + int(data[j + 1])
            i += 1
            j += 2
        (move, botname) = decide_move(board, playerTurn)
    #    print('sending ', move)
        send(s, move)


# wait = input('Press ENTER to close the program.')
