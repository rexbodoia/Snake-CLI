#!/Library/Frameworks/Python.framework/Versions/3.8/bin/python3
import time
import random
from pynput import keyboard

WIDTH = 65
HEIGHT = 25
SPEED = 0.15
SNAKE_SYMBOL = 'X'
FOOD_SYMBOL = 'O'

def clear_screen():
    for i in range(100):
        print()

def display(snake, food):
    horizontal_div = ''
    for i in range(WIDTH):
        horizontal_div += '-'
    print(horizontal_div)
    for y in range(HEIGHT):
        print('|', end = '')
        spaces = ''
        for x in range(WIDTH - 3):
            if x == food.x and y == food.y:
                spaces += FOOD_SYMBOL
            else:
                for square in snake.body:
                    if x == square.x and y == square.y:
                        spaces += SNAKE_SYMBOL
                    else:
                        spaces += ' '
        print(spaces, '|')
    print(horizontal_div)

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
    def __init__(self, *body):
        self.dir = 'DOWN'
        self.body = list(body)

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

    def move(self, dir):
        self.dir = dir
        for square in self.body:
            if dir == 'UP':
                square.y -= 1
            elif dir == 'DOWN':
                square.y += 1
            elif dir == 'LEFT':
                square.x -= 1
            elif dir == 'RIGHT':
                square.x += 1

    def grow(self):
        tail = self.body[-1]
        square = Square(x = tail.x, y = tail.y)
        self.move(self.dir)
        self.body.append(square)

if __name__ == '__main__':
    snake = Snake(Square())
    food = Food(snake)
    def on_press(key):
        try:
            if key.char == 'w':
                dir = 'UP'
            elif key.char == 's':
                dir = 'DOWN'
            elif key.char == 'a':
                dir = 'LEFT'
            elif key.char == 'd':
                dir = 'RIGHT'
            snake.move(dir)
        except AttributeError:
            print("Error")
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    while True:
        clear_screen()
        display(snake, food)
        if snake.next_square(dir) == food.square:
            food = Food(snake)
            snake.grow()
        snake.move(snake.dir)
        time.sleep(SPEED)
    clear_screen()
    display(snake)
    listener.join()
