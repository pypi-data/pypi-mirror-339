from __future__ import annotations

import tkinter as tk
from argparse import ArgumentParser
from pathlib import Path

from tkinterdnd2 import TkinterDnD

from venvflon.flon import Gui, __version__


def run() -> None:
    """Run the main GUI."""
    parser = ArgumentParser(description='simple virtual environment switcher')
    parser.add_argument('-V', '--version', action='version', version='%(prog)s version: ' + __version__)
    parser.add_argument('-p', '--pwsh', action='store', dest='link_mode', type=int, choices=[0, 5, 7], default=5,
                        help='0 - use Python, pwsh5 or pwsh7 to make symbolic link')
    parser.add_argument('-t', '--timer', action='store', dest='timer', type=float, default=1.2,
                        help='sleep time (in seconds) for pwsh5 and pwsh7')
    args = parser.parse_args()

    root_tk = TkinterDnD.Tk()
    width, height = 300, 250
    root_tk.title(f'venvflon - v{__version__}')
    root_tk.geometry(f'{width}x{height}')
    root_tk.iconphoto(False, tk.PhotoImage(file=Path(__file__).parent / 'img' / 'cannula_64.png'))
    gui = Gui(master=root_tk, cli_args=args)
    gui.mainloop()


if __name__ == '__main__':
    run()
