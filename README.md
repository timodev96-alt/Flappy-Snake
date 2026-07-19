# Flappy-Snake

### The famous Snake from that old game traveld to the FlappyBird game !
<img width="850" height="848" alt="image" src="https://github.com/user-attachments/assets/1793912d-39fc-4924-8515-6b1fbe08f735" />


##### A combination of dual games mechanics -Grid moving system for the snake and pipes moving system from flappy bird!- All chained together with a push system to make everything buttery SMOOTH !

## Features

* Classic snake movment in 25x25 Grid
* Flappy Bird-style Pipes scroll all from the right
* Amazing cutscenes for starting the game and death ! -First time to do that (: -
* Pause & Settings menu - pipe speed (Easy / Medium / Hard) and music volume, adjustable live, even mid-game.
* **Coins & Shop** - every apple you eat earns coins; spend them in the shop to unlock and equip new snake skins.
* Special apples with unique effects (see below)
* A growing library of unlockable Snake Skins!! - Alot of skins :D
* Local save file (JSON) so your settings, coins, skins, and high score persist between sessions

## Controles


| Action                   | Key                    |
| ------------------------ | ---------------------- |
| Move                     | W A S D or Arrow Keys |
| Pause / Menu             | ESC                    |
| Open Shop (title screen) | S                      |
| Confirm / Select         | `Enter` / `Space`     |
| Navigate menus           | W S / `↑ ↓`          |
| Adjust a setting         | A D / `← →`          |
| Start (title screen)     | Any key                |

## Apples
 
Apples aren't all the same — each one that spawns is rolled from a weighted pool:
<img width="960" height="240" alt="Milk Snake(1)" src="https://github.com/user-attachments/assets/f7748c95-610a-4108-bfcd-e41f65b4b4da" />
 
| Apple        | Chance | Score      | Coins | Effect |
|--------------|--------|------------|-------|--------|
| Apple (red)  | 85%    | 49–74      | 5     | — |
| Golden Apple (Golden?) | 5%     | 142–173    | 15    | — |
| Shield Apple (Blue) | 5%     | 10–20      | 0     | Grants a one-time shield that lets you smash through the next pipe you'd otherwise die on |
| Wide Gap Apple (Green) | 5%   | 10–20      | 0     | Widens the gap on the next 5 pipes, making them easier to pass |
 
Passing safely through a pipe's gap also earns you **9–23 points**.
 
---

## Dependencies

* `Python 3.10+`
* `pygame 2.6.1+`
* `numpy` (optinal - used in few generated sound effects)

### Install & Run

```
pip install pygame numpy
python main.py
```

#### Or just grab the pre-built [.exe](https://github.com/timodev96-alt/Flappy-Snake/releases/download/Main/FlappySnake.exe) if one is available for your release! 


# Snake Skins system

Each skin is just **4 images**:


| File         | What it should show                     |
| ------------ | --------------------------------------- |
| `head.png`   | The head, facing right                  |
| `tail.png`   | The tail, facing left                   |
| `body.png`   | A straight body segment, vertical      |
| `corner.png` | A corner piece that bends down + right |

#### Exacley Like This :

<img width="240" height="240" alt="Milk Snake" src="https://github.com/user-attachments/assets/5ee9a160-0aa9-41f2-ba97-dcc3a23e063e" />

Also must me rigisterd in `settings.py`:

```
SNAKE_SKINS.append(
       {"id": "my_skin", "name": "My Skin", "folder": "Your Skin Name", "cost": 75}
   )
```

That's it - `sprites.py` automatically rotates those 4 pieces into all 14 sprites the game needs (all tail directions, all 4 head directions, both body orientations, and all 4 corner orientations). No other code changes required.

# Everything is tunable from `settings.py`

Here's every gameplay-affecting value and what it's set to at startup:

**Grid / Screen**

* `cell_size = 34` px per grid cell
* `cell_number = 25` cells per side
* `screen_cords = 850` px (window is 850×850)

**Pipes**

* `pipe_speed = 1.9` (active at startup — matches the EASY preset, so the game starts on Easy)
* `PIPE_SPEED_PRESETS`: EASY = 1.9, MEDIUM = 2.1, HARD = 2.6
* `top_bottom_pipe_space = 4` — vertical gap a snake can pass through, in grid cells
* `pipe_to_pipe_space = 500` — horizontal pixel gap between consecutive pipes
* `initial_pipe_delay = 90` frames (\~1.5s at 60fps) before the very first pipe spawns

**Snake**

* `SNAKE_SIZE_SCALE = 1.2` — draw size multiplier (also scales the pipe hitbox slightly bigger than the base 0.8-cell tolerance
* Snake moves once every 9 game-update ticks (hardcoded)

**Scoring & Coins**

* Eating an apple: random score of **49–74 points**
* Passing through a pipe: random score of **9–23 points**
* Coins = 0 at startup -- *what do u expect? :D*
* Coins per Apple = 5 - coins earned per apple eaten (separate from score)

**Audio**

* Music Volume = 0.6 (60%) - at start up
* Music Volume Step = 0.05 - amount each menu press changes volume by

  ### There’s no right or wrong here! - just set them up in a way that makes sense to you.
