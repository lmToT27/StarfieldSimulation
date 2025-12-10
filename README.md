# Starfield Simulation: Principles and Algorithms

<p align="center">
  <b> English </b> &nbsp;|&nbsp; <a href="./README.vi.md">Tiếng Việt</a> 
</p>

This document explains in detail the operating mechanism of the Starfield Simulation effect. This is a classic problem in computer graphics used to create a 3D depth illusion on a flat 2D screen.

## 1. Basic Concepts

The goal of this effect is to simulate the perspective of a camera moving at high speed through a cloud of stars. In reality, the camera remains stationary, and the stars move towards the camera.

To achieve this, we need:

- A virtual 3D space.

- A formula to "project" points from that 3D space onto a 2D screen.

## 2. Simulated Coordinate System

Imagine a spatial box with the origin $(0,0,0)$ located at the center of the screen or at the viewer's eye position.

Each star is a data point consisting of 3 variables:

- X (Horizontal): Left/right position relative to the center.

- Y (Vertical): Up/down position relative to the center.

- Z (Depth): Distance from the star to the viewer's eye.

Convention: The positive Z-axis points into the screen (farther away). As Z decreases, it means the star is flying closer to you.

## 3. "Perspective Projection" Formula

This is the "heart" of the algorithm. To transform 3D coordinates $(x, y, z)$ into 2D screen coordinates $(sx, sy)$, we use the principle of similar triangles.

Core Formula:

$$sx = \frac{x}{z} \times FOV + \text{center\_x}$$

$$sy = \frac{y}{z} \times FOV + \text{center\_y}$$

Parameter Explanation:

- $x / z$ and $y / z$: This is the most critical division.

  - When $z$ is large (star is far): The division result is small $\rightarrow$ Star appears near the screen center.

  - When $z$ is small (star is near): The division result is large $\rightarrow$ Star is pushed outwards toward the screen edges.

  - This change creates the illusion that the star is rushing towards you.

- FOV (Field of View): Magnification factor. This value determines the "width" of the lens. A larger FOV results in a narrower viewing angle and a higher sense of speed.

- Center Offset: Since computer screen coordinates usually start at the top-left $(0,0)$, we need to add half the screen width/height to shift the virtual origin to the center.

## 4. Algorithmic Process (Logic Loop)

For the program to work, you need to set up an infinite loop (Game Loop) with the following steps for each star:

Step 1: Initialization

Create an array containing $N$ stars. Each star is assigned random values for $x, y$, and $z$.

- $x$: Random within the virtual width range.

- $y$: Random within the virtual height range.

- $z$: Random from 0 to the maximum depth (Max Depth).

### Step 2: Update (Physics)

In each frame, perform the following for each star:

1. Move: Decrease the star's $z$ value by an amount equal to speed ($z = z - speed$).

2. Boundary Check (Respawn):

- If $z \le 0$ (star has passed the camera), the star is considered gone.

- Immediately "respawn" it by:

  - Resetting $z$ to the farthest position (Max Depth).

  - Choosing new random $x, y$ coordinates.

  - Tip: Setting new $x, y$ prevents the star from repeating its old trajectory, creating a sense of an infinite universe.

### Step 3: Render (Graphics)

After updating the $z$ position, calculate the drawing coordinates:

1. Apply the Perspective Projection formula from Section 3 to find screen coordinates $(sx, sy)$.

2. Calculate Size: The closer the star ($z$ is small), the larger it should be drawn to increase realism.

3. Draw: Draw a circle or a point of light at $(sx, sy)$.

## 5. Advanced Techniques

To make the effect more visually appealing (like the Windows screensaver), you can add the following logic:

- Star Trails:

  - Instead of drawing a point, save the $z$ position from the previous frame ($old\_z$).

  - Calculate screen coordinates for both the current $z$ and $old\_z$.

  - Draw a line connecting these two points. The closer the star, the longer the line, creating a "Warp Speed" effect.

- Brightness by Distance: Stars far away (large $z$) are drawn dark/dim. As they get closer, they brighten up to pure white.

- Interaction: Assign the speed variable or the center coordinates (center_x, center_y) based on mouse position to simulate steering the spaceship.
