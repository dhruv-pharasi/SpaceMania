"""
Space Mania - A two-player space combat game using Pygame.

Players control spaceships on opposite sides of the screen and try to
destroy each other using bullets. The first player to reduce their opponent's
health to 0 wins the round. The game automatically restarts after each round.
"""

import pygame

# Initialize pygame subsystems for font rendering and audio playback
pygame.font.init()
pygame.mixer.init()

# ============================================================================
# GAME WINDOW & DISPLAY CONSTANTS
# ============================================================================
WIDTH, HEIGHT = 900, 500                    # Game window dimensions (in pixels)
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Mania")
FPS = 120                                   # Target frame rate (frames per second)

# ============================================================================
# COLOR CONSTANTS (RGB tuples)
# ============================================================================
YELLOW = (255, 255, 0)                      # Color for yellow spaceship & bullets
GREEN = (0, 255, 0)                         # Color for center border divider
WHITE = (255, 255, 255)                     # Color for text & UI elements
RED = (255, 0, 0)                           # Color for red spaceship & bullets

# ============================================================================
# GAME MECHANICS CONSTANTS
# ============================================================================
BORDER = pygame.Rect((WIDTH//2)-5, 0, 10, HEIGHT)  # Center divider separating player territories
SPACESHIP_DIMENSIONS = (70, 60)             # Width and height of spaceship sprites (pixels)
SPACESHIP_VELOCITY = 5                      # Speed of spaceship movement per frame (pixels/frame)
BULLET_VELOCITY = 10                        # Speed of bullet movement per frame (pixels/frame)
MAX_BULLETS = 4                             # Maximum bullets each player can have on screen simultaneously

# ============================================================================
# TEXT & FONT CONSTANTS
# ============================================================================
HEALTH_FONT = pygame.font.SysFont("Verdana", 40)   # Font for displaying health values
WINNER_FONT = pygame.font.SysFont("Verdana", 100)  # Font for displaying winner text

# ============================================================================
# CUSTOM EVENTS FOR GAME STATE
# ============================================================================
# Custom events posted when a bullet hits a spaceship (used for event handling)
YELLOW_HIT = pygame.USEREVENT + 1           # Event triggered when yellow spaceship is hit
RED_HIT = pygame.USEREVENT + 2              # Event triggered when red spaceship is hit

# ============================================================================
# VISUAL ASSETS (Images & Sprites)
# ============================================================================
# Load and transform yellow spaceship image
YELLOW_SPACESHIP_IMAGE = pygame.image.load("Assets/YellowSpaceship.png")
# Scale to dimensions and rotate 90° so it faces right (toward red player)
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, SPACESHIP_DIMENSIONS), 90)

# Load and transform red spaceship image
RED_SPACESHIP_IMAGE = pygame.image.load("Assets/RedSpaceship.png")
# Scale to dimensions and rotate 270° so it faces left (toward yellow player)
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, SPACESHIP_DIMENSIONS), 270)

# Load background image for the game scene
BACKGROUND_IMAGE = pygame.image.load("Assets/space_1080_540_bcg.png")

# ============================================================================
# AUDIO ASSETS (Sound Effects & Music)
# ============================================================================
BULLET_HIT_SOUND_EFFECT = pygame.mixer.Sound("Assets/Grenade+1.mp3")   # Sound when bullet hits spaceship
BULLET_FIRE_SOUND_EFFECT = pygame.mixer.Sound("Assets/Gun+Silencer.mp3")  # Sound when bullet is fired
BACKGROUND_MUSIC = pygame.mixer.Sound("Assets/arcadeMusic.mp3")        # Looping background music


# ============================================================================
# GAME FUNCTIONS
# ============================================================================

