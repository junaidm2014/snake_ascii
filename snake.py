#!/usr/bin/env python3
"""
A simple console-based Snake game using ASCII characters.
"""

import sys
import time
import random
import os

# Try to import getch for cross-platform keyboard input
try:
    import msvcrt
    def get_key():
        """Get key press on Windows."""
        if msvcrt.kbhit():
            return msvcrt.getch().decode('utf-8').upper()
        return None
except ImportError:
    import tty
    import termios
    import select
    
    def get_key():
        """Get key press on Unix-like systems."""
        dr, dw, de = select.select([sys.stdin], [], [], 0)
        if dr:
            return sys.stdin.read(1).upper()
        return None


class Snake:
    """Snake game class."""
    
    def __init__(self, width=40, height=20):
        """Initialize the snake game."""
        self.width = width
        self.height = height
        self.snake = [(height // 2, width // 2)]  # Start in the middle
        self.direction = (0, 1)  # Start moving right (row, col)
        self.food = self._generate_food()
        self.score = 0
        self.game_over = False
        
    def _generate_food(self):
        """Generate food at a random position not occupied by the snake."""
        while True:
            food = (random.randint(1, self.height - 2), 
                   random.randint(1, self.width - 2))
            if food not in self.snake:
                return food
    
    def update(self):
        """Update the game state."""
        if self.game_over:
            return
        
        # Calculate new head position
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        # Check for wall collision
        if (new_head[0] <= 0 or new_head[0] >= self.height - 1 or
            new_head[1] <= 0 or new_head[1] >= self.width - 1):
            self.game_over = True
            return
        
        # Check for self collision
        if new_head in self.snake:
            self.game_over = True
            return
        
        # Move snake
        self.snake.insert(0, new_head)
        
        # Check if food is eaten
        if new_head == self.food:
            self.score += 1
            self.food = self._generate_food()
        else:
            self.snake.pop()  # Remove tail if no food eaten
    
    def change_direction(self, new_direction):
        """Change the snake's direction."""
        # Prevent reversing direction
        if (new_direction[0] + self.direction[0] == 0 and
            new_direction[1] + self.direction[1] == 0):
            return
        self.direction = new_direction
    
    def render(self):
        """Render the game board."""
        # Clear screen
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Create game board
        board = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        
        # Draw borders
        for i in range(self.width):
            board[0][i] = '─'
            board[self.height - 1][i] = '─'
        for i in range(self.height):
            board[i][0] = '│'
            board[i][self.width - 1] = '│'
        board[0][0] = '┌'
        board[0][self.width - 1] = '┐'
        board[self.height - 1][0] = '└'
        board[self.height - 1][self.width - 1] = '┘'
        
        # Draw snake
        for i, segment in enumerate(self.snake):
            if i == 0:
                board[segment[0]][segment[1]] = '●'  # Head
            else:
                board[segment[0]][segment[1]] = '○'  # Body
        
        # Draw food
        board[self.food[0]][self.food[1]] = '★'
        
        # Print board
        for row in board:
            print(''.join(row))
        
        # Print score
        print(f"Score: {self.score}")
        print("Controls: W=Up, S=Down, A=Left, D=Right, Q=Quit")
        
        if self.game_over:
            print("\n*** GAME OVER ***")
            print(f"Final Score: {self.score}")


def main():
    """Main game loop."""
    # Set up terminal for non-blocking input on Unix
    if os.name != 'nt':
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setcbreak(sys.stdin.fileno())
            run_game()
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    else:
        run_game()


def run_game():
    """Run the game loop."""
    game = Snake(width=40, height=20)
    
    # Direction mapping
    direction_map = {
        'W': (-1, 0),  # Up
        'S': (1, 0),   # Down
        'A': (0, -1),  # Left
        'D': (0, 1)    # Right
    }
    
    game.render()
    
    while not game.game_over:
        # Get keyboard input
        key = get_key()
        
        if key == 'Q':
            print("\nThanks for playing!")
            return
        
        if key in direction_map:
            game.change_direction(direction_map[key])
        
        # Update game state
        game.update()
        game.render()
        
        # Control game speed
        time.sleep(0.15)
    
    # Game over - wait for any key
    print("\nPress any key to exit...")
    while get_key() is None:
        time.sleep(0.1)


if __name__ == "__main__":
    main()
