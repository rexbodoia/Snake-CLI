#!/Library/Frameworks/Python.framework/Versions/3.8/bin/python3
import time
import random
from pynput import keyboard

WIDTH = 65
HEIGHT = 25
# SPEED = 0.15
SPEED = 0.5
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

class Food:
    def __init__(self, snake):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.square = Square(x = self.x, y = self.y)
        def already_occupied(x, y):
            already_occupied = False
            for square in snake.body:
                if x == square.x and y == square.y:
                    already_occupied = True
            return already_occupied
        while already_occupied(self.x, self.y):
            self.x = random.randint(0, WIDTH)
            self.y = random.randint(0, HEIGHT)
            self.square = Square(self.x, self.y)

class Snake:
    def __init__(self, dir, *body):
        self.body = list(body)
        self.turns = [(body[0], dir)]

    def next_square(self, dir):
        x = self.body[0].x
        y = self.body[0].y
        if dir == 'UP':
            y = self.body[0].y - 1
        elif dir == 'DOWN':
            y = self.body[0].y + 1
        elif dir == 'LEFT':
            x = self.body[0].x - 1
        elif dir == 'RIGHT':
            x = self.body[0].x + 1
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

    def move(self, dir):
        for square in self.body:
            found_turn = False
            for (turn_square, turn_dir) in self.turns:
                print(turn_square.x, turn_square.y, turn_dir)
                if turn_square == square:
                    found_turn = True
                    self.shift_square(square, turn_dir)
            if not found_turn:
                self.shift_square(square, dir)

    def turn(self, dir):
        # self.dir = dir
        head = self.body[0]
        self.turns.append(head, dir)

    def grow(self):
        tail = self.body[-1]
        square = Square(x = tail.x, y = tail.y)
        # self.move(self.dir)
        self.body.append(square)

class Game:
    def __init__(self, width, height, food, snake):
        grid = []
        for row in range(height):
            row = []
            for col in range(width):
                row.append(None)
            grid.append(row)
        self.grid = grid
        self.snake = snake
        self.food = food

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
                    for segment in self.snake.body:
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
    food = Food(snake)
    game = Game(WIDTH, HEIGHT, food, snake)
    is_interrupted = False

    def on_press(key):
        try:
            dir = KEY_DICT[key.char]
            snake.move(dir)
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
        # if snake.next_square(dir) == food.square:
        #     food = Food(snake)
        #     snake.grow()

        # snake.grow()

        snake.move(starting_dir)
        time.sleep(SPEED)
    clear_screen()
    game.display()
    listener.join()
