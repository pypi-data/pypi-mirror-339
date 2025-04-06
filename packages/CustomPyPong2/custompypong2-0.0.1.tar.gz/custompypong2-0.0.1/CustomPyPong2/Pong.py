# Libraries
import random
import pygame

# Func. Game
def CreatePing(font, colorleft, colorright,
               bgcolor, music, sucsound,
               aisoundLeft, aisoundRight, pongSound, match):
    # Initialize
    pygame.init()
    screen = pygame.display.set_mode((800, 500))
    Clock = pygame.time.Clock()
    running = True

    # Scores
    Ta = 0
    Tb = 0

    # Other Variables
    l, x, y, i = 0, 2, 2, 0

    # Music
    music = pygame.mixer.music.load(music)
    pygame.mixer.music.play(-1)

    # Racquets
    Rect1 = pygame.Rect((30, 225), (20, 80))
    Rect2 = pygame.Rect((750, 225), (20, 80))
    Ball = pygame.Rect((397, 250), (10, 10))
    F1 = pygame.font.Font(font, 60)

    #Game Loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(bgcolor)
        T1 = F1.render(f"{int(Ta)}", False, "white")
        screen.blit(T1, T1.get_rect(center=(300, 100)))
        T2 = F1.render(f"{int(Tb)}", False, "white")
        screen.blit(T2, T2.get_rect(center=(500, 100)))
        pygame.draw.line(screen, "#FFFFFF", (400, 60),
                         (400, 440))
        pygame.draw.ellipse(screen, "#FFFFFF", Ball)
        keys = pygame.key.get_pressed()
        pygame.draw.rect(screen, colorleft, Rect1, 0,
                         4)

        # Movement
        if keys[pygame.K_s] and Rect1.bottom <= 480:
            Rect1.y += 7
        if keys[pygame.K_w] and Rect1.bottom >= 100:
            Rect1.y -= 7
        pygame.draw.rect(screen, colorright, Rect2, 0,
                         4)
        if keys[pygame.K_DOWN] and Rect2.bottom <= 480:
            Rect2.y += 7
        if keys[pygame.K_UP] and Rect2.bottom >= 100:
            Rect2.y -= 7

        # Rules
        if Ball.bottom >= 500:
            x *= 1
            y *= -1
        elif Ball.top <= 0:
            x *= 1
            y *= -1

        # More Movement
        if Rect1.colliderect(Ball):
            l += 1
            x *= -1
            y *= 1
            if l == 1:
                l = 0
                noice = pygame.mixer.Sound(pongSound)
                noice.play()
        elif Rect2.colliderect(Ball):
            l += 1
            x *= -1
            y *= 1
            if l == 1:
                l = 0
                noice = pygame.mixer.Sound(pongSound)
                noice.play()

        # Ball Movement
        Ball.x += x
        Ball.y += y

        # Scoring
        if Ball.x <= 0:
            Tb += 1
        if Ball.x >= 800:
            Ta += 1
        if Ta >= match:
            pygame.mixer.Sound(aisoundLeft).play()
        if Tb >= match:
            pygame.mixer.Sound(aisoundRight).play()


        # Serve
        if Ball.x <= 0 or Ball.x >= 800:
            Ball = pygame.Rect((397, 250), (10, 10))
            i = 0
            x = random.choice([2, -2])
            y = random.choice([2, -2])
            pygame.mixer.Sound(sucsound).play()

        # Close
        pygame.display.update()
        Clock.tick(100)