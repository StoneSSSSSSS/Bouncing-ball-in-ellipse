# Bouncing Ball in Ellipse

A Python simulation of a ball bouncing inside an ellipse, built with [Pygame](https://www.pygame.org/).

## How It Works

- An ellipse is drawn to fill the window.
- A ball travels in a straight line and reflects off the ellipse wall using the **angle of incidence = angle of reflection** principle, calculated from the tangent slope at the collision point.
- The two **foci** of the ellipse are marked with red dots.
- Each bounce draws a **red trail line** between consecutive reflection points, visualising the ball's path over time.

## Requirements

- Python 3.x
- Pygame

Install Pygame with:

```bash
pip install pygame
```

## Running

```bash
python elipse_project.py
```

## Controls

| Key / Action | Effect |
|---|---|
| Close window | Quit the simulation |

## Configuration

At the top of `elipse_project.py` you can tweak:

| Variable | Description |
|---|---|
| `fps` | Frames per second (default `30`) |
| `draw_trails` | Show/hide bounce trail lines (`True`/`False`) |
| `Circle(...)` | Starting position, angle, and speed of the ball |
