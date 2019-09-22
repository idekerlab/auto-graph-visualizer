# -*- coding: utf-8 -*-

import logging
import argparse
import sys
import seaborn as sns


class UnionFind:

    """Find union utility"""

    def __init__(self, n):
        # negative : root
        # non-negative : rank
        self.table = [-1] * n

    def _root(self, x):
        if self.table[x] < 0:
            return x
        else:
            self.table[x] = self._root(self.table[x])
            return self.table[x]

    def find(self, x, y):
        return self._root(x) == self._root(y)

    def unite(self, x, y):
        r1 = self._root(x)
        r2 = self._root(y)
        if r1 == r2:
            return
        d1 = self.table[r1]
        d2 = self.table[r2]
        if d1 <= d2:
            self.table[r2] = r1
            if d1 == d2:
                self.table[r1] -= 1
        else:
            self.table[r1] = r2



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


def setCommunityColors(cp, members):
    num_members = len(members)
    unique_communities = list(set(members))
    num_communities = len(unique_communities)
    d_colors = {-1: '#AAAAAA'}

    colorp = sns.color_palette(cp, num_communities)

    colorpalette = [rgb2hex(int(a[0]*255), int(a[1]*255),
                            int(a[2]*255)) for a in colorp]

    for i, communityname in enumerate(unique_communities):
        d_colors[communityname] = colorpalette[i]
    return d_colors


def communityToColors(colors, members):
    num_members = len(members)
    l_colors = ["#AAAAAA"]*num_members
    for i in range(num_members):
        l_colors[i] = colors[members[i]]
    return l_colors


def rgb2hex(r, g, b):
    color = (r, g, b)
    html_color = '#%02X%02X%02X' % (color[0], color[1], color[2])
    return html_color


def communities_from_clusterfile(data, rank=1):
    hierarchy = 0
    clist = []
    flag = True
    node_list = set()
    UF = UnionFind(int(data.split(';')[-2].split(',')[0]))
    for line in reversed(data.split(';')):
        slist = line.split(',')
        if len(slist) != 3:
            continue
        if slist[0] in clist:
            hierarchy += 1
            clist.clear()
        else:
            clist.append(slist[1])
        if slist[2].startswith('c-m'):
            node_list.add(int(slist[1]))
        if hierarchy >= rank:
            UF.unite(int(slist[0]), int(slist[1]))
    if hierarchy < rank:
        print("Your rank is larger than hierarchy\n")
        sys.exit()
    return [UF._root(i) for i in range(len(node_list))]


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
