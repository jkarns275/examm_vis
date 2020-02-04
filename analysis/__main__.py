import sys
import os
import subprocess
from collections import OrderedDict

from fitness_log import FitnessLog, DataPoint, Plotter, FitnessLogBatch
from config import Config
from colors import Colors

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import rc

import argparse

pa28_basic = {
    "PA28 Basic": ("basic_pa28", "yellow")
}

def combine(d1, d2):
    return dict(d1, **d2)

def main():
    cfg = Config()
    # rc('text', usetex=True)
    # matplotlib.rcParams['text.latex.unicode']=True
    
    Plotter.set_font(family='serif', size=18)

    plotter = Plotter()
    DATA_DIR = "/home/jak5763/Programming/tl/gecco/results/engine_par"
    
    for name, delay, truncate in cfg.to_plot:
        group = cfg.groups[name]
        for display_name, member in group.items():
            plotter.plot_batch(FitnessLogBatch(f"{cfg.results_dir}/{member}", 10), Colors.next_color(), display_name, start_time=delay, truncate=truncate)

    plotter.ax.set_title(cfg.title)
    plotter.ax.set_ylabel("Mean Squared Error")
    plotter.ax.set_xlabel("Genomes Evaluated")
    
    plotter.set_yrange(0.01, 0.1)
    plotter.set_xrange(2000, 4000)
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    plt.tight_layout()
    plotter.show()
    
if __name__ == '__main__':
    main()
