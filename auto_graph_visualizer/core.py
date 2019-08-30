# -*- coding: utf-8 -*-

import sys
import pandas as pd
import igraph
from ndex2.nice_cx_network import NiceCXNetwork
import ndex2.client as nc
import ndex2
import networkx as nx
from fa2 import ForceAtlas2
from utils import *
import json
import os


def graphvis():
    if(sys.stdin.isatty()):
        print("Usage: cat <file> | python3 graphvis.py")

    nice_cx_network = sys.stdin

    args = get_args()

    G_NAME = args.name
    SAVE_NAME = args.path + G_NAME
    ALGORITHM = args.algorithm

    # nice_cx_network = ndex2.create_nice_cx_from_server(server=SERVER, uuid=UUID)
    # show the graph detail
    nice_cx_network.print_summary()
    # convert nice_cx -> pandas
    nice_cx_from_server_df = nice_cx_network.to_pandas_dataframe()

    # convert pandas -> igraph
    edgelist = nice_cx_from_server_df.iloc[:, [0, 2]]
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

    communities_greedy = g.community_fastgreedy().as_clustering()
    communities_leading = g.community_leading_eigenvector()
    communities_label_propagation = g.community_label_propagation()

    v_community_greedy = communities_greedy.membership
    v_community_leading = communities_leading.membership
    v_community_label_propagation = communities_label_propagation.membership

    e_commnity_greedy = getCommunityEdge(g, v_community_greedy)
    e_commnity_leading = getCommunityEdge(g, v_community_leading)
    e_community_label_propagation = getCommunityEdge(
        g, v_community_label_propagation)

    # add color
    g.vs['color'] = communityToColors(communities_greedy.membership)
    g.es['color'] = communityToColors(e_commnity_greedy)

    # convert igraph -> networkx
    G_nx = nx.Graph()
    for i in range(g.vcount()):
        G_nx.add_node(g.vs['name'][i])
    for i, j in g.get_edgelist():
        G_nx.add_edge(g.vs['name'][i], g.vs['name'][j])

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
        scalingRatio=100,
        strongGravityMode=False,
        gravity=1500,

        # Log
        verbose=True)

    g.es['weights'] = [0 if i == -1 else 400 for i in e_commnity_greedy]
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
            i, "community.greedy", v_community_greedy[i])
        ncx_from_x.set_node_attribute(
            i, "community.leading", v_community_leading[i])
        ncx_from_x.set_node_attribute(
            i, "community.label.propagation", v_community_label_propagation[i])
        ncx_from_x.set_node_attribute(
            i, "colors.community.greedy", communityToColors(v_community_greedy)[i])
        ncx_from_x.set_node_attribute(
            i, "colors.community.leading", communityToColors(v_community_leading)[i])
        ncx_from_x.set_node_attribute(i, "colors.community.label.propagation", communityToColors(
            v_community_label_propagation)[i])

    for i in range(g.ecount()):
        ncx_from_x.set_edge_attribute(
            i, "betweenness.edge", g_es_betweenness[i])
        ncx_from_x.set_edge_attribute(
            i, "community.greedy", e_commnity_greedy[i])
        ncx_from_x.set_edge_attribute(
            i, "community.leading", e_commnity_leading[i])
        ncx_from_x.set_edge_attribute(
            i, "community.label.propagation", e_community_label_propagation[i])
        ncx_from_x.set_edge_attribute(
            i, "colors.community.greedy", communityToColors(e_commnity_greedy)[i])
        ncx_from_x.set_edge_attribute(
            i, "colors.community.leading", communityToColors(e_commnity_leading)[i])
        ncx_from_x.set_edge_attribute(i, "colors.community.label.propagation", communityToColors(
            e_community_label_propagation)[i])

    # add cytoscape visualization config
    with open(os.path.dirname(__file__)+'cy_visual.json') as f:
        cyconfig = json.load(f)
    ncx_from_x.set_opaque_aspect("cartesianLayout", certesian)
    ncx_from_x.set_opaque_aspect(
        "cyVisualProperties", cyconfig['cyVisualProperties'])

    cxobj = ncx_from_x.to_cx()

    tmp = open(SAVE_NAME+".cx", 'w')
    json.dump(cxobj, tmp)
    # print(cxobj)
