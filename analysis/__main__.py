import sys
import os
import subprocess
from collections import OrderedDict

from op_log import OperatorLog
from fitness_log import FitnessLog, DataPoint, Plotter, FitnessLogBatch
from config import Config
from colors import Colors

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import rc

import argparse

def combine(d1, d2):
    return dict(d1, **d2)

def fitness_main():
    cfg = Config()
    # rc('text', usetex=True)
    # matplotlib.rcParams['text.latex.unicode']=True
    
    Plotter.set_font(family='serif', size=18)

    plotter = Plotter()
    DATA_DIR = "/home/jak5763/Programming/tl/gecco/results/engine_par"
    
    # for name, delay, truncate in cfg.to_plot:
    #     group = cfg.groups[name]
    #     for display_name, member in group.items():
    #         # batch = FitnessLogBatch(f"{cfg.results_dir}/{name}/{member}", 10, f"{name}/{member}")
    #         batch = FitnessLogBatch(f"{cfg.results_dir}/{member}", 10, f"{name}/{member}")
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
        new_color = ((tinter[0] * w0 + color[0] * w1)/255, (tinter[1] * w0 + color[1] * w1)/255, (tinter[2] * w0 + color[2] * w1)/255)
        return new_color

    datatype = "coal"
    # Colors for each nmutations
    colors = { 0 : (0x2e, 0x2e, 0xae), 4 : (0xd8, 0x4b, 0x4b), 8 : (0x4c, 0xaf, 0x4a) }
    targets = []

    # All e1500 runs where darker colors are assigned for more islands killed
    # and different numbers of mutations get different colors.

    control = FitnessLogBatch(f"{cfg.results_dir}coal/num_island_kill_0", 10, f"Control")
    plotter.plot_batch(control, "magenta", "Control", start_time=0)
    
    batches = []

    for nmuts in (0, 4, 8,):
        for nkill in [1]:
            name = f"m{nmuts}k{nkill}"
            batch = FitnessLogBatch(f"{cfg.results_dir}{datatype}/e2000/{name}", 10, f"{name}e2000")
            if batch.valid:
                batches.append(batch)
                plotter.plot_batch(batch, tinted(colors[nmuts], nkill), name, start_time=0, truncate=None)
            else:
                print(f"ERROR: Invalid batch '{name}'")

    import matplotlib.ticker as plticker
    
    ax = plt.gca()
    locx = plticker.MultipleLocator(base=2000)
    ax.xaxis.set_major_locator(locx)

    # Add the grid
    ax.grid(which='major', axis='both', linestyle='-')

    def onresize(event):
        plt.tight_layout()
        plt.tight_layout()
    
    ax = plt.gca()
    cid = ax.figure.canvas.mpl_connect('resize_event', onresize)
    plotter.ax.set_title(cfg.title)
    plotter.ax.set_ylabel("Mean Squared Error")
    plotter.ax.set_xlabel("Genomes Evaluated")
    # sax = plotter.ax.secondary_xaxis('top', functions=(lambda x: x - 2000, lambda x: x + 2000))
    # sax.set_xlabel('Transfer Genomes Evaluated')

    # plotter.set_yrange(0.0, 0.2)
    # plotter.set_xrange(0, 4000)
    # mng = plt.get_current_fig_manager()
    # mng.window.showMaximized()
    plt.tight_layout()
    plt.tight_layout()
    plotter.show()

def operator_main():
    test = OperatorLog("/Users/josh/Programming/exact/test_output/debug/op_log.csv", "test", 0)
    print(f"len = {len(test)}")
    for i in range(len(test)):
        print(test[i].as_dict())
    print("Done")

if __name__ == '__main__':
    operator_main()
    # fitness_main()
