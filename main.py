'''
This program is a game called legman, written with pygame
'''
import random
import pygame
import sys


def start_screen():
    '''
    Showing start screen, with buttons, clouds, captions etc.
    '''
    # placing clouds in random places
    for i in range(5):
        cloud_box[i].center = [random.randint(-100, 700),
                               random.randint(-100, 900)]
    legman_box.center = (window_box.centerx, 250)
    # code for buttons
    button_box = [pygame.Rect(window_box.centerx - 200, 400, 400, 100),
                  pygame.Rect(window_box.centerx - 200, 550, 400, 100),
                  pygame.Rect(window_box.centerx - 200, 700, 400, 100)]
    button_text = [big_font.render("Start", True, (pygame.Color("black"))),
                   big_font.render("High scores", True,
                                   (pygame.Color("black"))),
                   big_font.render("Exit", True, (pygame.Color("black")))]
    button_text_box = [button_text[0].get_rect(),
                       button_text[1].get_rect(), button_text[2].get_rect()]
    for i in range(3):
        button_text_box[i].center = button_box[i].center

    title = big_font.render("Legman The Game", True, (pygame.Color("black")))
    title_box = title.get_rect()
    title_box.center = (window_box.centerx, 100)

    run = "True"
    # start screen loop
    while run:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_box[0].collidepoint(mouse[0], mouse[1]):
                    run = "False"
                    game()
                if button_box[1].collidepoint(mouse[0], mouse[1]):
                    run = "False"
                    high_scores_screen()
                if button_box[2].collidepoint(mouse[0], mouse[1]):
                    sys.exit()
        window.fill(pygame.Color('cyan2'))
        for i in range(7):
            window.blit(cloud[i], cloud_box[i])
        for i in range(3):
            pygame.draw.rect(window, pygame.Color("red"), button_box[i], 0)
            window.blit(button_text[i], button_text_box[i])
        window.blit(legman, legman_box)
        window.blit(title, title_box)
        pygame.display.flip()


def game():
    """
    Main game function
    """
#   Defining global variables, objects, pictures and variables
#   needed for main game loop
    global legman_box, legman, vec, hight, platform, jump_allow, ground_box, \
        game_speed, keys, acc, vec, legman_facing_left
    ground = pygame.image.load("groung.png")
    ground_box = ground.get_rect()
    ground_box.center = (window_box.centerx + 10, 880)
    legman_box.center = (window_box.centerx, 650)

    platform = [pygame.Rect(random.randint(-20, 550),
                            random.randint(-10, 60) + 750,
                            random.randint(70, 230), 40),
                pygame.Rect(random.randint(-20, 550),
                            random.randint(-60, 60) + 600,
                            random.randint(70, 230), 40),
                pygame.Rect(random.randint(-20, 550),
                            random.randint(-60, 60) + 450,
                            random.randint(70, 230), 40),
                pygame.Rect(random.randint(-20, 550),
                            random.randint(-60, 60) + 300,
                            random.randint(70, 230), 40),
                pygame.Rect(random.randint(-20, 550),
                            random.randint(-60, 60) + 150,
                            random.randint(70, 230), 40),
                pygame.Rect(random.randint(-20, 550),
                            random.randint(-60, 60), random.randint(70, 230),
                            40),
                pygame.Rect(random.randint(-20, 550),
                            random.randint(-60, 60) - 150,
                            random.randint(70, 230), 40),
                pygame.Rect(random.randint(-20, 550),
                            random.randint(-60, 60) - 300,
                            random.randint(70, 230), 40)]

    pygame.key.set_repeat(10, 70)
    fps = pygame.time.Clock()

    pygame.mixer.music.load('Bounce.mp3')

    vec = [0, 0]
    acc = [0, 3]
    hight = 0
    jump_allow = "True"
    legman_facing_left = "True"
    run = "True"
    game_speed = 1
#   main game loop
    while run:
        acc[0] = 0
        FRICTION[1] = 0.04
        jump_allow = "False"
        keys = pygame.key.get_pressed()
        struct_generator()
        key_inputs()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        window.fill(pygame.Color('cyan2'))
        movement_animation()
        for i in range(3):
            window.blit(cloud[i], cloud_box[i])
        for i in range(7):
            pygame.draw.rect(window, pygame.Color("chocolate4"),
                             platform[i], 0)
        window.blit(ground, ground_box)
        window.blit(legman, legman_box)
        score()
        pygame.display.flip()
        fps.tick(60)


def key_inputs():
    '''
    Reading inputs and calculating player's position
    '''
    global keys, legman, jump_allow, legman_facing_left, acc, vec, legman_box, \
        FRICTION
