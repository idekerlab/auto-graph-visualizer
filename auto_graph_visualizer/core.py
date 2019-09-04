# -*- coding: utf-8 -*-

import sys
import pandas as pd
import igraph
from ndex2.nice_cx_network import NiceCXNetwork
import ndex2.client as nc
import ndex2
import networkx as nx
from fa2 import ForceAtlas2
from .utils import *
import json
import os
import math


def main():
    if(sys.stdin.isatty()):
        print("Usage: cat <file> | python3 graphvis.py")
        sys.exit()
    cx_network = json.load(sys.stdin)
    nice_cx_network = ndex2.create_nice_cx_from_raw_cx(cx_network)
    args = get_args()

    G_NAME = args.name
    SAVE_NAME = args.path + G_NAME
    ALGORITHM = args.algorithm
    COLORPALETTE = args.colorpalette
    # nice_cx_network = ndex2.create_nice_cx_from_server(server=SERVER, uuid=UUID)
    # show the graph detail
    nice_cx_network.print_summary()
    # convert nice_cx -> pandas
    nice_cx_df = nice_cx_network.to_pandas_dataframe()
    nice_cx_df = nice_cx_df.sort_values(
        by=([nice_cx_df.columns[0], nice_cx_df.columns[2]]))

    # convert pandas -> igraph
    edgelist = nice_cx_df.iloc[:, [0, 2]]
    tuples = [tuple(x) for x in edgelist.values]
    g_original = igraph.Graph.TupleList(tuples, directed=False)

    # Pick largest subgraph
    subgraphs = g_original.decompose()
    tmp = [i.vcount() for i in subgraphs]
    largeset_subgraph = subgraphs[tmp.index(max(tmp))]

    g = largeset_subgraph.simplify(multiple=True, loops=True)

    g.name = G_NAME

    # analysis

    """
        g_density = g.density() #density
        g_transitivity_undirected = g.transitivity_undirected() #Transitivity
        """
    g_closeness = g.vs.closeness()  # Closeness Centrarity
    g_degree = g.vs.degree()  # Degree
    g_pagerank = g.vs.pagerank(directed=False)  # PageRank
    g_vs_betweenness = g.vs.betweenness()  # Betweenness Centrarity
    g_es_betweenness = g.es.edge_betweenness()  # Edge Betweenness

    communities, v_community, e_community = get_communities(ALGORITHM, g)

    # add color
    g.vs['color'] = communityToColors(COLORPALETTE, communities.membership)
    g.es['color'] = communityToColors(COLORPALETTE, e_community)

    # convert igraph -> networkx
    G_nx = nx.Graph()
    for i in range(g.vcount()):
        G_nx.add_node(g.vs['name'][i])
    for i, j in g.get_edgelist():
        G_nx.add_edge(g.vs['name'][i], g.vs['name'][j])

    ratio = g.vcount()/100.0
    # add position
    forceatlas2 = ForceAtlas2(
        # Behavior alternatives
        outboundAttractionDistribution=True,  # Dissuade hubs
        linLogMode=False,  # NOT IMPLEMENTED
        adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
        edgeWeightInfluence=1.0,

        # Performance
        jitterTolerance=1.0,  # Tolerance
        barnesHutOptimize=True,
        barnesHutTheta=1.2,
        multiThreaded=False,  # NOT IMPLEMENTED

        # Tuning
        scalingRatio=math.sqrt(ratio) * 4,
        strongGravityMode=False,
        gravity=ratio * 25,

        # Log
        verbose=True)

    g.es['weights'] = [0 if i == -
                       1 else math.sqrt(ratio)*15 for i in e_community]
    positions = forceatlas2.forceatlas2_igraph_layout(
        g, pos=None, iterations=2000, weight_attr='weights')

    # convert position -> certesian
    certesian = [{'node': i, 'x': list(positions)[i][0], 'y': list(positions)[
        i][1]}for i in range(len(positions))]

    # convert networkx -> Nicex
    ncx_from_x = ndex2.create_nice_cx_from_networkx(G_nx)

    # add atributes
    for i in range(g.vcount()):
        ncx_from_x.set_node_attribute(i, "closeness", g_closeness[i])
        ncx_from_x.set_node_attribute(i, "degree", g_degree[i])
        ncx_from_x.set_node_attribute(i, "pagerank", g_pagerank[i])
        ncx_from_x.set_node_attribute(i, "betweenness", g_vs_betweenness[i])
        ncx_from_x.set_node_attribute(
            i, "community", v_community[i])
        ncx_from_x.set_node_attribute(
            i, "colors_community", communityToColors(COLORPALETTE, v_community)[i])

    for i in range(g.ecount()):
        ncx_from_x.set_edge_attribute(
            i, "betweenness_edge", g_es_betweenness[i])
        ncx_from_x.set_edge_attribute(
            i, "community", e_community[i])
        ncx_from_x.set_edge_attribute(
            i, "colors_community", communityToColors(COLORPALETTE, e_community)[i])

    # add cytoscape visualization config
    with open(os.path.dirname(__file__)+'/cy_visual.json') as f:
        cyconfig = json.load(f)
    ncx_from_x.set_opaque_aspect("cartesianLayout", certesian)
    ncx_from_x.set_opaque_aspect(
        "cyVisualProperties", cyconfig['cyVisualProperties'])

    cxobj = ncx_from_x.to_cx()

    tmp = open(SAVE_NAME+".cx", 'w')
    json.dump(cxobj, tmp)
