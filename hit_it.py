from turtle import *
from time import sleep

class Sprite(Turtle):
    def __init__(self, x, y, step=10, shape='circle', color='black'):
        super().__init__()
        self.penup()
        self.speed(0)
        self.goto(x, y)
        self.color(color)
        self.shape(shape)
        self.step = step
        self.direction = 'right'
    
    def stepRight(self):
        self.goto(self.xcor() + self.step, self.ycor())

    def stepLeft(self):
        self.goto(self.xcor() - self.step, self.ycor())

    def stepUp(self):
        self.goto(self.xcor(), self.ycor() + self.step)

    def stepDown(self):
        self.goto(self.xcor(), self.ycor() - self.step)
    
    def set_move(self):
        if self.xcor() >= 150:
            self.direction = 'left'
        elif self.xcor() <= -150:
            self.direction = 'right'

    def make_step(self):
        if self.direction == 'right':
            self.stepRight()
        elif self.direction == 'left':
            self.stepLeft()

    def move_automatically(self):
        self.set_move()  
        self.make_step()  
            
    def is_collide(self, other):
        if abs(self.xcor() - other.xcor()) < 20 and abs(self.ycor() - other.ycor()) < 20:
            return True
        return False

player = Sprite(0, -100, 10, 'circle', 'orange')
square_1 = Sprite(-150, -30, 10,'square', 'red')
square_2 = Sprite(150, 30, 10, 'square', 'red')
triangle = Sprite(0, 100, 0, 'triangle', 'green')

target_collisions = 0
game_over = False

scr = player.getscreen()
scr.listen()

scr.onkey(player.stepRight, 'Right')
scr.onkey(player.stepLeft, 'Left')
scr.onkey(player.stepUp, 'Up')
scr.onkey(player.stepDown, 'Down')

def game_loop():
    global target_collisions, game_over

    if game_over:
        return

    square_1.move_automatically()
    square_2.move_automatically()

    if player.is_collide(triangle):
        player.goto(0, -100)
        target_collisions += 1
        print(f"Вы поймали цель {target_collisions} раз(а)!")
        if target_collisions >= 3:
            print("Поздравляем, вы победили!")
            square_1.hideturtle()
            square_2.hideturtle()
            game_over = True
            return
    
    if player.is_collide(square_1) or player.is_collide(square_2):
        print("Вы столкнулись с препятствием! Игра окончена.")
        triangle.hideturtle()
        game_over = True
        return
    
    scr.ontimer(game_loop, 100)  

game_loop()

scr.mainloop()














