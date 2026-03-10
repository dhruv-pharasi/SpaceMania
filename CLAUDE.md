# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Game

```bash
python SpaceMania.py
```

Must be run from the project root so the `Assets/` folder is accessible.

## Architecture

The entire game lives in a single file, `SpaceMania.py`. All pygame initialization, asset loading, and constants are defined at module level (top of file). The game loop is in `main()`, which calls itself recursively after a round ends to restart.

Key functions:
- `main()` — game loop; handles events, movement, bullets, win condition, and auto-restarts via recursive call
- `draw_graphics()` — renders background, border, health text, spaceships, and bullets each frame
- `bullet_handler()` — moves bullets and detects collisions using `pygame.Rect.colliderect()`; posts `RED_HIT`/`YELLOW_HIT` custom events
- `yellow_movement()` / `red_movement()` — move spaceships and clamp them within their respective halves

## Gameplay Constants (tweak in `SpaceMania.py`)

| Constant | Default |
|----------|---------|
| `FPS` | 120 |
| `SPACESHIP_VELOCITY` | 5 |
| `BULLET_VELOCITY` | 10 |
| `MAX_BULLETS` | 4 |
| `WIDTH, HEIGHT` | 900, 500 |

## Controls

| Action | Yellow (Left) | Red (Right) |
|--------|--------------|-------------|
| Move | `WASD` | Arrow keys |
| Shoot | `Q` | `Right Shift` |
