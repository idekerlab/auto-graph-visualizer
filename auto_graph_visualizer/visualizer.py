import pandas as pd
import igraph
from ndex2.nice_cx_network import NiceCXNetwork
import ndex2.client as nc
import ndex2
import networkx as nx
from fa2 import ForceAtlas2
from .utils import *
import math
import json
import os


class graph_status:
    def __init__(self, graph):
        self.graph = graph
        self.density = -1  # density
        self.transitivity_undirected = -1  # Transitivity
        self.closeness = -1  # Closeness Centrarity
        self.degree = -1  # Degree
        self.pagerank = -1  # PageRank
        self.vs_betweenness = -1  # Betweenness Centrarity
        self.es_betweenness = -1  # Edge Betweenness
        self.communities = []
        self.v_community = []
        self.e_community = []


class AutoGraphVisualizer:

    def __init__(self, options):
        self.options = options

    def generate_viz(self, cx_network):
        nice_cx_network = ndex2.create_nice_cx_from_raw_cx(cx_network)
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

        g_status = graph_status(
            largeset_subgraph.simplify(multiple=True, loops=True))

        self.__compute_stats(g_status.graph, g_status, self.options)

        positions = self.__apply_layout(g_status.graph, g_status, self.options)

        # convert igraph -> networkx
        G_nx = nx.Graph()
        for i in range(g_status.graph.vcount()):
            G_nx.add_node(g_status.graph.vs['name'][i])
        for i, j in g_status.graph.get_edgelist():
            G_nx.add_edge(g_status.graph.vs['name']
                          [i], g_status.graph.vs['name'][j])

        # convert position -> certesian
        certesian = [{'node': i, 'x': list(positions)[i][0], 'y': list(positions)[
            i][1]}for i in range(len(positions))]

        # convert networkx -> NiceCX
        ncx_from_x = ndex2.create_nice_cx_from_networkx(G_nx)

        self.__add_ncxattributes(ncx_from_x, g_status, certesian, self.options)

        cxobj = ncx_from_x.to_cx()

        return cxobj

    def __apply_layout(self, graph, g_status, options):
        ratio = graph.vcount()/100.0
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

        graph.es['weights'] = [0 if i == -
                               1 else math.sqrt(ratio)*15 for i in g_status.e_community]
        positions = forceatlas2.forceatlas2_igraph_layout(
            graph, pos=None, iterations=2000, weight_attr='weights')

        return positions

    def __compute_stats(self, graph, g_status, options):
        g_status.density = graph.density()  # density
        g_status.transitivity_undirected = graph.transitivity_undirected()  # Transitivity
        g_status.closeness = graph.vs.closeness()  # Closeness Centrarity
        g_status.degree = graph.vs.degree()  # Degree
        g_status.pagerank = graph.vs.pagerank(directed=False)  # PageRank
        g_status.vs_betweenness = graph.vs.betweenness()  # Betweenness Centrarity
        g_status.es_betweenness = graph.es.edge_betweenness()  # Edge Betweenness

        g_status.communities, g_status.v_community, g_status.e_community = get_communities(
            options["algorithm"], graph)

    def __add_ncxattributes(self, ncx, g_status, certesian, options):
        for i in range(g_status.graph.vcount()):
            ncx.set_node_attribute(i, "closeness", g_status.closeness[i])
            ncx.set_node_attribute(i, "degree", g_status.degree[i])
            ncx.set_node_attribute(i, "pagerank", g_status.pagerank[i])
            ncx.set_node_attribute(
                i, "betweenness", g_status.vs_betweenness[i])
            ncx.set_node_attribute(
                i, "community", g_status.v_community[i])
            ncx.set_node_attribute(
                i, "colors_community", communityToColors(options["color_palette"], g_status.v_community)[i])

        for i in range(g_status.graph.ecount()):
            ncx.set_edge_attribute(
                i, "betweenness_edge", g_status.es_betweenness[i])
            ncx.set_edge_attribute(
                i, "community", g_status.e_community[i])
            ncx.set_edge_attribute(
                i, "colors_community", communityToColors(options["color_palette"], g_status.e_community)[i])

        # add cytoscape visualization config
        with open(os.path.dirname(__file__)+'/cy_visual.json') as f:
            cyconfig = json.load(f)
        ncx.set_opaque_aspect("cartesianLayout", certesian)
        ncx.set_opaque_aspect(
            "cyVisualProperties", cyconfig['cyVisualProperties'])
