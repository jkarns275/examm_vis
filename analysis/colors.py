from matplotlib import colors as mcolors
from random import shuffle

def make_colors():
    colors = [
        "tab:blue",
        "tab:orange",
        "tab:green",
        "tab:red",
        "tab:purple",
        "tab:brown",
        "tab:pink",
        "tab:gray",
        "tab:olive",
        "tab:cyan"
    ]
    return tuple(colors)

class Colors:

    RESULTS_DIR = "RESULTS_DIR"

    COLORS = make_colors() 

    COLOR_IDX = 0

    @staticmethod
    def next_color():
        r = Colors.COLORS[Colors.COLOR_IDX % len(Colors.COLORS)]
        Colors.COLOR_IDX += 1
        return r

 
