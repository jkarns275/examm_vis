import sys
import os
import subprocess
from collections import OrderedDict

from fitness_log import FitnessLog, DataPoint, Plotter, FitnessLogBatch

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

c172_to_pa28_all = {
    "C172 to PA28 (Dropped V1)": ("c172_pa28/dropped_ver_1", "red"),
    "C172 to PA28 (Dropped V2)": ("c172_pa28/dropped_ver_2", "green"),
    "C172 to PA28 (Dropped V3)": ("c172_pa28/dropped_ver_3", "blue"),
    "C172 to PA28 (Non-dropped)": ("c172_pa28/dropped_ver_none", "orange"),
}

pa28_basic = {
    "PA28 Basic": ("basic_pa28", "yellow")
}

def combine(d1, d2):
    return dict(d1, **d2)

def main():
    plotter = Plotter()

    DATA_DIR = "/home/jak5763/Dropbox/TransferLearning/gecco/results/engine_par"
    
    groups = { 2000: c172_to_pa28_all, 0: pa28_basic }

    for start_time, group in groups.items():
        for name, (path, color) in group.items():
            plotter.plot_batch(FitnessLogBatch(f"{DATA_DIR}/{path}", 10), color, name, start_time=start_time)

    plotter.ax.set_title("Transfer Learning from C172 to PA28 for Engine Parameters")
    plotter.ax.set_ylabel("Mean Squared Error")
    plotter.ax.set_xlabel("Genome Number")
    
    plotter.set_yrange(0.01, 0.05)
    plotter.set_xrange(2000, 4000)
    plotter.show()
    
if __name__ == '__main__':
    main()
