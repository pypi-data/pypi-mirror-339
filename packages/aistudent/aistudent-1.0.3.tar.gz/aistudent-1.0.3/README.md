# AI Utilities Package

This package provides essential implementations of AI algorithms, making it easier for students to learn and experiment with **search algorithms, constraint satisfaction problems (CSP), and game-playing strategies**. It is based on the **AIMA-Python** project but has been modularized and simplified for educational use.

## Features
- **Search Algorithms**: Implements **uninformed** (BFS, DFS, UCS) and **informed** (Greedy, A*) search algorithms.
- **Constraint Satisfaction Problems (CSP)**: Includes **backtracking search, forward-checking, and heuristics** for CSPs.
- **Game Playing**: Implements **Minimax and Alpha-Beta pruning** for decision-making in two-player games.

## Installation  
To install this package, use:

```sh
pip install aistudent-1.0.0-non-any-py312.whl
```
## Dependencies
- numpy
- networkx
- sortedcontainers
- scipy
- matplotlib

### These dependencies will be installed automatically, but you can manually install them using:
```sh
pip install numpy networkx sortedcontainers scipy matplotlib
```
## Usage

Once installed, you can import and use the package in your Python scripts.


### Example 1: Using BFS from Search Module
```sh
from aistudent.aiutils.search import breadth_first_graph_search, EightPuzzle
initial_state = (1, 2, 3, 4, 0, 5, 6, 7, 8)
puzzle_problem = EightPuzzle(initial_state)
solution = breadth_first_graph_search(puzzle_problem)
for node in solution.path():
    print("Move:", node.action) 
    print("State:", node.state)

```

### Example 2: Solving a CSP Problem
```sh
from aistudent.aiutils.csp import CSP, backtracking_search
variables = ["A", "B", "C", "D"]
domains = {var: ["Red", "Green", "Blue"] for var in variables}
neighbors = {
    "A": ["B", "C"],
    "B": ["A", "C", "D"],
    "C": ["A", "B", "D"],
    "D": ["B", "C"]
}

def constraint(var1, value1, var2, value2):
    return value1 != value2

graph_coloring = CSP(variables, domains, neighbors, constraint)
solution = backtracking_search(graph_coloring)
print("Graph Coloring Solution:", solution)
```

### Example 3: Minimax Algorithm for Game AI
```sh

from aistudent.aiutils.games import TicTacToe, GameState, minmax_decision
game = TicTacToe()
board_state = {
    (1, 1): 'X', (1, 2): 'O', (1, 3): 'O',
    (2, 2): 'O',
    (3, 2): 'X', (3, 3): 'X'
}
all_positions = {(r, c) for r in range(1, 4) for c in range(1, 4)}
occupied_positions = set(board_state.keys())
available_moves = list(all_positions - occupied_positions)
initial_state = GameState(
    to_move='X',  # X's turn to play
    utility=0,  # No immediate win/loss
    board=board_state,  # Given board configuration
    moves=available_moves  # Possible moves for X
)
print("The initial board for Tic-Tac-Toe is:")
game.display(initial_state)
# Use the Minimax algorithm to determine the best move for X
best_move = minmax_decision(game=game, state=initial_state)
# Apply the best move to get the next board state
next_state = game.result(initial_state, best_move)
# Display the chosen best move
print("\nBest move for X:", best_move)
# Display the board after X's move
print("\nBoard after X's move:")
game.display(next_state)
```
### Example 4: A* Algorithm
```sh
from aistudent.aiutils.search import astar_search, EightPuzzle
initial_state = (1, 2, 3, 4, 0, 5, 6, 7, 8)
puzzle_problem = EightPuzzle(initial_state)
solution = astar_search(puzzle_problem)
for node in solution.path():
    print("Move:", node.action) 
    print("State:", node.state)

```

### Example 5: DFS Example
```sh
from aistudent.aiutils.search import depth_first_graph_search
from collections import deque

class PacmanGame:
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.start = None
        self.goal = None
        # Find Pac-Man (P) and Apple (A) positions
        for r in range(self.rows):
            for c in range(self.cols):
                if grid[r][c] == 'P':
                    self.start = (r, c)
                elif grid[r][c] == 'A':
                    self.goal = (r, c)
        # Set initial state for search
        self.initial = self.start  
    def actions(self, state):
        """ Returns valid moves: (Up, Down, Left, Right) """
        r, c = state
        possible_moves = [
            (r-1, c), (r+1, c), (r, c-1), (r, c+1)
        ]
        return [move for move in possible_moves if self.is_valid(move)]
    def is_valid(self, state):
        """ Check if a move is within bounds and not a wall """
        r, c = state
        return 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] != 'X'
    def result(self, state, action):
        """ Moving Pac-Man to new state """
        return action
    def goal_test(self, state):
        """ Check if Pac-Man found the Apple """
        return state == self.goal
    def path_cost(self, c, state1, action, state2):
        """ Returns cost of the path (default = 1 per move) """
        return c + 1  

grid = [
    ['P', '.', '.', 'X', 'A'],
    ['.', 'X', '.', '.', '.'],
    ['.', '.', 'X', '.', '.'],
    ['X', '.', '.', '.', '.']
]
pacman = PacmanGame(grid)
solution = depth_first_graph_search(pacman)
if solution:
    print("Solution found! Path to Apple:")
    for step in solution.path():
        print(step.state)
else:
    print("No solution found!")
```
## Credits & Contributions
This package is based on the AIMA-Python implementations by Stuart Russell & Peter Norvig, originally developed as part of Artificial Intelligence: A Modern Approach.

Original Implementation: AIMA-Python Contributors

Refactored & Simplified for Students: [Babar Ahmad]

Package Creation & Modularization: [Babar Ahmad]

This package is designed to simplify AI learning for students by providing easy-to-use, modular AI implementations.

