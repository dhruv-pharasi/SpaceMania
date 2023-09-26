import pygame
pygame.font.init()
pygame.mixer.init()

# CONSTANTS
WIDTH, HEIGHT = 900, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Mania")
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
FPS = 120
BORDER = pygame.Rect((WIDTH//2)-5, 0, 10, HEIGHT)
SPACESHIP_DIMENSIONS = (70, 60)
SPACESHIP_VELOCITY = 5
BULLET_VELOCITY = 10
MAX_BULLETS = 4
HEALTH_FONT = pygame.font.SysFont("Verdana", 40)
WINNER_FONT = pygame.font.SysFont("Verdana", 100)
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
YELLOW_SPACESHIP_IMAGE = pygame.image.load("Assets/YellowSpaceship.png")
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, SPACESHIP_DIMENSIONS), 90)
RED_SPACESHIP_IMAGE = pygame.image.load("Assets/RedSpaceship.png")
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, SPACESHIP_DIMENSIONS), 270)
BACKGROUND_IMAGE = pygame.image.load("Assets/space_1080_540_bcg.png")
BULLET_HIT_SOUND_EFFECT = pygame.mixer.Sound("Assets/Grenade+1.mp3")
BULLET_FIRE_SOUND_EFFECT = pygame.mixer.Sound("Assets/Gun+Silencer.mp3")
BACKGROUND_MUSIC = pygame.mixer.Sound("Assets/arcadeMusic.mp3")


# GAME FUNCTIONS
def draw_graphics(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    ''' Draw graphics on screen '''
    WINDOW.blit(BACKGROUND_IMAGE, (0, 0))
    pygame.draw.rect(WINDOW, GREEN, BORDER)

    red_health_text = HEALTH_FONT.render(f"Health: {red_health}", 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        f"Health: {yellow_health}", 1, WHITE)

    WINDOW.blit(red_health_text,
                (WIDTH - red_health_text.get_width() - 10, 10))
    WINDOW.blit(yellow_health_text, (10, 10))

    WINDOW.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WINDOW.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW, YELLOW, bullet)

    pygame.display.update()


def bullet_handler(yellow_bullets, red_bullets, yellow, red):
    '''Handling bullets'''
    # Checking for collision with red spaceship from yellow bullet
    for yellow_bullet in yellow_bullets:
        yellow_bullet.x += BULLET_VELOCITY
        if red.colliderect(yellow_bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(yellow_bullet)
        elif yellow_bullet.x > WIDTH:
            yellow_bullets.remove(yellow_bullet)

    # Checking for collision with yellow spaceship from red bullet
    for red_bullet in red_bullets:
        red_bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(red_bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(red_bullet)
        elif red_bullet.x + red_bullet.width < 0:
            red_bullets.remove(red_bullet)


def yellow_movement(keys_pressed, yellow):
    ''' Move yellow spaceship '''
    if keys_pressed[pygame.K_a]:  # Left movement
        yellow.x -= SPACESHIP_VELOCITY
        if (yellow.x < 0):
            yellow.x = 0

    if keys_pressed[pygame.K_d]:    # Right movement
        yellow.x += SPACESHIP_VELOCITY
        if (yellow.x > (WIDTH/2)-75):
            yellow.x = (WIDTH/2)-75

    if keys_pressed[pygame.K_w]:  # Up movement
        yellow.y -= SPACESHIP_VELOCITY
        if (yellow.y < 0):
            yellow.y = 0

    if keys_pressed[pygame.K_s]:    # Down movement
        yellow.y += SPACESHIP_VELOCITY
        if (yellow.y + yellow.height > HEIGHT - 10):
            yellow.y = HEIGHT - yellow.height - 10


def red_movement(keys_pressed, red):
    ''' Move red spaceship '''
    if keys_pressed[pygame.K_LEFT]:  # Left movement
        red.x -= SPACESHIP_VELOCITY
        if (red.x < (WIDTH/2)+15):
            red.x = (WIDTH/2)+15

    if keys_pressed[pygame.K_RIGHT]:    # Right movement
        red.x += SPACESHIP_VELOCITY
        if (red.x + red.width - 10 > 900):
            red.x = 900 - red.width + 10

    if keys_pressed[pygame.K_UP]:  # Up movement
        red.y -= SPACESHIP_VELOCITY
        if (red.y < 0):
            red.y = 0

    if keys_pressed[pygame.K_DOWN]:    # Down movement
        red.y += SPACESHIP_VELOCITY
        if (red.y + red.height > HEIGHT - 10):
            red.y = HEIGHT - red.height - 10


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WINDOW.blit(draw_text, (WIDTH//2 - draw_text.get_width() //
                2, HEIGHT/2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    '''Game loop'''
    yellow = pygame.Rect(
        100, 215, SPACESHIP_DIMENSIONS[0], SPACESHIP_DIMENSIONS[1])
    red = pygame.Rect(
        750, 215, SPACESHIP_DIMENSIONS[0], SPACESHIP_DIMENSIONS[1])

    yellow_bullets = []
    yellow_health = 10

    red_bullets = []
    red_health = 10

    BACKGROUND_MUSIC.play()

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                BACKGROUND_MUSIC.stop()
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + (yellow.height)//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND_EFFECT.play()

                if event.key == pygame.K_RSHIFT and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + (red.height//2) - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND_EFFECT.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND_EFFECT.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND_EFFECT.play()

        winner_text = ""

        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_graphics(red, yellow, red_bullets, yellow_bullets,
                          red_health, yellow_health)
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_movement(keys_pressed, yellow)
        red_movement(keys_pressed, red)
        bullet_handler(yellow_bullets, red_bullets, yellow, red)
        draw_graphics(red, yellow, red_bullets, yellow_bullets,
                      red_health, yellow_health)

    BACKGROUND_MUSIC.stop()
    main()


if __name__ == "__main__":
    main()