#   Reading inputs and performing actions based on them
    if keys[pygame.K_RIGHT]:
        if legman_facing_left == "True":
            legman = pygame.transform.flip(legman, True, False)
            legman_facing_left = "False"
        acc[0] = 1
    if keys[pygame.K_LEFT]:
        if legman_facing_left == "False":
            legman = pygame.transform.flip(legman, True, False)
            legman_facing_left = "True"
        acc[0] = -1
    if keys[pygame.K_SPACE] and jump_allow == "True" and vec[1] == 0:
        pygame.mixer.music.play()
        vec[1] = -70
        jump_allow = "False"
    # Game's physisc / calculating player's position
    vec[0] -= vec[0] * FRICTION[0]
    vec[0] += acc[0]
    vec[1] -= vec[1] * FRICTION[1]
    vec[1] += acc[1]
    legman_box = legman_box.move(vec[0] + 0.5 * acc[0],
                                 vec[1] + 0.5 * acc[1])


def movement_animation():
    '''
    Function moves objects down, creating inpresion of player going upwards
    '''
    pygame.mixer.music.load('death.mp3')
    global game_speed, hight
    if window_box.left > legman_box.right:
        legman_box.left = window_box.right
    if window_box.right < legman_box.left:
        legman_box.right = window_box.left
    if legman_box.centery + 150 < window_box.centery:
        for i in range(7):
            platform[i][1] += 15
        for i in range(3):
            cloud_box[i][1] += 15
        ground_box[1] += 15
        hight += 15
        legman_box.centery += 15
    if legman_box.top > window_box.bottom:
        pygame.mixer.music.play()
        game_end_screen()
    for i in range(7):
        platform[i][1] += game_speed
    for i in range(3):
        cloud_box[i][1] += game_speed
    ground_box[1] += game_speed
    legman_box.centery += game_speed
    hight += game_speed
    game_speed = int(hight / 1500)


def high_scores_screen():
    '''
    Screen containing 5 best scores
    '''
    global high_scores
    read_scores()
    button_box = [pygame.Rect(35, 650, 300, 100),
                  pygame.Rect(365, 650, 300, 100)]

    button_text = [medium_font.render("Menu", True, (pygame.Color("black"))),
                   medium_font.render("Exit", True, (pygame.Color("black")))]
    button_text_box = [button_text[0].get_rect(), button_text[1].get_rect()]
    for i in range(2):
        button_text_box[i].center = button_box[i].center

    high_scores_text = big_font.render("High Scores:", True,
                                       (pygame.Color("black")))
    high_scores_text_box = high_scores_text.get_rect()
    high_scores_text_box.center = (window_box.centerx, 40)

    scores = []
    scores_box = []
    for i in range(5):
        scores.append(
            medium_font.render("nr." + str(i + 1) + ":  " +
                               str(high_scores[i]), True,
                               (pygame.Color("black"))))
        scores_box.append(scores[i].get_rect())
        scores_box[i].centery = 150 + 100 * i
        scores_box[i].left = 200

    run = "True"

    while run:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_box[0].collidepoint(mouse[0], mouse[1]):
                    run = "False"
                    start_screen()
                if button_box[1].collidepoint(mouse[0], mouse[1]):
                    sys.exit()
        window.fill(pygame.Color('cyan2'))
        for i in range(2):
            pygame.draw.rect(window, pygame.Color("red"), button_box[i], 0)
            window.blit(button_text[i], button_text_box[i])
        for i in range(5):
            window.blit(scores[i], scores_box[i])
        window.blit(high_scores_text, high_scores_text_box)
        pygame.display.flip()


def struct_generator():
    """
    Generate clouds, platforms, detect colisions
    """
    global jump_allow, vec, ground_box
    if legman_box.colliderect(ground_box):
        if vec[1] > 0:
            vec[1] = 0
            jump_allow = "True"
            legman_box.bottom = ground_box.top + 10
    for i in range(7):
        if platform[i].top > window_box.bottom + 30:
            platform[i] = pygame.Rect(random.randint(-20, 550),
                                      random.randint(-60, 60) - 180,
                                      random.randint(70, 230), 40)
            if i == 0:
                if platform[7].centery - platform[i].centery < 150:
                    platform[i] = pygame.Rect(random.randint(-20, 550),
                                              random.randint(-80, 80) - 180,
                                              random.randint(70, 230), 40)
            else:
                if platform[i - 1].centery - platform[i].centery < 150:
                    platform[i] = pygame.Rect(random.randint(-20, 550),
                                              random.randint(-80, 80) - 180,
                                              random.randint(70, 230), 40)
            for n in range(7):
                if not i == n:
                    while platform[i].colliderect(platform[n]):
                        platform[i] = pygame.Rect(random.randint(-50, 600),
                                                  random.randint(-75, 75) - 200,
                                                  random.randint(50, 250), 40)
        if legman_box.colliderect(platform[i]) \
                and legman_box.bottom < platform[i].bottom:
            if vec[1] >= 0:
                vec[1] = 0
                jump_allow = "True"
                legman_box.bottom = platform[i].top
    for i in range(5):
        if cloud_box[i].centery > window_box.bottom:
            cloud_box[i].center = [random.randint(-50, 600),
                                   random.randint(-900, -100)]