def draw_graphics(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    """
    Render all game graphics to the screen each frame.

    This function is called every frame to draw:
    - Background image
    - Center border divider
    - Health text for both players
    - Both spaceship sprites
    - All active bullets on screen

    Args:
        red (pygame.Rect): Position and dimensions of red spaceship
        yellow (pygame.Rect): Position and dimensions of yellow spaceship
        red_bullets (list): List of red bullet pygame.Rect objects
        yellow_bullets (list): List of yellow bullet pygame.Rect objects
        red_health (int): Current health value of red player (0-10)
        yellow_health (int): Current health value of yellow player (0-10)
    """
    # Draw the space background image at origin (0, 0)
    WINDOW.blit(BACKGROUND_IMAGE, (0, 0))

    # Draw green border down the middle to separate player territories
    pygame.draw.rect(WINDOW, GREEN, BORDER)

    # Render health text for each player
    red_health_text = HEALTH_FONT.render(f"Health: {red_health}", 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        f"Health: {yellow_health}", 1, WHITE)

    # Place red health in top-right corner
    WINDOW.blit(red_health_text,
                (WIDTH - red_health_text.get_width() - 10, 10))
    # Place yellow health in top-left corner
    WINDOW.blit(yellow_health_text, (10, 10))

    # Draw both spaceships at their current positions
    WINDOW.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WINDOW.blit(RED_SPACESHIP, (red.x, red.y))

    # Draw all active red bullets as rectangles
    for bullet in red_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)

    # Draw all active yellow bullets as rectangles
    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW, YELLOW, bullet)

    # Update the display to show all drawn graphics
    pygame.display.update()


def bullet_handler(yellow_bullets, red_bullets, yellow, red):
    """
    Update bullet positions and detect collisions with spaceships.

    This function handles all bullet movement and collision detection:
    - Yellow bullets move right toward the red player
    - Red bullets move left toward the yellow player
    - When a bullet hits a spaceship, a HIT event is posted and the bullet is removed
    - Bullets that leave the screen are also removed to free memory

    Args:
        yellow_bullets (list): List of yellow bullet pygame.Rect objects
        red_bullets (list): List of red bullet pygame.Rect objects
        yellow (pygame.Rect): Bounding box of yellow spaceship
        red (pygame.Rect): Bounding box of red spaceship
    """
    # Process all yellow bullets (fired by yellow player toward red player)
    for yellow_bullet in yellow_bullets:
        # Move bullet right by BULLET_VELOCITY pixels per frame
        yellow_bullet.x += BULLET_VELOCITY

        # Check if yellow bullet collides with red spaceship
        if red.colliderect(yellow_bullet):
            # Post custom event to trigger red player taking damage
            pygame.event.post(pygame.event.Event(RED_HIT))
            # Remove bullet from active bullets list after collision
            yellow_bullets.remove(yellow_bullet)
        # Remove bullet if it travels beyond right edge of screen (off-screen)
        elif yellow_bullet.x > WIDTH:
            yellow_bullets.remove(yellow_bullet)

    # Process all red bullets (fired by red player toward yellow player)
    for red_bullet in red_bullets:
        # Move bullet left by BULLET_VELOCITY pixels per frame
        red_bullet.x -= BULLET_VELOCITY

        # Check if red bullet collides with yellow spaceship
        if yellow.colliderect(red_bullet):
            # Post custom event to trigger yellow player taking damage
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            # Remove bullet from active bullets list after collision
            red_bullets.remove(red_bullet)
        # Remove bullet if it travels beyond left edge of screen (off-screen)
        elif red_bullet.x + red_bullet.width < 0:
            red_bullets.remove(red_bullet)


def yellow_movement(keys_pressed, yellow):
    """
    Handle yellow spaceship movement based on keyboard input.

    Yellow player controls (left side of screen):
    - A/D keys: Move left/right (confined to left half of screen)
    - W/S keys: Move up/down (confined to screen boundaries)

    Movement is clamped to keep the spaceship within valid bounds:
    - Cannot move past left/right borders (only left half of screen)
    - Cannot move past top/bottom borders

    Args:
        keys_pressed (pygame.key.get_pressed()): Array of all currently pressed keys
        yellow (pygame.Rect): Mutable spaceship position/dimensions
    """
    # Move left (A key): decrease x position
    if keys_pressed[pygame.K_a]:
        yellow.x -= SPACESHIP_VELOCITY
        # Clamp to left boundary (cannot go past left edge)
        if yellow.x < 0:
            yellow.x = 0

    # Move right (D key): increase x position
    if keys_pressed[pygame.K_d]:
        yellow.x += SPACESHIP_VELOCITY
        # Clamp to center border (cannot cross into red player's territory)
        if yellow.x > (WIDTH/2) - 75:
            yellow.x = (WIDTH/2) - 75

    # Move up (W key): decrease y position
    if keys_pressed[pygame.K_w]:
        yellow.y -= SPACESHIP_VELOCITY
        # Clamp to top boundary (cannot go past top edge)
        if yellow.y < 0:
            yellow.y = 0

    # Move down (S key): increase y position
    if keys_pressed[pygame.K_s]:
        yellow.y += SPACESHIP_VELOCITY
        # Clamp to bottom boundary (cannot go past bottom edge, accounting for ship height)
        if yellow.y + yellow.height > HEIGHT - 10:
            yellow.y = HEIGHT - yellow.height - 10


