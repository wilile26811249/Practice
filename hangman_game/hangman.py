import os
import math
import random
import pygame
import nltk
from nltk.corpus import brown

# OS Path Setting
current_folder = os.path.dirname(os.path.abspath(__file__))
images_path = os.path.join(current_folder, 'images')

# Setup Display
pygame.init()
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("~~Hangman Game~~")

# Button Variables
RADIUS = 20
GAP = 15
letters = []  # [position_x, position_y, char, visible]
startX = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
startY = 400
for i in range(26):
    x = startX + RADIUS + ((RADIUS * 2 + GAP) * (i % 13))
    y = startY + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(65 + i), True])

# Fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)

# load images
images = []
for i in range(7):
    image = os.path.join(images_path, "hangman" + str(i) + ".jpg")
    images.append(image)

# Game Variables
hangman_status = 0
news_text = brown.words(categories='news')
words = [vocabulary.upper() for vocabulary in news_text if 2 < len(vocabulary) and len(vocabulary) < 6 and vocabulary.isalpha()]
word = ""
guessed = []


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Setup game loop
FPS = 60
clock = pygame.time.Clock()
run = True

def draw():
    '''
    Draw button
    '''
    win.fill(WHITE)

    # Draw title
    text = TITLE_FONT.render("DEVELOPER HANGMAN", 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, 20))

    # Draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (400, 200))

    # Draw buttons
    for letter in letters:
        posx, posy, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (posx, posy), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(text, (posx - text.get_width() / 2, posy - text.get_height() / 2))

    win.blit(pygame.image.load(images[hangman_status]), (150, 100))
    pygame.display.update()

def display_message(message):
    pygame.time.delay(1000)
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(2000)

def reset_status():
    global guessed, letters, hangman_status
    hangman_status = 0
    guessed = []
    for letter in letters:
        letter[3] = True

def main():
    global run, hangman_status, FPS, RADIUS, guessed, letters, word
    word = random.choice(words)
    print(word)
    while run:
        clock.tick(FPS)
        draw()
        text = TITLE_FONT.render(word, 1, BLACK)
        win.blit(text, (WIDTH / 2 - text.get_width() / 2, 10))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # Close window
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1

        draw()
        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break

        if won:
            display_message("You Win!")
            reset_status()
            break

        if hangman_status == 6:
            display_message("You Lost! The answer is " + word)
            reset_status()
            won = True
            break

while True:
    if run:
        main()
    else:
        break
pygame.quit()

