from matplotlib import colors as mcolors
from random import shuffle

def make_colors():
    colors = list(dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS).keys())
    shuffle(colors)
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

 
