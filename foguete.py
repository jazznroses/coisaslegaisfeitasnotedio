import pygame
import random
import math
import sys

pygame.init()

WIDTH = 1200
HEIGHT = 700
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Foguetinho Do Jaburu")
clock = pygame.time.Clock()

BG = (10, 12, 20)
GRID = (30, 35, 55)
GREEN = (0, 255, 140)
RED = (255, 70, 70)
WHITE = (240, 240, 240)
YELLOW = (255, 220, 50)
BLUE = (60, 130, 255)


font_big = pygame.font.SysFont("arial", 60, bold=True)
font = pygame.font.SysFont("arial", 28)
small = pygame.font.SysFont("arial", 20)


balance = 1000
bet = 100
multiplier = 1.00
running_round = False
crashed = False
cashed_out = False
profit = 0

points = []
start_x = 100
start_y = HEIGHT - 120


crash_point = 0


cashout_rect = pygame.Rect(930, 560, 220, 70)
play_rect = pygame.Rect(930, 470, 220, 70)

stars = []
for _ in range(120):
    stars.append([
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT),
        random.randint(1, 3)
    ])

def start_round():
    global multiplier
    global running_round
    global crashed
    global cashed_out
    global crash_point
    global points
    global profit
    global balance

    if balance < bet:
        return

    balance -= bet

    multiplier = 1.00
    running_round = True
    crashed = False
    cashed_out = False
    profit = 0

    points = []

  
    crash_point = round(random.uniform(1.3, 12.0), 2)


def draw_background():
    screen.fill(BG)

   
    for s in stars:
        pygame.draw.circle(screen, WHITE, (s[0], s[1]), s[2])

    
    for x in range(0, WIDTH, 50):
        pygame.draw.line(screen, GRID, (x, 0), (x, HEIGHT), 1)

    for y in range(0, HEIGHT, 50):
        pygame.draw.line(screen, GRID, (0, y), (WIDTH, y), 1)


def draw_graph():
    if len(points) > 1:
        pygame.draw.lines(screen, GREEN, False, points, 4)


def draw_rocket(x, y):
    
    pygame.draw.polygon(screen, (255, 120, 0), [
        (x - 10, y + 20),
        (x + 10, y + 20),
        (x, y + 50 + random.randint(0, 10))
    ])

   
    pygame.draw.rect(screen, WHITE, (x - 15, y - 20, 30, 50), border_radius=10)

   
    pygame.draw.polygon(screen, RED, [
        (x - 15, y - 20),
        (x + 15, y - 20),
        (x, y - 45)
    ])

    
    pygame.draw.polygon(screen, BLUE, [
        (x - 15, y + 10),
        (x - 30, y + 30),
        (x - 15, y + 30)
    ])

    
    pygame.draw.polygon(screen, BLUE, [
        (x + 15, y + 10),
        (x + 30, y + 30),
        (x + 15, y + 30)
    ])

   
    pygame.draw.circle(screen, BLUE, (x, y), 7)


def draw_explosion(x, y):
    for i in range(25):
        angle = random.random() * math.pi * 2
        dist = random.randint(10, 80)

        px = x + math.cos(angle) * dist
        py = y + math.sin(angle) * dist

        color = random.choice([
            (255, 200, 0),
            (255, 100, 0),
            (255, 0, 0)
        ])

        pygame.draw.circle(screen, color, (int(px), int(py)), random.randint(4, 10))


def update_game():
    global multiplier
    global crashed
    global running_round

    if running_round and not crashed:
        multiplier += 0.012

        if multiplier >= crash_point:
            crashed = True
            running_round = False


def add_graph_point():
    x = start_x + len(points) * 4

    growth = (multiplier ** 2.1)
    y = start_y - growth * 12

    points.append((x, y))


def draw_ui():
    # multiplicador
    mult_color = GREEN if not crashed else RED

    text = font_big.render(f"{multiplier:.2f}x", True, mult_color)
    screen.blit(text, (470, 40))

    
    bal = font.render(f"Saldo: ${balance}", True, WHITE)
    screen.blit(bal, (20, 20))

   
    bet_text = font.render(f"Aposta: ${bet}", True, WHITE)
    screen.blit(bet_text, (20, 60))

    
    prof = font.render(f"Lucro: ${profit}", True, YELLOW)
    screen.blit(prof, (20, 100))

   
    pygame.draw.rect(screen, BLUE, play_rect, border_radius=15)
    txt = font.render("APOSTAR", True, WHITE)
    screen.blit(txt, (980, 492))

   
    pygame.draw.rect(screen, GREEN, cashout_rect, border_radius=15)
    txt2 = font.render("SACAR", True, WHITE)
    screen.blit(txt2, (995, 582))

   
    info = small.render("Clique em SACAR antes do foguete explodir!", True, WHITE)
    screen.blit(info, (380, 650))


def cash_out():
    global cashed_out
    global profit
    global balance

    if running_round and not crashed and not cashed_out:
        cashed_out = True

        profit = int(bet * multiplier)
        balance += profit

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()

            if play_rect.collidepoint(mouse):
                if not running_round:
                    start_round()

            if cashout_rect.collidepoint(mouse):
                cash_out()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                bet += 10

            if event.key == pygame.K_DOWN:
                bet = max(10, bet - 10)

    update_game()

    if running_round and not crashed:
        add_graph_point()

    draw_background()
    draw_graph()

    
    if len(points) > 0:
        rocket_x, rocket_y = points[-1]

        if crashed:
            draw_explosion(rocket_x, rocket_y)
        else:
            draw_rocket(rocket_x, rocket_y)

    draw_ui()

    # mensagens
    if crashed:
        msg = font_big.render("CRASHOU!", True, RED)
        screen.blit(msg, (450, 280))

    if cashed_out:
        msg = font_big.render("SACOU!", True, GREEN)
        screen.blit(msg, (470, 280))

    pygame.display.flip()