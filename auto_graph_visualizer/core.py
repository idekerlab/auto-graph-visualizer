# -*- coding: utf-8 -*-
import sys
import json
from .utils import *
from .visualizer import AutoGraphVisualizer


def main():
    if(sys.stdin.isatty()):
        print("Usage: cat <file> | python3 graphvis.py")
        sys.exit()
    args = get_args()

    G_NAME = args.name
    SAVE_NAME = args.path + G_NAME
    ALGORITHM = args.algorithm
    COLORPALETTE = args.colorpalette
    NODE_SIZE = args.nodesize
    MAX_NODESIZE = args.maxnodesize
    DENSITY = args.density
    POSITIONS_ALG = args.positions

    cx_network = json.load(sys.stdin)

    options = {
        "graph_name": G_NAME,
        "output_file_name": SAVE_NAME,
        "algorithm": ALGORITHM,
        "color_palette": COLORPALETTE,
        "nodesize": NODE_SIZE,
        "maxnodesize": MAX_NODESIZE,
        "density": DENSITY,
        "positions": POSITIONS_ALG}

    # Create visualizer instance
    viz = AutoGraphVisualizer(options)

    # Generate visualization
    cxobj = viz.generate_viz(cx_network)

    tmp = open(SAVE_NAME+".cx", 'w')
    json.dump(cxobj, tmp)
