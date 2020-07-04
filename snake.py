#!/Library/Frameworks/Python.framework/Versions/3.8/bin/python3

import random
import time
from pynput import keyboard

WIDTH = 48
HEIGHT = 25
SPEED = 0.2
SNAKE_SYMBOL = 'X'
FOOD_SYMBOL = 'O'
UP = 'UP'; DOWN = 'DOWN'; LEFT = 'LEFT'; RIGHT = 'RIGHT'
KEY_DICT = { 'w': UP, 's': DOWN, 'a': LEFT, 'd': RIGHT}
DIRS = [UP, DOWN, RIGHT, LEFT]

def on_press(key, snake):
    try:
        dir = KEY_DICT[key.char]
        snake.turn(dir)
    except (KeyError, Attribute):
        return False

def random_dir():
    return DIRS[random.randint(0, len(DIRS) - 1)]

def clear_screen():
    for i in range(50):
        print()

class Square:
    def __init__(self, **coordinates):
        x = coordinates.get('x', None)
        y = coordinates.get('y', None)
        if x == None:
            self.x = random.randint(0, WIDTH)
        else:
            self.x = x
        if y == None:
            self.y = random.randint(0, HEIGHT)
        else:
            self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Turn:
    def __init__(self, square, dir):
        self.square = square
        self.dir = dir
        self.age = 0

    def age_by_one(self): self.age += 1

class Snake:
    def __init__(self, dir, *segments):
        self.body = []
        for square in segments:
            self.body.append((square, dir))
        self.turns = []

    def head(self):
        head, _dir = self.body[0]
        return head

    def length(self):
        return len(self.body)

    def next_square(self):
        head, dir = self.body[0]
        x = head.x; y = head.y
        if dir == UP:
            y = head.y - 1
        elif dir == DOWN:
            y = head.y + 1
        elif dir == LEFT:
            x = head.x - 1
        elif dir == RIGHT:
            x = head.x + 1
        return Square(x=x, y=y)

    def shift_square(self, square, dir):
        if dir == UP:
            square.y -= 1
        elif dir == DOWN:
            square.y += 1
        elif dir == LEFT:
            square.x -= 1
        elif dir == RIGHT:
            square.x += 1

    def move(self):
        for segment in range(self.length()):
            square, dir = self.body[segment]
            turn_idx = 0
            while turn_idx < (len(self.turns)):
                turn = self.turns[turn_idx]
                if turn.age > self.length():
                    self.turns.remove(turn)
                else:
                    if turn.square == square:
                        dir = turn.dir
                        self.body[segment] = square, dir
                    turn_idx += 1
            self.shift_square(square, dir)
        for turn in self.turns:
            turn.age_by_one()


    def grow(self):
        tail, dir = self.body[-1]
        x = tail.x; y = tail.y
        self.move()
        square = Square(x=x, y=y)
        self.body.append((square, dir))

    def turn(self, dir):
        head = self.head()
        square = Square(x=head.x, y=head.y)
        self.turns.append(Turn(square, dir))
        self.body[0] = head, dir

class Game:
    def __init__(self, width, height, snake):
        grid = []
        for row in range(height):
            row = []
            for col in range(width):
                row.append(None)
            grid.append(row)
        self.grid = grid
        self.snake = snake
        self.width = width
        self.height = height
        self.gen_food()

    def gen_food(self):
        def already_occupied(square):
            occupied = False
            for (snake_square, _dir) in self.snake.body:
                if square == snake_square:
                    occupied = True
            return occupied
        gen_x = lambda x : random.randint(0, x - 3)
        gen_y = lambda y : random.randint(0, y - 1)
        x = gen_x(WIDTH); y = gen_y(HEIGHT)
        while already_occupied(Square(x=x, y=y)):
            x = gen_x(WIDTH); y = gen_y(HEIGHT)
        self.food = Square(x=x, y=y)

    def display(self):
        def print_border(symbol):
            line = ''
            for i in range(self.width):
                line += symbol
            print(line)
        print_border('_')
        for row in range(self.height):
            print('|', end='')
            for col in range(self.width - 2):
                empty = True
                if self.food.x == col and self.food.y == row:
                    print(FOOD_SYMBOL, end='')
                    empty = False
                else:
                    for square, dir in self.snake.body:
                        if square.x == col and square.y == row:
                            print(SNAKE_SYMBOL, end='')
                            empty = False
                if empty:
                    print(' ', end='')
            print('|')
        print_border('-')

if __name__ == '__main__':
    starting_dir = random_dir()
    snake = Snake(starting_dir, Square())
    game = Game(WIDTH, HEIGHT, snake)
    game.display()
    listener = keyboard.Listener(on_press=lambda key : on_press(key, snake))
    listener.start()
    while True:
        clear_screen()
        game.display()
        next_square = snake.next_square()
        if next_square == game.food:
            game.gen_food()
            snake.grow()
        else:
            snake.move()
        time.sleep(SPEED)
