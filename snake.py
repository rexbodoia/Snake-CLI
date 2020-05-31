#!/Library/Frameworks/Python.framework/Versions/3.8/bin/python3
import time
import random
from pynput import keyboard

WIDTH = 48
HEIGHT = 25
CLEAR_SPACE = 20
SPEED = 0.15
SNAKE_SYMBOL = 'X'
FOOD_SYMBOL = 'O'
UP = 'UP'; DOWN = 'DOWN'; LEFT = 'LEFT'; RIGHT = 'RIGHT'
KEY_DICT = {'w': UP, 's': DOWN, 'a': LEFT, 'd': RIGHT}
DIRS = [UP, DOWN, LEFT, RIGHT]

def clear_screen():
    for i in range(CLEAR_SPACE):
        print()

def random_dir():
    return DIRS[random.randint(0, len(DIRS) - 1)]

def opposite_dir(dir):
    if dir == UP: return DOWN
    elif dir == DOWN: return UP
    elif dir == LEFT: return RIGHT
    elif dir == RIGHT: return LEFT

def on_press(key, snake):
    try:
        if snake.self_collide(): return False
        dir = KEY_DICT[key.char]
        curr_dir = snake.curr_dir()
        if dir != curr_dir and dir != opposite_dir(curr_dir):
            snake.turn(dir)
        if snake.self_collide(): return False
    except (KeyError, AttributeError):
        global is_interrupted
        is_interrupted = True
        return False

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
        for segment in segments:
            self.body.append((segment, dir))
        self.turns = []

    def head(self):
        head, _dir = self.body[0]
        return head

    def curr_dir(self):
        _head, dir = self.body[0]
        return dir

    def length(self):
        return len(self.body)

    def next_square(self, dir=None):
        if dir == None:
            head, dir = self.body[0]
        else:
            head = self.head()
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

    def get_different_dir(self, game):
        new_dir = DIRS[random.randint(0, len(DIRS) - 1)]
        _head, curr_dir = self.body[0]
        next_square = self.next_square(new_dir)
        out_of_bounds = game.out_of_bounds(next_square)
        while new_dir == curr_dir or new_dir == opposite_dir(curr_dir) or out_of_bounds:
            new_dir = DIRS[random.randint(0, len(DIRS) - 1)]
            next_square = self.next_square(new_dir)
            out_of_bounds = game.out_of_bounds(next_square)
        return new_dir

    def turn(self, dir):
        head = self.head()
        square = Square(x=head.x, y=head.y)
        self.turns.append(Turn(square, dir))
        self.body[0] = head, dir

    def grow(self):
        tail, dir = self.body[-1]
        x = tail.x; y = tail.y
        self.move()
        square = Square(x=x, y=y)
        self.body.append((square, dir))

    def self_collide(self):
        for (square, dir) in self.body[1:-1]:
            if self.next_square() == square:
                return True
        return False

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
        self.gen_food()

    def gen_food(self):
        def already_occupied(x, y):
            already_occupied = False
            for (square, _dir) in self.snake.body:
                if x == square.x and y == square.y:
                    already_occupied = True
            return already_occupied
        gen_x = lambda x : random.randint(1, x - 3)
        gen_y = lambda y : random.randint(1, y - 1)
        x = gen_x(WIDTH); y = gen_y(HEIGHT)
        while already_occupied(x, y):
            x = gen_x(WIDTH); y = gen_y(HEIGHT)
        self.food = Square(x=x, y=y)

    def out_of_bounds(self, square):
        height = len(self.grid)
        width = len(self.grid[0])
        left = square.x < 0
        right = square.x > width - 3
        top = square.y < 0
        bottom = square.y > height - 1
        return left or right or top or bottom

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

if __name__ == '__main__':
    starting_dir = random_dir()
    snake = Snake(starting_dir, Square())
    game = Game(WIDTH, HEIGHT, snake)
    is_interrupted = False
    listener = keyboard.Listener(on_press=lambda key : (on_press(key, snake)))
    listener.start()
    while not is_interrupted and not snake.self_collide():
        clear_screen()
        game.display()
        next_square = snake.next_square()
        if next_square == game.food:
            game.gen_food()
            snake.grow()
        elif game.out_of_bounds(next_square):
            snake.turn(snake.get_different_dir(game))
        else:
            snake.move()
        time.sleep(SPEED)
    clear_screen()
    game.display()
    print('\nYour score:', snake.length())
