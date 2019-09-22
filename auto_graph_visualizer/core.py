# -*- coding: utf-8 -*-
import logging
import sys
import json
from .arg_parser import get_args
from .visualizer import AutoGraphVisualizer

logging.basicConfig(level=logging.INFO)


def main():
    if sys.stdin.isatty():
        print("Usage: cat [Input CX file name] | agviz (Output CX file name)")
        sys.exit()

    args = get_args()
    logging.info('Argument parsed')

    # Output file name (optional)
    out_file = args.path + args.name

    # Load CX from STDIN
    cx_network = json.load(sys.stdin)
    logging.info('CX Loaded')

    options = {
        "graph_name": args.name,
        "output_file_name": out_file,
        "algorithm": args.algorithm,
        "color_palette": args.colorpalette,
        "nodesize": args.nodesize,
        "maxnodesize": args.maxnodesize,
        "density": args.density,
        "positions": args.positions,
        "displaylabels": args.displaylabelnumber
    }

    # Create visualizer instance
    viz = AutoGraphVisualizer(options)

    # Generate visualization
    cxobj = viz.generate_viz(cx_network)
    logging.info('Output CX created.')

    if args.name != None and args.name != '':
        logging.info('Output CX to file' + args.name)
        tmp = open(out_file + ".cx", 'w')
        json.dump(cxobj, tmp)
    else:
        logging.info('Output CX to STDOUT')
        json.dump(cxobj, sys.stdout, indent=2)
        logging.info('Done!!')
