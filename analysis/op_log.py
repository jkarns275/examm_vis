import numpy as np
import csv
import matplotlib.pyplot as plt
import matplotlib as mpl
from collections import OrderedDict

class DataPoint:

    NODE_TYPES = [
        "simple",
        "jordan",
        "elman",
        "UGRNN",
        "MGU",
        "GRU",
        "LSTM",
        "delta",
    ]

    OP_LOG_ORDERING = [
        "genomes",
        "crossover",
        "island_crossover",
        "clone",
        "add_edge",
        "add_recurrent_edge",
        "enable_edge",
        "disable_edge",
        "enable_node",
        "disable_node",
    ]

    OPS_WITH_NODE_TYPE = [
        "add_node",
        "split_node",
        "merge_node",
        "split_edge",
    ]

    OP_LOG_HEADER = []

    OP_VAR_NAMES = []

    def __init__(self, *argv):
        assert len(argv) >= len(DataPoint.OP_VAR_NAMES)

        for name, value in zip(DataPoint.OP_VAR_NAMES, argv):
            self.__setattr__(name, value)

    def as_dict(self):
        d = {}
        for name in DataPoint.OP_VAR_NAMES:
            d[name] = self.__getattribute__(name)
        return d

    def __str__(self):
           return f"inserted genomes: {self.genomes}, bp_epochs: {self.bp_epochs}, " + \
                f"time: {self.time}, best mae: {self.mae}, best mse: {self.mse}, " + \
                f"enabled nodes: {self.nodes}, enabled edges: {self.edges}, " + \
                f"enabled recursive edges: {self.rec_edges}"

# Statically initialize DataPoint.OP_LOG_HEADER

for op in DataPoint.OPS_WITH_NODE_TYPE:
    for node_ty in DataPoint.NODE_TYPES:
        DataPoint.OP_LOG_ORDERING.append(f"{op}({node_ty})")

for op in DataPoint.OP_LOG_ORDERING:
    DataPoint.OP_LOG_HEADER.append(f"{op} Generated")
    DataPoint.OP_LOG_HEADER.append(f"{op} Inserted")

for op in DataPoint.OP_LOG_ORDERING:
    new_op: str = op.lower()
    new_op = new_op.replace("(", "_")
    new_op = new_op.replace(")", "")
    DataPoint.OP_VAR_NAMES.append(new_op)


class OperatorLog:

    def __init__(self, file_path, name, fold):
        # python csv docs say use newline='' of using a file object
        self.data = []
        self.name = name
        self.fold = fold

        try:
            with open(file_path, newline='') as csvfile:
                csv_reader = csv.reader(csvfile, delimiter=',')
                # verify that the header order matches the one we've computed here
                for row in csv_reader:
                    for i, label in enumerate(DataPoint.OP_LOG_HEADER):
                        row[i] = row[i].strip()
                        assert label == row[i].strip()
                    # break because we are only concerned with the header
                    break
                    
                for row in csv_reader:
                    dp = DataPoint(*row)
                    self.data.append(dp)

            self.valid = len(self.data) > 0
            if self.valid:
                self.breakthroughs = len(set(self.query(lambda l: l.mse)))
            print(f"{file_path} op log len: {len(self)}")        
        except Exception as e:
            if type(e) == AssertionError:
                raise e
            print("Oh")
            print(str(e))
            self.valid = False

    def display(self):
        # print(f"    fold {self.fold}: len={len(self)}; min_mse={min(self.query(lambda l: l.mse))}; breakthrough_count={self.breakthroughs}")
        pass

    def get_row_dict(self, index):
        dp = self.data[index]
        return dp.as_dict()

    def __getitem__(self, item):
        assert type(item) == int
        return self.data[item]

    def __len__(self):
        return len(self.data)

    def query(self, l):
        return list(map(l, self.data))



