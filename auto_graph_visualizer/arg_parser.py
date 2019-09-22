# -*- coding: utf-8 -*-

import argparse


def get_args():
    parser = argparse.ArgumentParser(
        description='test argparse script')
    parser.add_argument('-n', '--name', default='',
                        type=str, help='This is output graph name.')
    parser.add_argument('-p', '--path', default='./',
                        type=str, help='This is output directory path')
    parser.add_argument('-a', '--algorithm', default='greedy', type=str,
                        choices=['greedy', 'eigenvec', 'labelprop', 'rest'],
                        help='This is community detection algorithm')
    parser.add_argument('-cp', '--colorpalette', default='hls', type=str,
                        choices=['hls', 'Accent', 'Set1', 'brg', 'hsv', 'gnuplot'],
                        help='This is color palette')
    parser.add_argument('-ns', '--nodesize', default='betweenness', type=str,
                        choices=['closeness', 'degree', 'pagerank', 'betweenness', 'diversity'],
                        help='This is standard of node size')
    parser.add_argument('-maxns', '--maxnodesize',
                        default=100, type=int, help='This is max node size')
    parser.add_argument('-d', '--density', default='normal', type=str,
                        choices=['dense', 'normal', 'sparse'],
                        help='This is density of output graph')
    parser.add_argument('-pos', '--positions', default='fa',
                        choices=['fa', 'kk'], help='This is layout algorithm')
    parser.add_argument('-dln', '--displaylabelnumber', default='20',
                        type=int, help='This is the number of display labels')
    return parser.parse_args()