def score():
    """
    Score box in right upper corner
    """
    global hight
    score = small_font.render("score: " + str(hight),
                              True, (pygame.Color("black")))
    score_box = score.get_rect()
    score_box.center = (600, 20)
    window.blit(score, score_box)


def add_score():
    """
    Save score in txt file
    """
    global hight
    file = open("High scores.txt", 'a')
    file.write("\n" + str(hight))
    file.close()


def read_scores():
    '''
    Read scores from txt file, and put 5 highest of them into variable
    '''
    global high_scores
    file = open("High scores.txt", 'r')
    all_scores = []
    high_scores = []
    for line in file:
        all_scores.append(int(line.strip()))
    for n in list(reversed(sorted(all_scores)))[:5]:
        high_scores.append(n)
    file.close()


def game_end_screen():
    """
    You loose, you see this screen
    """
    global hight
    add_score()
#   defining buttons and text
    button_box = [pygame.Rect(195, 450, 300, 100),
                  pygame.Rect(35, 600, 300, 100),
                  pygame.Rect(365, 600, 300, 100)]

    button_text = [medium_font.render("Play", True,
                                      (pygame.Color("black"))),
                   medium_font.render("High scores",
                                      True, (pygame.Color("black"))),
                   medium_font.render("Exit", True,
                                      (pygame.Color("black")))]
    button_text_box = [button_text[0].get_rect(),
                       button_text[1].get_rect(),
                       button_text[2].get_rect()]
    for i in range(3):
        button_text_box[i].center = button_box[i].center

    final_score = big_font.render("Your score: " + str(hight),
                                  True, (pygame.Color("black")))
    final_score_box = final_score.get_rect()
    final_score_box.center = (window_box.centerx, 100)

    run = "True"
    # main loop of the function
    while run:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_box[0].collidepoint(mouse[0], mouse[1]):
                    run = "False"
                    game()
                if button_box[1].collidepoint(mouse[0], mouse[1]):
                    run = "False"
                    high_scores_screen()
                if button_box[2].collidepoint(mouse[0], mouse[1]):
                    sys.exit()
        window.fill(pygame.Color('cyan2'))
        for i in range(3):
            pygame.draw.rect(window, pygame.Color("red"), button_box[i], 0)
            window.blit(button_text[i], button_text_box[i])
        window.blit(legman, legman_box)
        window.blit(final_score, final_score_box)
        pygame.display.flip()


if __name__ == '__main__':
    '''
    Initiating pygame, defining screen size, reading fonts, music
    and picture files, also declarating some objects
    '''
    pygame.init()

    Display_Width, Display_Height = 700, 900
    window = pygame.display.set_mode((Display_Width, Display_Height))
    pygame.display.set_caption("Legman")

    window_box = window.get_rect()

    big_font = pygame.font.Font("ChunkFive-Regular.otf", 60)
    medium_font = pygame.font.Font("ChunkFive-Regular.otf", 40)
    small_font = pygame.font.Font("ChunkFive-Regular.otf", 20)

    cloud = [pygame.image.load("cloud1.png"),
             pygame.image.load("cloud2.png"),
             pygame.image.load("cloud3.png"),
             pygame.image.load("cloud4.png"),
             pygame.image.load("cloud1.png"),
             pygame.image.load("cloud2.png"),
             pygame.image.load("cloud3.png"),
             pygame.image.load("cloud4.png")]
    cloud_box = [cloud[0].get_rect(), cloud[1].get_rect(),
                 cloud[2].get_rect(), cloud[3].get_rect(),
                 cloud[4].get_rect(), cloud[5].get_rect(),
                 cloud[6].get_rect(), cloud[7].get_rect()]
    legman = pygame.image.load("legman.png")
    legman_box = legman.get_rect()
    FRICTION = [0.05, 0.04]
    start_screen()
