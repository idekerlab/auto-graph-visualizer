# -*- coding: utf-8 -*-

import argparse
import sys
import igraph
import seaborn as sns


def get_args():
    parser = argparse.ArgumentParser(
        description='test argparse script')
    parser.add_argument('-n', '--name', default='test_out',
                        type=str, help='This is output graph name.')
    parser.add_argument('-p', '--path', default='./',
                        type=str, help='This is output directory path')
    parser.add_argument('-a', '--algorithm', default='greedy', type=str,
                        choices=['greedy', 'eigenvec', 'labelprop', 'rest'], help='This is community detection algorithm')
    parser.add_argument('-cp', '--colorpalette', default='hls', type=str,
                        choices=['hls', 'Accent', 'Set1', 'brg', 'hsv', 'gnuplot'], help='This is color palette')
    parser.add_argument('-ns', '--nodesize', default='betweenness', type=str,
                        choices=['closeness', 'degree', 'pagerank', 'betweenness', 'diversity'], help='This is standard of node size')
    parser.add_argument('-maxns', '--maxnodesize',
                        default=1000000, type=int, help='This is max node size')
    parser.add_argument('-d', '--density', default='normal', type=str,
                        choices=['dense', 'normal', 'sparse'], help='This is density of output graph')
    parser.add_argument('-pos', '--positions', default='fa',
                        choices=['fa', 'kk'], help='This is layout algorithm')
    return parser.parse_args()


def getCommunityEdge(g, community):
    num_edges = g.ecount()
    edge_community = [-1]*num_edges
    comms = community
    sources = [i for i, _ in g.get_edgelist()]
    targets = [j for _, j in g.get_edgelist()]
    for i in range(num_edges):
        sidx = sources[i]
        tidx = targets[i]
        source = comms[sidx]
        target = comms[tidx]

        if source == target:
            edge_community[i] = source
    return edge_community


def communityToColors(cp, members):
    basecolor = '#AAAAAA'
    num_members = len(members)
    num_communities = max(members)+1
    colors = [basecolor]*num_members

    colorp = sns.color_palette(cp, num_communities)

    colorpalette = [rgb2hex(int(a[0]*255), int(a[1]*255),
                            int(a[2]*255)) for a in colorp]

    for i in range(num_members):
        newcolor = colorpalette[members[i]]
        if(members[i] == -1):
            newcolor = basecolor
        colors[i] = newcolor
    return colors


def rgb2hex(r, g, b):
    color = (r, g, b)
    html_color = '#%02X%02X%02X' % (color[0], color[1], color[2])
    return html_color


def communities_from_clusterfile(data):

    community = {}
    for line in data.split(';'):
        slist = line.split(',')
        if len(slist) != 3:
            #sys.stderr.write(line + ' does not have appropriate number of columns. skipping\n')
            continue

        if slist[2].startswith('c-m'):
            community.update({int(slist[1]): int(slist[0])})
    communities = [community[i] for i in range(len(community))]

    return communities


def get_communities(algo, g, rest_output=None):
    communities = []
    v_community = []
    e_community = []

    if algo == 'greedy':
        communities = g.community_fastgreedy().as_clustering()
        v_community = communities.membership
        e_community = getCommunityEdge(g, v_community)

    elif algo == 'eigenvec':
        communities = g.community_leading_eigenvector()
        v_community = communities.membership
        e_community = getCommunityEdge(g, v_community)

    elif algo == 'labelprop':
        communities = g.community_label_propagation()
        v_community = communities.membership
        e_community = getCommunityEdge(g, v_community)
    else:
        communities = communities_from_clusterfile(rest_output)
        v_community = communities
        e_community = getCommunityEdge(g, v_community)

    return communities, v_community, e_community
