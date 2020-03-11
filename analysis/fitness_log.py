import numpy as np
import csv
import matplotlib.pyplot as plt
import matplotlib as mpl
from collections import OrderedDict

class DataPoint:

    def __init__(self, inserted_genomes, bp_epochs, time, best_mae, best_mse, \
                    enabled_nodes, enabled_edges, enabled_rec_edges, *argv):
        self.genomes = int(inserted_genomes)
        self.bp_epochs = int(bp_epochs)
        self.time = int(time)
        self.mae = float(best_mae)
        self.mse = float(best_mse)
        self.nodes = int(enabled_nodes)
        self.edges = int(enabled_edges)
        self.rec_edges = int(enabled_rec_edges)


    def __str__(self):
           return f"inserted genomes: {self.genomes}, bp_epochs: {self.bp_epochs}, " + \
                f"time: {self.time}, best mae: {self.mae}, best mse: {self.mse}, " + \
                f"enabled nodes: {self.nodes}, enabled edges: {self.edges}, " + \
                f"enabled recursive edges: {self.rec_edges}"

class FitnessLog:

    def __init__(self, file_path, name, fold):
        # python csv docs say use newline='' of using a file object
        self.data = []
        self.name = name
        self.fold = fold

        try:
            with open(file_path, newline='') as csvfile:
                csv_reader = csv.reader(csvfile, delimiter=',')

                # Ignore the first row because it is column names
                for row in csv_reader:
                    break
                
                for row in csv_reader:
                    dp = DataPoint(*row)
                    self.data.append(dp)
            self.valid = len(self.data) > 0
            if self.valid:
                self.breakthroughs = len(set(self.query(lambda l: l.mse)))
        
        except Exception as e:
            self.valid = False

    def display(self):
        print(f"    fold {self.fold}: len={len(self)}; min_mse={min(self.query(lambda l: l.mse))}; breakthrough_count={self.breakthroughs}")

    def get_row_dict(self, index):
        dp = self.data[index]
        return {'genomes_inserted': dp.genomes,
                'bp_epochs': dp.bp_epochs,
                'mae': dp.mae,
                'mse': dp.mse,
                'nodes': dp.nodes,
                'edges': dp.edges,
                'rec_edges': dp.rec_edges}

    def __getitem__(self, item):
        assert type(item) == int
        return self.data[item]

    def __len__(self):
        return len(self.data)

    def query(self, l):
        return list(map(l, self.data))

class FitnessLogBatch:

    def __init__(self, folder_path, n, batch_name):
        self.logs = []
        self.batch_name = batch_name

        for i in range(n):
            log = FitnessLog(f"{folder_path}/{i}/fitness_log.csv", batch_name, i)
            if log.valid:
                self.logs.append(log)
        
        if len(self.logs) == 0:
            self.valid = False
        else:
            self.longest_log_len = max(map(len, self.logs))
            self.calculate_min_line()
            self.calculate_max_line()
            self.calculate_mean_line()
            self.avg_breakthroughs = np.mean(list(map(lambda l: l.breakthroughs, self.logs)))
            self.std_breakthroughs = np.std(list(map(lambda l: l.breakthroughs, self.logs)))
            # Only valid if every entry is valid
            # self.valid = sum(map(lambda log: 1 if log.valid else 0, self.logs)) == n
            self.valid = True
    
    def display_stats(self):
        best_mses = list(map(lambda log: min(log.query(lambda l: l.mse)), self.logs))
        # average of the best MSEs (lower MSE is better)
        mean_best_mse = sum(best_mses) / len(self.logs)
        # Lowest MSE out of all logs
        min_best_mse = min(best_mses)
        # Given the list of best MSEs from each log, which one is largest?
        worst_best_mse = max(best_mses)

        return  f"best: {min_best_mse}; worst: {worst_best_mse}; average: {mean_best_mse};\n" + \
                f"avg_breakthroughs: {self.avg_breakthroughs} (stdev={self.std_breakthroughs})"

    def display(self):
        print(f"FitnessLogBatch {self.batch_name}: {self.display_stats()}")
        for log in self.logs:
            log.display()

    def calculate_max_line(self):
        max_line = np.full(self.longest_log_len, np.NINF)

        for i in range(self.longest_log_len):
            for log in self.logs:
                if len(log) <= i:
                    continue
                m = log[i].mse
                if m > max_line[i]:
                    max_line[i] = m

        self.max_line = max_line


    def calculate_min_line(self):
        min_line = np.full(self.longest_log_len, np.inf)

        for i in range(self.longest_log_len):
            for log in self.logs:
                if len(log) <= i:
                    continue
                m = log[i].mse
                if m < min_line[i]:
                    min_line[i] = m

        self.min_line = min_line

    def calculate_mean_line(self):
        # Towards the end of the runs the number of data points available will not be equal to the
        # number of logs in this batch, so we keep track of the number of runs that have a datapoint
        # at each index so we can calculate the average precicely
        ns = np.zeros(self.longest_log_len)
        sums = np.zeros(self.longest_log_len)

        for i in range(self.longest_log_len):
            for log in self.logs:
                if len(log) <= i:
                    continue
                sums[i] += log[i].mse
                ns[i] += 1

        # Sanity check
        for i in ns:
            assert i > 0

        self.mean_line = np.true_divide(sums, ns)

class Plotter:

    def __init__(self):
        self.fig, self.ax = 0, 0
        self.reset()

    def set_yrange(self, mi, ma):
        self.ax.set_ylim(mi, ma)

    def set_xrange(self, mi, ma):
        self.ax.set_xlim(mi, ma)

    @staticmethod
    def set_font(family='normal', weight='normal', size=22):
        mpl.rc('font', **{'family': family, 'weight': weight, 'size': size})

    def reset(self):
        self.fig, self.ax = plt.subplots()

    def fix_legend(self):
        self.ax.legend()
        handles, labels = self.ax.get_legend_handles_labels()
        by_label = OrderedDict(zip(labels, handles))
        self.ax.get_legend().remove()
        self.ax.legend(by_label.values(), by_label.keys())

    def plot_log(self, log, color, label, start_time=0, truncate=None):
        if truncate is not None:
            t = list(range(start_time, min(len(log), truncate) + startime))
            self.ax.plot(t, log.query(lambda d: d.mse)[:truncate], color=color, label=label)
        else:
            t = list(range(start_time, len(log) + startime))
            self.ax.plot(t, log.query(lambda d: d.mse), color=color, label=label)

    def plot_all_logs(self, batch, color, label, start_time=0, truncate=None):
        for log in batch.logs:
            self.plot_log(log, color, label, start_time, truncate)

    def plot_batch(self, batch, color, label, show_min_max=True, start_time=0, truncate=None):
        if truncate is not None:
            t = list(range(start_time, min(batch.longest_log_len, truncate) + start_time))
            if show_min_max:
                self.ax.fill_between(t, batch.min_line[:truncate], batch.max_line[:truncate], alpha=0.25, color=color)
            self.ax.plot(t, batch.mean_line[:truncate], color=color, label=label)
        else:
            t = list(range(start_time, batch.longest_log_len + start_time))
            if show_min_max:
                self.ax.fill_between(t, batch.min_line, batch.max_line, alpha=0.25, color=color)
            self.ax.plot(t, batch.mean_line, color=color, label=label)
        
        self.fix_legend()

    def show(self):
        plt.show()