def red_movement(keys_pressed, red):
    """
    Handle red spaceship movement based on keyboard input.

    Red player controls (right side of screen):
    - Left/Right arrow keys: Move left/right (confined to right half of screen)
    - Up/Down arrow keys: Move up/down (confined to screen boundaries)

    Movement is clamped to keep the spaceship within valid bounds:
    - Cannot move past left/right borders (only right half of screen)
    - Cannot move past top/bottom borders

    Args:
        keys_pressed (pygame.key.get_pressed()): Array of all currently pressed keys
        red (pygame.Rect): Mutable spaceship position/dimensions
    """
    # Move left (LEFT arrow): decrease x position
    if keys_pressed[pygame.K_LEFT]:
        red.x -= SPACESHIP_VELOCITY
        # Clamp to center border (cannot cross into yellow player's territory)
        if red.x < (WIDTH/2) + 15:
            red.x = (WIDTH/2) + 15

    # Move right (RIGHT arrow): increase x position
    if keys_pressed[pygame.K_RIGHT]:
        red.x += SPACESHIP_VELOCITY
        # Clamp to right boundary (cannot go past right edge, accounting for ship width)
        if red.x + red.width - 10 > 900:
            red.x = 900 - red.width + 10

    # Move up (UP arrow): decrease y position
    if keys_pressed[pygame.K_UP]:
        red.y -= SPACESHIP_VELOCITY
        # Clamp to top boundary (cannot go past top edge)
        if red.y < 0:
            red.y = 0

    # Move down (DOWN arrow): increase y position
    if keys_pressed[pygame.K_DOWN]:
        red.y += SPACESHIP_VELOCITY
        # Clamp to bottom boundary (cannot go past bottom edge, accounting for ship height)
        if red.y + red.height > HEIGHT - 10:
            red.y = HEIGHT - red.height - 10


def draw_winner(text):
    """
    Display the winner message on screen and pause for 5 seconds.

    This function renders large text (e.g., "Yellow Wins!" or "Red Wins!")
    centered on the screen, then freezes the game for 5 seconds before
    the game loop continues and restarts.

    Args:
        text (str): The winner message to display (e.g., "Yellow Wins!")
    """
    # Render the winner text using the large WINNER_FONT (100pt)
    draw_text = WINNER_FONT.render(text, 1, WHITE)

    # Calculate centered position: x at screen center, y at screen middle
    # (subtract half the text width/height to center it)
    WINDOW.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2,
                            HEIGHT // 2 - draw_text.get_height() // 2))

    # Update display to show the winner message
    pygame.display.update()

    # Pause for 5 seconds (5000 milliseconds) to let players see the result
    pygame.time.delay(5000)


