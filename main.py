from pytetris import tetris
from engine.input import Input

for i in Input.getActionMappings().items():
    print(i)

if (__name__ == "__main__"):
    tetris.run()
