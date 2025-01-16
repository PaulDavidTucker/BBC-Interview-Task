# Blackjack Game Documentation

Assets for the card spritesheet are taken from https://opengameart.org/content/boardgame-pack which is free and under the CC0 license. Credit - www.kenney.nl

This was a really fun mini project! I implemented:

- A working deck of cards, with methods to deal cards (represented in their own class)
- Implemented a fisher yates shuffle to shuffle the deck
- A player / dealer class with the ability to calculate the score
- A game and menu object with loops to continually draw graphics to the screen
- A utils class containing spritesheet splicing logic and game control methods
 - unit tests for the given scenarios on the assignment sheet
 - unit tests for all other functionality! :)

 I'd like to add bets, better animations, sound and possibly a prediction / decision engine to help the player win more games!

## Setup 

- Ensure Python 3 is installed
- Use either a virtual environment or install the required packages globally (I used conda and pip with this project!):
```bash
pip install -r requirements.txt
```
- Run the program with:
```bash
python3 blackjack.py
```

## Testing
- Run the unit tests:

```bash
python3 -m unittest discover test
```

### Debugging install / running of pygame

If using conda on a debian based linux and are met with some form of - libGL error: MESA-LOADER: failed to open swrast then you'll need to copy over the supporting library files:

See [Solution link](https://unix.stackexchange.com/questions/655495/trying-to-run-pygame-on-my-conda-environment-on-my-fresh-manjaro-install-and-ge)

```bash
 cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6 ~/miniconda3/lib/
```