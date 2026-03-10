# Space Mania

A 2-player local multiplayer space shooter game built with Python and Pygame. Two spaceships battle it out across a split screen — the first to drain the opponent's health wins.

## Gameplay

Two players share the same keyboard. Each spaceship is confined to its half of the screen, separated by a green border. Players move freely within their half and fire bullets horizontally at the opponent. The game ends when a player's health reaches zero, displaying the winner for 5 seconds before automatically restarting.

## Controls

| Action | Yellow (Left) | Red (Right) |
|--------|--------------|-------------|
| Move Up | `W` | `Up Arrow` |
| Move Down | `S` | `Down Arrow` |
| Move Left | `A` | `Left Arrow` |
| Move Right | `D` | `Right Arrow` |
| Shoot | `Q` | `Right Shift` |

## Features

- 2-player local multiplayer on a single keyboard
- Each player starts with 10 health points
- Max 4 bullets per player on screen at a time
- Sound effects for shooting and bullet hits
- Background arcade music
- Automatic game restart after a winner is declared

## Requirements

- Python 3.x
- Pygame

Install Pygame with:

```bash
pip install pygame
```

## Running the Game

```bash
python SpaceMania.py
```

Make sure you run the command from the project root directory so the `Assets/` folder is accessible.

## Project Structure

```
spaceGame_pygame/
├── SpaceMania.py               # Main game file
└── Assets/
    ├── YellowSpaceship.png     # Yellow player sprite
    ├── RedSpaceship.png        # Red player sprite
    ├── space_1080_540_bcg.png  # Background image
    ├── Gun+Silencer.mp3        # Bullet fire sound effect
    ├── Grenade+1.mp3           # Bullet hit sound effect
    └── arcadeMusic.mp3         # Background music
```

## Game Settings

These constants in `SpaceMania.py` can be tweaked to adjust gameplay:

| Constant | Default | Description |
|----------|---------|-------------|
| `FPS` | 120 | Frames per second |
| `SPACESHIP_VELOCITY` | 5 | Movement speed |
| `BULLET_VELOCITY` | 10 | Bullet speed |
| `MAX_BULLETS` | 4 | Max bullets per player on screen |
| `WIDTH, HEIGHT` | 900, 500 | Window dimensions |
