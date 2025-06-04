# Mancala AI Implementation

## Overview
This project implements an AI player for the ancient board game Mancala using the Minimax algorithm. The AI is designed to compete against various difficulty levels of bot opponents (P3, P4, and P5 bots) in a client-server architecture.

## Game Rules
Mancala is a two-player turn-based strategy game with the following rules:
- The board consists of two rows of six pits each, plus two stores (one per player)
- Each pit initially contains 4 stones
- Players take turns picking up all stones from one of their pits and distributing them counter-clockwise
- If the last stone lands in the player's store, they get another turn
- If the last stone lands in an empty pit on the player's side, they capture that stone plus all stones in the opposite pit
- The game ends when one side has no stones left
- The winner is the player with the most stones in their store

## Implementation Details

### Architecture
The implementation consists of two main client files:
- `P_client.py` - Uses score difference utility function
- `P_client_Classic_Score.py` - Uses win/loss/draw utility function

### Minimax Algorithm
The AI uses the Minimax algorithm with the following components:

#### Core Functions
1. **ACTIONS(board, playerTurn)** - Returns valid moves for the current player
2. **TERMINAL_TEST(board)** - Checks if the game has ended
3. **RESULT(board, action, playerTurn)** - Simulates a move and returns the new game state
4. **UTILITY(board, original_player)** - Evaluates terminal game states
5. **EVALUATE(board, original_player, depth)** - Heuristic evaluation for non-terminal states

#### Search Algorithm
- **MAX_VALUE/MIN_VALUE** - Implements the minimax search with alternating maximizing and minimizing players
- **MINIMAX** - Main function that returns the best move for the current player
- **Search Depth**: Configurable (default: 3 levels)

### Utility Functions

#### Version 1: Score Difference (P_client.py)
```python
def UTILITY(board, original_player):
    # Calculate score difference from original player's perspective
    if original_player == 1:
        return final_board[6] - final_board[13]  # P1 store - P2 store
    else:
        return final_board[13] - final_board[6]  # P2 store - P1 store
```
- Returns the actual point difference between players
- Allows the AI to prefer larger victories and smaller defeats
- Provides granular evaluation of game outcomes

#### Version 2: Win/Loss/Draw (P_client_Classic_Score.py)
```python
def UTILITY(board, original_player):
    # Returns: +1 (win), 0 (draw), -1 (loss)
    if original_player == 1:
        if p1_score > p2_score:
            return 1    # Win
        elif p1_score < p2_score:
            return -1   # Loss
        else:
            return 0    # Draw
```
- Returns discrete categorical outcomes
- Treats all wins equally regardless of margin
- Classical game theory approach

### Heuristic Evaluation
For non-terminal states, the AI uses a weighted combination of factors:

```python
def EVALUATE(board, original_player, depth):
    evaluation = (
        10 * score_diff +      # Store difference (most important)
        2 * stone_advantage +   # Stone count advantage  
        1 * mobility           # Move flexibility
    )
    return evaluation
```

**Factors considered:**
1. **Score Difference** (Weight: 10) - Stones in stores
2. **Stone Advantage** (Weight: 2) - Total stones on player's side vs opponent
3. **Mobility** (Weight: 1) - Number of available moves

### Game Simulation
The `play()` function accurately simulates Mancala moves:
- Handles stone distribution around the board
- Implements the "free turn" rule when landing in own store
- Implements the "capture" rule when landing in empty pit
- Skips opponent's store during distribution

## Usage

### Starting the Game
1. Start the Mancala server: `python Mancala_server.pyc`
2. Run your AI client: `python P_client.py`
3. Run a bot opponent (e.g., `python P3_bot.pyc`)

### Configuration
- **Player Name**: Set in the `playerName` variable
- **Search Depth**: Modify `max_depth` parameter in MINIMAX function
- **Server Settings**: Host and port configuration available in main section

### Performance Considerations
- **Time Limit**: 20 seconds per move
- **Search Depth**: Limited to prevent timeout
- **Memory**: Efficient board copying and state management

## Bot Opponents
- **P3_bot**: Beginner level (Grade 3 if defeated)
- **P4_bot**: Intermediate level (Grade 4 if defeated)  
- **P5_bot**: Advanced level (Grade 5 if defeated)

## Technical Details

### Communication Protocol
- Socket-based client-server communication
- Board state encoded as 28-character string
- Move responses as single digit ('1'-'6')

### Board Representation
- 14-element array: [P1_pits(6), P1_store(1), P2_pits(6), P2_store(1)]
- Indices 0-5: Player 1 pits
- Index 6: Player 1 store
- Indices 7-12: Player 2 pits
- Index 13: Player 2 store

### Error Handling
- Invalid move detection and prevention
- Timeout handling for server communication
- Fallback to random moves in edge cases

## Strategy Analysis
The AI employs several strategic principles:
1. **Immediate Scoring**: Prioritizes moves that gain points
2. **Future Planning**: Looks ahead multiple moves using minimax
3. **Defensive Play**: Considers opponent's potential responses
4. **Mobility Management**: Maintains move options
5. **Endgame Optimization**: Focuses on final stone collection

## Files Structure
```
Lab4/
├── P_client.py                 # Score difference version
├── P_client_Classic_Score.py   # Win/loss/draw version
├── Mancala_server.pyc         # Game server
├── P3_bot.pyc                 # Beginner bot
├── P4_bot.pyc                 # Intermediate bot
├── P5_bot.pyc                 # Advanced bot
├── launch_game.py             # Game launcher utility
└── assignment.md              # Assignment description
```

## Performance Optimization
- Efficient board state copying
- Pruning of invalid moves
- Depth-limited search to meet time constraints
- Optimized evaluation function computation

## Future Improvements
- Alpha-beta pruning for faster search
- Dynamic depth adjustment based on time remaining
- Opening book for early game moves
- Endgame tablebase for perfect play
- Machine learning-based evaluation function tuning
