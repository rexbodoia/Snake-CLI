#!/Library/Frameworks/Python.framework/Versions/3.8/bin/python3
import time
import random
from pynput import keyboard

WIDTH = 65
HEIGHT = 25
SPEED = 0.15
SNAKE_SYMBOL = 'X'
FOOD_SYMBOL = 'O'
KEY_DICT = {'w': 'UP', 's': 'DOWN', 'a': 'LEFT', 'd': 'RIGHT'}

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

class Snake:
    def __init__(self, dir, *body):
        self.body = []
        for segment in body:
            self.body.append((segment, dir))
        self.turns = [(body[0], dir)]

    def next_square(self):
        head, dir = self.body[0]
        x = head.x
        y = head.y
        if dir == 'UP':
            y = head.y - 1
        elif dir == 'DOWN':
            y = head.y + 1
        elif dir == 'LEFT':
            x = head.x - 1
        elif dir == 'RIGHT':
            x = head.x + 1
        return Square(x = x, y = y)

    def shift_square(self, square, dir):
        if dir == 'UP':
            square.y -= 1
        elif dir == 'DOWN':
            square.y += 1
        elif dir == 'LEFT':
            square.x -= 1
        elif dir == 'RIGHT':
            square.x += 1

    def move(self):
        for segment in range(len(self.body)):
            square, dir = self.body[segment]
            for (turn_square, turn_dir) in self.turns:
                if turn_square == square:
                    dir = turn_dir
                    self.body[segment] = square, dir
            self.shift_square(square, dir)

    def turn(self, dir):
        head, old_dir = self.body[0]
        self.turns.append((head, dir))
        self.body[0] = head, dir

    def grow(self):
        tail, dir = self.body[-1]
        square = Square(x = tail.x, y = tail.y)
        self.body.append((square, dir))

class Game:
    def gen_food(self):
        def already_occupied(x, y):
            already_occupied = False
            for (square, _dir) in self.snake.body:
                if x == square.x and y == square.y:
                    already_occupied = True
            return already_occupied
        gen_x = lambda x : random.randint(1, x - 2)
        gen_y = lambda y : random.randint(1, y - 2)
        x = gen_x(WIDTH)
        y = gen_y(HEIGHT)
        while already_occupied(x, y):
            x = gen_x(WIDTH)
            y = gen_y(HEIGHT)
        self.food = Square(x = x, y = y)

    def __init__(self, width, height, snake):
        grid = []
        for row in range(height):
            row = []
            for col in range(width):
                row.append(None)
            grid.append(row)
        self.grid = grid
        self.snake = snake
        self.gen_food()

    def display(self):
        def print_border(symbol):
            line = ''
            for i in range(WIDTH):
                line += symbol
            print(line)
        print_border('_')
        for row in range(len(self.grid)):
            print('|', end='')
            for col in range(len(self.grid[row]) - 2):
                empty = True
                if self.food.x == col and self.food.y == row:
                    empty = False
                    print(FOOD_SYMBOL, end='')
                else:
                    for (segment, _dir) in self.snake.body:
                        if segment.x == col and segment.y == row:
                            empty = False
                            print(SNAKE_SYMBOL, end='')
                if empty:
                    print(' ', end='')
            print('|')
        print_border('-')

def clear_screen():
    for i in range(100):
        print()

def random_dir():
    dirs = list(KEY_DICT.values())
    i = random.randint(0, len(dirs) - 1)
    return dirs[i]

if __name__ == '__main__':
    starting_dir = random_dir()
    snake = Snake(starting_dir, Square())
    game = Game(WIDTH, HEIGHT, snake)
    is_interrupted = False

    def on_press(key):
        try:
            dir = KEY_DICT[key.char]
            snake.turn(dir)
        except KeyError or AttributeError:
            global is_interrupted
            is_interrupted = True
            return False
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    while not is_interrupted:
        print(is_interrupted)
        clear_screen()
        game.display()
        if snake.next_square() == game.food:
            game.gen_food()
            snake.grow()
        snake.move()
        time.sleep(SPEED)
    clear_screen()
    game.display()
    listener.join()
