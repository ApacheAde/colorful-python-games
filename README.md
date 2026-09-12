# Colorful Python Games

A small arcade of **full-colour** Python 3 games built with Pygame.

Made for **[ElbowOS](https://x.com/ElbowOS)** — a new world OS.

**GitHub:** https://github.com/ApacheAde/colorful-python-games  
**X:** https://x.com/ElbowOS

## Games

| Game | File | What it is |
|------|------|------------|
| Super Block Bros | `super_block_bros.py` | Colourful side-scrolling platformer (Mario-style jump & run — original art, not an emulator) |
| Neon Blackjack | `neon_blackjack.py` | Casino card game vs the dealer |
| Lucky Slots | `lucky_slots.py` | Three-reel slot machine |
| Memory Cards | `memory_cards.py` | Flip-and-match colour cards |
| Neon Snake | `neon_snake.py` | Classic snake with a neon palette |

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
```

Needs **Python 3.10+** and a display (Pygame / SDL).

## Controls

- **Launcher:** click a game, or press `1`–`5`. Esc quits.
- **Super Block Bros:** A/D or arrows move, Space/W/Up jump. Esc quit.
- **Blackjack:** H hit, S stand, N new hand. Esc quit.
- **Slots:** Space or click SPIN. Esc quit.
- **Memory:** click two cards. Esc quit.
- **Snake:** arrows or WASD. Esc quit.

## Licence

MIT. Have fun.
