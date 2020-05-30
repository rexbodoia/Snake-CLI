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

class Turn:
    def __init__(self, square, dir):
        self.square = square
        self.dir = dir
        self.age = 0

    def age_by_one(self): self.age += 1

class Snake:
    def head(self):
        head, dir = self.body[0]
        return head

    def tail(self):
        tail, dir = self.body[-1]
        return tail

    def __init__(self, dir, *segments):
        self.body = []
        for segment in segments:
            self.body.append((segment, dir))
        self.turns = [Turn(self.head(), dir)]

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
        return Square(x=x, y=y)

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
        length = len(self.body)
        for segment in range(length):
            square, dir = self.body[segment]
            for turn_idx in range(len(self.turns)):
                turn = self.turns[turn_idx]
                if turn.age > length:
                    self.turns.pop(turn_idx)
                elif turn.square == square:
                    dir = turn.dir
                    self.body[segment] = square, dir
                turn.age_by_one()
                print('turn_square:', turn.square.x, turn.square.y, turn.dir, turn.age)
                print('segment:', square.x, square.y, dir)
            self.shift_square(square, dir)

    def turn(self, dir):
        head = self.head()
        self.turns.append(Turn(head, dir))
        self.body[0] = head, dir

    def grow(self):
        tail, dir = self.body[-1]
        self.move()
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
        self.food = Square(x=x, y=y)

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
        except (KeyError, AttributeError):
            global is_interrupted
            is_interrupted = True
            return False
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    while not is_interrupted:
        clear_screen()
        game.display()
        if snake.next_square() == game.food:
            game.gen_food()
            snake.grow()
        else:
            snake.move()
        time.sleep(SPEED)
    clear_screen()
    game.display()
    listener.join()
