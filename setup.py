import os

from cx_Freeze import setup, Executable

os.environ['TCL_LIBRARY'] = r'C:\Users\Megaport\PycharmProjects\GameOfLife\venv\Lib\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Program Files\Python37\tcl\tk8.6'

setup(
    name='Game of Life',
    version='1.0',
    author="Valentin FOUCHER",
    description="Implémentation du jeu de la vie de John Conway",
    executables=[Executable('run.py')]
)
