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


def ACTIONS(board, playerTurn):
    possible_moves = []

    if playerTurn == 1:
        for i in range(6):
            if board[i] > 0:
                possible_moves.append(i + 1)  # Convert to move number (1-6)
    else:
        for i in range(7, 13):
            if board[i] > 0:
                possible_moves.append(i - 6)  # Convert to move number (1-6)

    return possible_moves


def TERMINAL_TEST(board):
    empty1 = sum(board[0:6]) == 0
    empty2 = sum(board[7:13]) == 0
    IS_GAME_OVER = empty1 or empty2
    return IS_GAME_OVER


def RESULT(board, action, playerTurn):
    board_copy = board.copy()

    result = play(playerTurn, action, board_copy)

    if result is None:
        return board_copy, playerTurn

    board_copy, next_player = result
    return board_copy, next_player


def UTILITY(board, actual_player):
    board_copy = board.copy()

    add_to_p1 = sum(board_copy[0:6])
    board_copy[6] += add_to_p1

    add_to_p2 = sum(board_copy[7:13])
    board_copy[13] += add_to_p2

    if actual_player == 1:
        return board_copy[6] - board_copy[13]
    else:
        return board_copy[13] - board_copy[6]


def UTIL_EVAL(board, actual_player, depth):
    if TERMINAL_TEST(board):
        return UTILITY(board, actual_player)

    if actual_player == 1:
        score_diff = board[6] - board[13]
    else:
        score_diff = board[13] - board[6]

    if actual_player == 1:
        player_nr_stones = sum(board[0:6])
        opponent_nr_stones = sum(board[7:13])
    else:
        player_nr_stones = sum(board[7:13])
        opponent_nr_stones = sum(board[0:6])

    stones_diff = player_nr_stones - opponent_nr_stones

    evaluation = (
        10 * score_diff +
        1 * stones_diff
    )

    return evaluation


# ---------------------------------------------------------------------------
# Minimax algorithm – core recursive routines
# Adapted from Lecture 7 “Adversarial Search (Multi-agent Decision Making)”
# slide set by Johan Hjorth in (Lecture_7.pptx)
# ---------------------------------------------------------------------------

# function MAX-VALUE(state)          # Returns a utility value
#     if TERMINAL-TEST(state) then
#         return UTILITY(state)
#     v ← −∞
#     for each a in ACTIONS(state) do
#         v ← MAX(v, MIN-VALUE(RESULT(state, a)))
#     return v

# function MIN-VALUE(state)          # Returns a utility value
#     if TERMINAL-TEST(state) then
#         return UTILITY(state)
#     v ← ∞
#     for each a in ACTIONS(state) do
#         v ← MIN(v, MAX-VALUE(RESULT(state, a)))
#     return v

def MAX_VALUE(state, original_player, current_player, depth, max_depth):
    if TERMINAL_TEST(state) or depth >= max_depth:
        return UTIL_EVAL(state, original_player, depth)

    v = float('-inf')
    actions = ACTIONS(state, current_player)

    for a in actions:
        new_state, next_player = RESULT(state, a, current_player)
        v = max(v, MIN_VALUE(new_state, original_player,
                next_player, depth + 1, max_depth))

    return v


def MIN_VALUE(state, original_player, current_player, depth, max_depth):
    if TERMINAL_TEST(state) or depth >= max_depth:
        return UTIL_EVAL(state, original_player, depth)

    v = float('inf')
    actions = ACTIONS(state, current_player)

    for a in actions:
        new_state, next_player = RESULT(state, a, current_player)
        v = min(v, MAX_VALUE(new_state, original_player,
                next_player, depth + 1, max_depth))

    return v


def MINIMAX(state, playerTurn, max_depth=3):
    best_action = None
    best_value = float('-inf')

    actions = ACTIONS(state, playerTurn)

    if not actions:
        return None

    for a in actions:
        new_state, next_player = RESULT(state, a, playerTurn)

        if next_player == playerTurn:
            action_value = MAX_VALUE(
                new_state, playerTurn, next_player, 1, max_depth)
        else:

            action_value = MIN_VALUE(
                new_state, playerTurn, next_player, 1, max_depth)

        if action_value > best_value:
            best_value = action_value
            best_action = a

    return best_action


def decide_move(boardIn, playerTurnIn):
    best_move = MINIMAX(boardIn, playerTurnIn, max_depth=3)
    playerMove = str(best_move)
    return playerMove, "minimax"


###################
# Rest is unchanged
###################

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
