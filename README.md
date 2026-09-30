# Anvil Dodge Repair Lab

This project is a modular survival dodger game using **Pygame**. It introduces students to falling hazard mechanics, boundary management, collision detection, and survival time tracking within a clean, object-oriented codebase.

---

## What's Provided

A working Anvil Dodge game with:

- A player character that can move left and right across the ground line using keyboard inputs
- Heavy anvils spawned continuously from random horizontal positions falling toward the ground
- Collision detection when an anvil hits the player, triggering game over
- Real-time survival time tracking and a Game Over overlay with restart functionality

It has **one deliberate bug** and **three optional features** left as tasks to implement. You are expected to **analyze**, **interact with an AI assistant**, and **complete/fix** the game to make it fully functional and more interesting.

### **Use an LLM (e.g. ChatGPT or Claude) as your debugging and pair-programming partner for this lab.**
---

## Getting Started

### Setup

1. Make sure you have Python 3.10+ installed.
2. Install dependencies:

```bash
pip install pygame
```

3. Run the game:

```bash
python main.py
```

**Controls:** Left / A to move left, Right / D to move right, R to reset after Game Over.   


## Tasks to Complete

Each task must be completed using an iterative process involving LLM suggestions and your critical code review.

### Task 1: Fix the player off-screen boundary bug [COMPLETED]

The player is supposed to stay inside the visible left and right boundaries of the screen. In the current build, player.update() has no boundary checks, allowing the player to walk indefinitely off the left or right edges of the screen where anvils cannot hit them, achieving infinite survival time. Implement horizontal bounds in player.update() so the player cannot step past 0 or self.screen_width - self.width.

* **Bug (Before):** `Player.update()` in `game/player.py` contained only a `pass` statement. When the player moved left or right using `A`/`D` or the arrow keys, `self.x` had no upper or lower boundary constraints. As a result, the player could move completely off the screen (`x < 0` or `x > screen_width - width`), completely dodging falling anvils and achieving an infinite survival time exploit.
* **Fix Implemented:** In `game/player.py`, implemented boundary clamping inside `Player.update()`:
  ```python
  def update(self):
      if self.x < 0:
          self.x = 0
      elif self.x > self.screen_width - self.width:
          self.x = self.screen_width - self.width
  ```
  This ensures `self.x` is strictly bounded between `0` (left screen boundary) and `self.screen_width - self.width` (right screen boundary, accounting for the player's 44px width), keeping the player sprite fully visible and within hazard range at all times.

### Task 2: Implement dynamic difficulty scaling [COMPLETED]

Right now, anvils spawn at a constant interval of 700ms throughout the entire run. Implement logic in game_engine.update() to decrease spawn_delay as survival_time increases (for example, reducing the delay gradually down to a minimum cap of 200ms), making the game progressively more challenging over time.

* **Implementation Details:** In `game/game_engine.py`, updated `GameEngine.update()` to dynamically adjust `spawn_delay` based on `survival_time`, and updated `GameEngine.reset()` to restore initial difficulty:
  ```python
  # inside GameEngine.update()
  self.spawn_delay = max(200, 700 - (self.survival_time * 10))

  # inside GameEngine.reset()
  self.spawn_delay = 700
  ```
* **Behavior:**
  * **Initial Delay:** Starts at `700ms`.
  * **Scaling Formula:** `spawn_delay` decreases by `10ms` for every `1s` survived.
  * **Minimum Cap:** `max(200, ...)` guarantees the spawn delay never drops below `200ms`.
  * **Reset:** Pressing `R` after Game Over resets `spawn_delay` back to `700ms` and `survival_time` to `0s`.

### Task 3: Implement speed-based anvil tinting [COMPLETED]

All falling anvils currently share identical shades of grey. In anvil.render(), introduce dynamic color tinting based on each anvil's randomized falling speed (self.speed). Fast-falling anvils should render with an orange or red accent, warning the player of rapid hazards.

* **Implementation Details:** In `game/anvil.py`, updated `Anvil.render()` to dynamically calculate color tint based on `self.speed` (`4.5` to `7.0` range):
  ```python
  t = max(0.0, min(1.0, (self.speed - 4.5) / (7.0 - 4.5)))
  top_color = (int(120 + t * (235 - 120)), int(120 + t * (90 - 120)), int(130 + t * (40 - 130)))
  base_color = (int(80 + t * (180 - 80)), int(80 + t * (50 - 80)), int(90 + t * (20 - 90)))
  border_color = (int(200 + t * (255 - 200)), int(200 + t * (150 - 200)), int(210 + t * (100 - 210)))
  ```
* **Visual Appearance:**
  * **Slow Anvils (`speed = 4.5`):** Standard cool grey (`120, 120, 130`).
  * **Fast Anvils (`speed = 7.0`):** Vibrant warning orange/red accent (`235, 90, 40`).

### Task 4: Implement ground impact effects [COMPLETED]

When an anvil leaves the bottom of the screen, it is silently removed from the game. Add a brief visual effect—such as a small dust puff, ground particles, or screen-shake vibration—whenever an anvil strikes the ground before being removed.

* **Implementation Details:** In `game/game_engine.py`, introduced a lightweight `GroundParticle` class. When an anvil passes `anvil.is_off_screen(self.height)`, 8 dust puff / debris particles are generated at `(anvil.x + anvil.width // 2, ground_y)` before removing the anvil:
  ```python
  if anvil.is_off_screen(self.height):
      impact_x = anvil.x + anvil.width // 2
      for _ in range(8):
          self.particles.append(GroundParticle(impact_x, ground_y))
      self.anvils.remove(anvil)
  ```
* **Effect Behavior & Duration:**
  * Each particle bursts upward/outward with randomized velocities and warm ground/dust colors.
  * Particles shrink and fade over a brief lifetime of `10` to `16` frames (~0.2s).
  * Expired particles are removed automatically from memory, and `self.particles.clear()` runs on `reset()`.

---

## Expected Behavior

- The player cannot move beyond the visible left and right edges of the screen
- Anvils fall continuously from randomized X coordinates and clean up after passing below the screen
- Touching any falling anvil immediately triggers the Game Over screen and stops time tracking
- Pressing R after losing resets the player, clears all falling anvils, and restarts the survival timer

---

## Folder Structure

```
anvil_dodge/
├── game/
│   ├── anvil.py
│   ├── game_engine.py
│   └── player.py
├── main.py
└── README.md
```

---

## Submission Checklist

Submission is only the following three things:

- [] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [] The Chat/LLM used page link, with the complete chat history
