# Snakey

A simple snake game made with pygame with multiplayer option.

## Running the game

To install Snakey, run the following command:

```bash
python -m pip install snakey
```

Then, to run the game, execute:

```bash
python -m snakey
```

A new window should appear where you and your friend can play a game of snake. Default keys for player one are 
<kbd>&uarr;</kbd>, <kbd>&darr;</kbd>, <kbd>&rarr;</kbd> and <kbd>&larr;</kbd>. Keys for player two are 
<kbd>W</kbd>, <kbd>S</kbd>, <kbd>D</kbd> and <kbd>A</kbd>.

## Game configuration
Game configuration is defined with a json configuration file, by default, this configuration is set like this:

```json
{
    "main_window_size": [640, 480],
	"block_size": 10,
    "refresh_rate": 100,
    "num_snakes": 2,
    "start_pos": [[300, 100],
			   [300, 200],
			   [300, 300],
			   [300, 400]],
    "keys": [["K_UP", "K_RIGHT", "K_DOWN", "K_LEFT"],
		     ["K_w", "K_d", "K_s", "K_a"],
		     ["K_t", "K_h", "K_g", "K_f"],
		     ["K_i", "K_l", "K_k", "K_j"]],
	"initial_snake_length": 10,
	"num_cherries": 2
}
```

In order to run the game with different configuration, create a new .json file, and modify the configuration there.
Then, provide the path to the created file with *--config* option, like this

```bash
python -m snakey --config {path to configuration file}
```

