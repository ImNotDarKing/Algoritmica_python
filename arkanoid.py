import pygame

pygame.init()

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BACKGROUND = (200, 255, 255)
WINDOW_WIDTH, WINDOW_HEIGHT = 500, 500
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
window.fill(BACKGROUND)

clock = pygame.time.Clock()

platform_x, platform_y = 200, 300 
ball_x, ball_y = 160, 200

dx = 5
dy = 5

class Area():
    def __init__(self, x=0, y=0, width=10, height=10, color=BACKGROUND):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = color

    def color(self, new_color):
        self.fill_color = new_color

    def fill(self):
        pygame.draw.rect(window, self.fill_color, self.rect)

    def colliderect(self, rect1):
        return self.rect.colliderect(rect1)

class Label(Area):
    def set_text(self, text, fsize=12, text_color=BLACK):
        self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)

    def draw(self, shift_x=0, shift_y=0):
        self.fill()
        window.blit(self.image, (self.rect.x+shift_x, self.rect.y+shift_y))

class Picture(Area):
    def __init__(self, filename, x=0, y=0, width=10, height=10, color=BACKGROUND):
        super().__init__(x, y, width, height, color)
        self.image = pygame.image.load(filename)

    def draw(self):
        self.fill()
        window.blit(self.image, (self.rect.x, self.rect.y))

ball = Picture('ball.png', ball_x, ball_y, 50, 50)
platform = Picture('platform.png', platform_x, platform_y, 100, 30)

start_x = 5
start_y = 5
n = 9

monsters = []

for i in range(3):
    x = start_x + 27.5*i
    y = start_y + 55*i
    for i in range(n):
        enemy = Picture('enemy.png', x, y, 50, 50)
        monsters.append(enemy)
        x += 55
    n -= 1

game_over = False
move_right = False
move_left = False

while not game_over:
    platform.fill()
    ball.fill()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                move_right = True
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                move_left = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                move_right = False
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                move_left = False
    
    if move_left and platform.rect.x > 0:
        platform.rect.x -= 5
    if move_right and platform.rect.x < 400:
        platform.rect.x += 5

    ball.rect.x += dx
    ball.rect.y += dy

    if ball.colliderect(platform.rect) or ball.rect.y < 0:
        dy *= -1
    
    if ball.rect.x < 0 or ball.rect.x > 450:
        dx *= -1

    for enemy in monsters:
        enemy.draw()
        if enemy.colliderect(ball.rect):
            monsters.remove(enemy)
            enemy.fill()
            dy *= -1

    if ball.rect.y > platform_y + platform.rect.height:
        lose_text = Label(150, 160, 50, 50, BACKGROUND)
        lose_text.set_text('YOU LOSE!', 60, RED)
        lose_text.draw(10, 10)
        game_over = True

    if len(monsters) == 0:
        win_text = Label(150, 160, 50, 50, BACKGROUND)
        win_text.set_text('YOU WIN!', 60, GREEN)
        win_text.draw(10, 10)
        game_over = True

    ball.draw()
    platform.draw()
    
    pygame.display.update()
    clock.tick(40)


