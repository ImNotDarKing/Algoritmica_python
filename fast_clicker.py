import pygame
from random import randint
import time

pygame.init()

LIGHT_BLUE = (200, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (80, 80, 225)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
LIGHT_GREEN = (200, 255, 200)
LIGHT_RED = (250, 128, 114)
WINDOW_HEIGHT, WINDOW_WIDTH = (500, 500)

window = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
window.fill(LIGHT_BLUE)

clock = pygame.time.Clock()

class Area():
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = color

    def color(self, new_color):
        self.fill_color = new_color

    def fill(self):
        pygame.draw.rect(window, self.fill_color, self.rect)

    def outline(self, frame_color, thickness):
        pygame.draw.rect(window, frame_color, self.rect, thickness)

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)

class Label(Area):
    def set_text(self, text, fsize=12, text_color=BLACK):
        self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)

    def draw(self, shift_x=0, shift_y=0):
        self.fill()
        window.blit(self.image, (self.rect.x+shift_x, self.rect.y+shift_y))

cards = []
num_cards = 4
x = 70

for i in range(num_cards):
    new_card = Label(x, 170, 70, 100, YELLOW)
    new_card.outline(BLUE, 10)
    new_card.set_text('CLICK', 26)
    cards.append(new_card)
    x += 100

text_timer = Label(10, 10, 90, 80, LIGHT_BLUE)
text_timer.set_text('Время:', 30)
text_timer.draw(10, 10)

timer = Label(50, 55, 50, 30, LIGHT_BLUE)
timer.set_text('0', 30)
timer.draw(0, 0)

text_score = Label(390, 10, 90, 80, LIGHT_BLUE)
text_score.set_text('Счет:', 30)
text_score.draw(20, 10)

score = Label(430, 55, 50, 30, LIGHT_BLUE)
score.set_text('0', 30)
score.draw(0, 0)

wait = 0
points = 0
start_time = time.time()
cur_time = time.time()

end_game = 0 #0 - продолжаем игру, 1 - победа, 2 -  проигрыш

while end_game == 0:
    if wait == 0:
        wait = 20
        click = randint(0, num_cards-1)
        for i in range(num_cards):
            cards[i].color(YELLOW)
            if i == click:
                cards[i].draw(10, 40)
            else:
                cards[i].fill()
    else:
        wait -= 1

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            for i in range(num_cards):
                if cards[i].collidepoint(x, y):
                    if i == click:
                        cards[i].color(GREEN)
                        points += 1
                    else:
                        cards[i].color(RED)
                        if points > 0:
                            points -= 1
                    cards[i].fill()
                    score.set_text(str(points), 30)
                    score.draw(0, 0)

    new_time = time.time()
    if new_time - cur_time >= 1:
        timer.set_text(str(int(new_time - start_time)), 30)
        timer.draw(0, 0)
        cur_time = new_time
    
    if points >= 5:
        end_game = 1
    if new_time - start_time > 10:
        end_game = 2

    pygame.display.update()
    clock.tick(40)

if end_game == 1:
    win = Label(0, 0, 500, 500, LIGHT_GREEN)
    win.set_text('WINNER!!!', 60)
    win.draw(160, 180)
    result_time = Label(90, 230, 250, 250, LIGHT_GREEN)
    result_time.set_text('Время прохождения: ' + str(int(new_time-start_time))+' сек.', 40)
    result_time.draw(0, 0)
elif end_game == 2:
    lose = Label(0, 0, 500, 500, LIGHT_RED)
    lose.set_text('LOSER!!!', 60)
    lose.draw(160, 180)

pygame.display.update()







    