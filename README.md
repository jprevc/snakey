# Snakey 🐍

> A classic snake game written in Python with pygame — supports up to **4 players simultaneously**.

[![CI](https://github.com/jprevc/snakey/actions/workflows/main.yml/badge.svg)](https://github.com/jprevc/snakey/actions/workflows/main.yml)
[![PyPI](https://img.shields.io/pypi/v/snakey)](https://pypi.org/project/snakey/)
[![Python](https://img.shields.io/pypi/pyversions/snakey)](https://pypi.org/project/snakey/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.txt)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

---

## Features

- Up to 4 players on a single keyboard
- Configurable window size, speed, number of cherries, and key bindings via JSON
- Restart automatically after a collision
- Installable as a CLI tool via `pip` or `uv`

---

## Installation

### From PyPI

```bash
pip install snakey
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv tool install snakey
```

### Running the game

```bash
snakey
```

Or, if installed as a module:

```bash
python -m snakey
```

---

## Default Controls

| Player | Up  | Down | Left | Right |
|--------|-----|------|------|-------|
| 1      | ↑   | ↓    | ←    | →     |
| 2      | W   | S    | A    | D     |
| 3      | T   | G    | F    | H     |
| 4      | I   | K    | J    | L     |

---

## Configuration

The game loads a JSON configuration file at startup. Pass a custom one with the `--config` flag:

```bash
snakey --config my_config.json
```

### Configuration options

| Key                    | Type               | Description                                                      |
|------------------------|--------------------|------------------------------------------------------------------|
| `main_window_size`     | `[width, height]`  | Game window dimensions in pixels                                 |
| `block_size`           | `int`              | Size of each snake/cherry block in pixels                        |
| `refresh_rate`         | `int`              | Game tick interval in milliseconds (lower = faster)              |
| `num_snakes`           | `int`              | Number of players (1–4)                                          |
| `initial_snake_length` | `int`              | Starting length of each snake in blocks                          |
| `num_cherries`         | `int`              | Number of cherries on the board at once                          |
| `start_pos`            | `[[x, y], …]`      | Starting position for each snake's head                          |
| `keys`                 | `[["K_UP", …], …]` | Pygame key names for each player (`up`, `right`, `down`, `left`) |

### Default configuration

```json
{
    "main_window_size": [640, 480],
    "block_size": 10,
    "refresh_rate": 100,
    "num_snakes": 2,
    "start_pos": [[300, 100], [300, 200], [300, 300], [300, 400]],
    "keys": [
        ["K_UP",  "K_RIGHT", "K_DOWN", "K_LEFT"],
        ["K_w",   "K_d",     "K_s",    "K_a"],
        ["K_t",   "K_h",     "K_g",    "K_f"],
        ["K_i",   "K_l",     "K_k",    "K_j"]
    ],
    "initial_snake_length": 10,
    "num_cherries": 100
}
```

---

## Development

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (recommended)

### Setup

```bash
git clone https://github.com/jprevc/snakey.git
cd snakey

# Install project and dev dependencies
uv sync

# Install pre-commit hooks
uv run pre-commit install
```

### Running tests

```bash
uv run pytest -v
```

### Linting and formatting

```bash
uv run ruff check src tests      # lint
uv run ruff format src tests     # format
uv run mypy src                  # type checking
```

---

## License

[MIT](LICENSE.txt) © Jost Prevc
