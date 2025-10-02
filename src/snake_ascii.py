import curses
import random
import time

# Game settings
HEIGHT = 20
WIDTH = 40
SNAKE_CHAR = '#'
FOOD_CHAR = '*'
EMPTY_CHAR = ' '

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    # max_y, max_x = stdscr.getmaxyx()
    # print(f'maxy = {max_y}, and max_x = {max_x}')

    # Initial snake and food
    snake = [(HEIGHT//2, WIDTH//2 + i) for i in range(3)]
    direction = (0, -1)  # moving left
    food = (random.randint(1, HEIGHT-2), random.randint(1, WIDTH-2))

    score = 0

    while True:
        stdscr.clear()
        # Draw border
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if y == 0 or y == HEIGHT-1 or x == 0 or x == WIDTH-1:
                    stdscr.addch(y, x, '#')
        # Draw food
        stdscr.addch(food[0], food[1], FOOD_CHAR)
        # Draw snake
        for y, x in snake:
            stdscr.addch(y, x, SNAKE_CHAR)
        stdscr.addstr(0, 2, f'Score: {score}')

        # Input
        key = stdscr.getch()
        if key in [curses.KEY_UP, 65]:
            if direction != (1, 0):
                direction = (-1, 0)
        elif key in [curses.KEY_DOWN, 66]:
            if direction != (-1, 0):
                direction = (1, 0)
        elif key in [curses.KEY_LEFT, 68]:
            if direction != (0, 1):
                direction = (0, -1)
        elif key in [curses.KEY_RIGHT, 67]:
            if direction != (0, -1):
                direction = (0, 1)
        elif key == ord('q'):
            break

        # Move snake
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        if (new_head in snake or
            new_head[0] == 0 or new_head[0] == HEIGHT-1 or
            new_head[1] == 0 or new_head[1] == WIDTH-1):
            stdscr.addstr(HEIGHT//2, WIDTH//2 - 5, "GAME OVER!")
            stdscr.refresh()
            time.sleep(2)
            break

        snake.insert(0, new_head)
        if new_head == food:
            score += 1
            while True:
                food = (random.randint(1, HEIGHT-2), random.randint(1, WIDTH-2))
                if food not in snake:
                    break
        else:
            snake.pop()

        stdscr.refresh()


if __name__ == "__main__":
    curses.wrapper(main)