def main():
    """
    Main game loop that handles one complete round of Space Mania.

    Game Flow:
    1. Initialize both spaceships at starting positions
    2. Set initial health (10 for each player)
    3. Start background music
    4. Enter main loop:
       - Process events (quit, key presses, collisions)
       - Update spaceship positions based on keyboard input
       - Move and handle collisions for all bullets
       - Render frame to screen
       - Check for winner each frame
    5. When a player's health <= 0, display winner and restart game

    The game runs at FPS (120 frames/second) and recursively calls itself
    after each round to restart.
    """
    # ========== INITIALIZATION ==========
    # Initialize yellow spaceship: x=100, y=215 (left side, centered vertically)
    yellow = pygame.Rect(
        100, 215, SPACESHIP_DIMENSIONS[0], SPACESHIP_DIMENSIONS[1])

    # Initialize red spaceship: x=750, y=215 (right side, centered vertically)
    red = pygame.Rect(
        750, 215, SPACESHIP_DIMENSIONS[0], SPACESHIP_DIMENSIONS[1])

    # Initialize empty bullet lists (will store bullet Rect objects)
    yellow_bullets = []
    yellow_health = 10

    red_bullets = []
    red_health = 10

    # Start background music (loops during gameplay)
    BACKGROUND_MUSIC.play()

    # Initialize clock for frame rate control
    clock = pygame.time.Clock()
    run = True

    # ========== MAIN GAME LOOP ==========
    while run:
        # Cap frame rate at FPS (120 frames/second)
        clock.tick(FPS)

        # Process all pygame events (keyboard, mouse, quit, etc.)
        for event in pygame.event.get():
            # Handle window close button (quit game completely)
            if event.type == pygame.QUIT:
                run = False
                BACKGROUND_MUSIC.stop()
                pygame.quit()

            # Handle keyboard key presses
            if event.type == pygame.KEYDOWN:
                # Yellow player shoots (Q key): create bullet at right edge of spaceship
                # Only allow shooting if under MAX_BULLETS limit
                if event.key == pygame.K_q and len(yellow_bullets) < MAX_BULLETS:
                    # Create bullet starting from the right edge of yellow spaceship,
                    # centered vertically on the ship (10x5 pixel rectangle)
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + (yellow.height)//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    # Play gun fire sound effect
                    BULLET_FIRE_SOUND_EFFECT.play()

                # Red player shoots (RIGHT SHIFT key): create bullet at left edge of spaceship
                # Only allow shooting if under MAX_BULLETS limit
                if event.key == pygame.K_RSHIFT and len(red_bullets) < MAX_BULLETS:
                    # Create bullet starting from the left edge of red spaceship,
                    # centered vertically on the ship (10x5 pixel rectangle)
                    bullet = pygame.Rect(
                        red.x, red.y + (red.height//2) - 2, 10, 5)
                    red_bullets.append(bullet)
                    # Play gun fire sound effect
                    BULLET_FIRE_SOUND_EFFECT.play()

            # Handle custom collision events (posted by bullet_handler)
            if event.type == RED_HIT:
                # Red spaceship was hit by yellow bullet: decrease health
                red_health -= 1
                # Play bullet impact sound effect
                BULLET_HIT_SOUND_EFFECT.play()

            if event.type == YELLOW_HIT:
                # Yellow spaceship was hit by red bullet: decrease health
                yellow_health -= 1
                # Play bullet impact sound effect
                BULLET_HIT_SOUND_EFFECT.play()

        # ========== WIN CONDITION CHECK ==========
        winner_text = ""

        # Check if red player's health is depleted
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        # Check if yellow player's health is depleted
        if yellow_health <= 0:
            winner_text = "Red Wins!"

        # If we have a winner, display result and end this round
        if winner_text != "":
            # Draw final frame with game state
            draw_graphics(red, yellow, red_bullets, yellow_bullets,
                          red_health, yellow_health)
            # Display winner message and pause for 5 seconds
            draw_winner(winner_text)
            # Break out of game loop to restart
            break

        # ========== UPDATE GAME STATE ==========
        # Get currently pressed keys (allows holding down keys for continuous movement)
        keys_pressed = pygame.key.get_pressed()

        # Update yellow spaceship position based on WASD input
        yellow_movement(keys_pressed, yellow)

        # Update red spaceship position based on arrow key input
        red_movement(keys_pressed, red)

        # Update all bullet positions and check for collisions
        bullet_handler(yellow_bullets, red_bullets, yellow, red)

        # Render all game graphics to screen
        draw_graphics(red, yellow, red_bullets, yellow_bullets,
                      red_health, yellow_health)

    # ========== ROUND COMPLETE ==========
    # Stop background music before restarting
    BACKGROUND_MUSIC.stop()

    # Recursively call main() to restart the game for a new round
    main()


# ============================================================================
# PROGRAM ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    # Start the game by calling main() only when this file is run directly
    # (not when imported as a module in another file)
    main()
