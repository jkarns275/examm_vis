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
    
    # for name, delay, truncate in cfg.to_plot:
    #     group = cfg.groups[name]
    #     for display_name, member in group.items():
    #         batch = FitnessLogBatch(f"{cfg.results_dir}/{name}/{member}", 10, f"{name}/{member}")
    #         if batch.valid:
    #             if cfg.should_print:
    #                 print("AAA")
    #                 batch.display()
    #             plotter.plot_batch(batch, Colors.next_color(), display_name, start_time=delay, truncate=truncate)


    def tinted(color, nkill):
        # with white
        tinter = (0xFF, 0xFF, 0xFF)
        w0 = (nkill - 1) / 12
        w1 = 1 - w0
        new_color = (int(tinter[0] * w0 + color[0] * w1), int(tinter[1] * w0 + color[1] * w1), int(tinter[2] * w0 + color[2] * w1))
        return new_color

    datatype = "coal"
    # Colors for each nmutations
    colors = { 0 : (0x2e, 0x2e, 0xae), 4 : (0xd8, 0x4b, 0x4b), 8 : (0x4c, 0xaf, 0x4a) }
    targets = []

    # All e1500 runs where darker colors are assigned for more islands killed
    # and different numbers of mutations get different colors.

    batches = []

    for nmuts in (0, 4, 8):
        for nkill in range(1, 11):
            name = f"k{nkill}m{nmuts}"
            batch = FitnessLogBach(f"{cfg.results_dir}/{datatype}/e1500/{name}", 10, f"{name}e1500")
            if batch.valid:
                batches.append(batch)
                plotter.plot_batch(batch, tinted(colors[nmuts], nkill), name, start_time=0, truncate=None)
            else:
                print(f"ERROR: Invalid batch '{name}'")

    plotter.ax.set_title(cfg.title)
    plotter.ax.set_ylabel("Mean Squared Error")
    plotter.ax.set_xlabel("Genomes Evaluated")
    # sax = plotter.ax.secondary_xaxis('top', functions=(lambda x: x - 2000, lambda x: x + 2000))
    # sax.set_xlabel('Transfer Genomes Evaluated')

    plotter.set_yrange(0.0, 0.2)
    plotter.set_xrange(0, 4000)
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    plt.tight_layout()
    plotter.show()
    
if __name__ == '__main__':
    main()
