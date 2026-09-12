# Colorful Python Games

A small arcade of **full-colour** Python 3 games built with Pygame.

Made for **[ElbowOS](https://x.com/ElbowOS)** — a new world OS.

**GitHub:** https://github.com/ApacheAde/colorful-python-games  
**X:** https://x.com/ElbowOS

## Games

| Key | Game | File | What it is |
|-----|------|------|------------|
| 1 | Super Block Bros | `super_block_bros.py` | Side-scrolling platformer (Mario-style jump & run — original art, **not** an emulator) |
| 2 | Neon Blackjack | `neon_blackjack.py` | Casino card game vs the dealer |
| 3 | Lucky Slots | `lucky_slots.py` | Three-reel slot machine |
| 4 | Memory Cards | `memory_cards.py` | Flip-and-match colour cards |
| 5 | Neon Snake | `neon_snake.py` | Classic snake with a neon palette |
| 6 | Neon Roulette | `neon_roulette.py` | European-style wheel (red / black / zero / even / odd) |
| 7 | Ruby Draw Poker | `ruby_draw_poker.py` | 5-card draw with hold/draw and payouts |
| 8 | Brick Breakout | `brick_breakout.py` | Arcade brick breaker |
| 9 | Pipe Glide | `pipe_glide.py` | Flyer through neon pipes |
| a | Space Raiders | `space_raiders.py` | Invader-style shooter |
| b | Neon Pong | `neon_pong.py` | Arcade rally vs the CPU |
| c | Color Connect | `color_connect.py` | Four-in-a-row vs CPU |
| d | Neon Craps | `neon_craps.py` | Pass-line dice table |
| e | Color Stack | `color_stack.py` | Falling-block puzzle |

These are **simple originals**. Super Block Bros is a homegrown platformer drawn with shapes — it is **not** a Nintendo emulator and includes no ROM or copyrighted assets.

## Run

```bash
python3 -m pip install -r requirements.txt
python3 launcher.py
```

Or run any game directly:

```bash
python3 super_block_bros.py
python3 neon_blackjack.py
python3 lucky_slots.py
python3 memory_cards.py
python3 neon_snake.py
python3 neon_roulette.py
python3 ruby_draw_poker.py
python3 brick_breakout.py
python3 pipe_glide.py
python3 space_raiders.py
python3 neon_pong.py
python3 color_connect.py
python3 neon_craps.py
python3 color_stack.py
```

Needs **Python 3.10+** and a display (Pygame / SDL).

## Controls

- **Launcher:** click a game, or press `1`–`9` and `a`–`e`. Esc quits.
- **Super Block Bros:** A/D or arrows move, Space/W/Up jump. Esc quit.
- **Blackjack:** H hit, S stand, N new hand. Esc quit.
- **Slots:** Space or click SPIN. Esc quit.
- **Memory:** click two cards. Esc quit.
- **Snake:** arrows or WASD. Esc quit.
- **Roulette:** click a bet, Space or SPIN. `+`/`-` change stake.
- **Poker:** D deal/draw, click cards to HOLD. `+`/`-` change stake.
- **Breakout:** A/D or arrows. R restart.
- **Pipe Glide:** Space / click to flap.
- **Space Raiders:** arrows / A D move, Space fire, R restart.
- **Pong:** W/S or arrows.
- **Color Connect:** click a column. R restart.
- **Craps:** Space roll, `+`/`-` stake.
- **Color Stack:** arrows / WASD, Up rotate, Space hard drop.

## Licence

MIT. Have fun.
