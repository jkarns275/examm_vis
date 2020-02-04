import sys

import json

import matplotlib
import matplotlib.pyplot as plt
from random import shuffle

class Config:

    RESULTS_DIR = "RESULTS_DIR"

    def __init__(self):
        import argparse
    
        parser = argparse.ArgumentParser(prog='examm_vis')
        parser.add_argument('cfg_path', metavar="CONFIG_FILE_PATH", type=str,
                            help="The location of the json file which contains the groups and the results directory.")
        parser.add_argument('groups', metavar='GROUP_NAME[:time_lag][:truncate]', type=str, nargs='*', 
                help="The name of a group to be graphed. You can optionally specify a time lag - i.e. what genome number should the curves begin for this group. You can optionally specify how long this log can be at most (truncate).")

        parser.add_argument('-o', metavar='IMAGE_DEST', nargs=1, type=str,
                help="If this is specified, the interactive window will not open and an image will be saved at the specified path.")
        parser.add_argument('-d', metavar='WIDTHxHEIGHT', type=str, 
                help="If this is specified and IMAGE_DEST is not defined, the interactive window will have the specified dimensions. If it is specified, then the resulting image will have these dimensions.")
        parser.add_argument('-t', metavar='TITLE', type=str,default='default_title', action='store',
                help='The title for the plot')
        args = parser.parse_args()
        self.width, self.height = 640, 480 if args.d is None else tuple(map(int, args.d.lower().split('x')))
        self.interactive = args.o is None
        self.title = args.t
        self.img_path = args.o
        self.to_plot = []
        
        for group in args.groups:
            if ':' in group:
                r = group.split(':')
                if len(r) == 2:
                    name, delay = r
                    delay = int(delay)
                    self.to_plot.append((name, delay, None))
                else:
                    name, delay, truncate = r
                    self.to_plot.append((name, int(delay), int(truncate)))
            else:
                self.to_plot.append((group, 0, None))
        
        cfg_path = args.cfg_path
        
        with open(cfg_path) as f:
            text = f.read()
        cfg_obj = json.loads(text)
        
        assert Config.RESULTS_DIR in cfg_obj, f"\"{config.RESULTS_DIR}\" must be specified in the config file."

        self.results_dir = cfg_obj.pop(Config.RESULTS_DIR)
        assert type(self.results_dir) == str, f"\"{Config.RESULTS_DIR}\" must be a string."

        self.groups = cfg_obj

        self.validate_groups()
        
    def validate_groups(self):
        assert len(self.groups) > 0, "You must specify at least one group."
        for name, members in self.groups.items():
            assert " " not in name, "Group names must not have spaces."
            assert type(members) == dict
            self.validate_members(members)

    def validate_members(self, members):
        assert len(members) > 0
        import os
        for mname, mpath in members.items():
            assert type(mpath) == str, f"Group member named {mname} does not have a string path."
            if not os.path.isdir(f"{self.results_dir}/{mpath}"):
                print(f"WARNING: folder {self.results_dir}/{mpath} does not exist")
