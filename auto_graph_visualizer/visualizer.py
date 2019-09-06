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
import numpy as np


class graph_status:
    def __init__(self, graph):
        self.graph = graph
        self.communities = []
        self.v_community = []
        self.e_community = []

    """

    def calc_closeness(self):
        self.closeness = self.graph.vs.closeness()  # Closeness Centrarity

    def calc_degree(self):
        self.degree = self.graph.vs.degree()  # Degree

    def calc_pagerank(self):
        self.pagerank = self.graph.vs.pagerank(directed=False)  # PageRank

    def calc_betweenness(self):
        self.betweenness = self.graph.vs.betweenness()  # Betweenness Centrarity
    """


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

        self.__compute_stats(g_status, self.options)

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
<<<<<<< HEAD
        if options["kamada_kawai"]:
            if options["density"] == "normal":
                c = 70
            elif options["density"] == "dense":
                c = 30
            else:
                c = 140
            positions = graph.layout_kamada_kawai()
            positions = np.array(positions) * c
            return positions
        else:
            ratio = graph.vcount()/100.0
            if options["density"] == "normal":
                c = 4
            elif options["density"] == "dense":
                c = 1
            else :
                c = 16
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
                scalingRatio=math.sqrt(ratio) * c,
                strongGravityMode=False,
                gravity=ratio * 25,
                # Log
                verbose=True)

            graph.es['weights'] = [0 if i == -
                                1 else math.sqrt(ratio)*15 for i in g_status.e_community]
            positions = forceatlas2.forceatlas2_igraph_layout(
                graph, pos=None, iterations=2000, weight_attr='weights')

            return positions
=======
        ratio = graph.vcount()/100.0
        if options["density"] == "normal":
            c = 4
        elif options["density"] == "dense":
            c = 1
        else:
            c = 16
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
            scalingRatio=math.sqrt(ratio) * c,
            strongGravityMode=False,
            gravity=ratio * 25,
            # Log
            verbose=True)

        graph.es['weights'] = [0 if i == -
                               1 else math.sqrt(ratio)*15 for i in g_status.e_community]
        positions = forceatlas2.forceatlas2_igraph_layout(
            graph, pos=None, iterations=2000, weight_attr='weights')

        return positions
>>>>>>> b43a0dcdcd8ff1273e8f5161860f83daf3445379

    def __compute_stats(self, g_status, options):
        # g_status.density = graph.density()  # density
        # g_status.transitivity_undirected = graph.transitivity_undirected()  # Transitivity
        setattr(g_status, options['nodesize'], getattr(
            g_status.graph, options['nodesize'])())
        g_status.communities, g_status.v_community, g_status.e_community = get_communities(
            options["algorithm"], g_status.graph)

    def __add_ncxattributes(self, ncx, g_status, certesian, options):
        colors = communityToColors(
            options["color_palette"], g_status.v_community)

        for i in range(g_status.graph.vcount()):
            ncx.set_node_attribute(
                i, options['nodesize'], getattr(g_status, options['nodesize'])[i])
            ncx.set_node_attribute(
                i, "community", g_status.v_community[i])
            ncx.set_node_attribute(
                i, "colors_community", colors[i])

        colors = communityToColors(
            options["color_palette"], g_status.e_community)

        for i in range(g_status.graph.ecount()):
            ncx.set_edge_attribute(
                i, "community", g_status.e_community[i])
            ncx.set_edge_attribute(
                i, "colors_community", colors[i])

        # add cytoscape visualization config
        with open(os.path.dirname(__file__)+'/cy_visual.json') as f:
            cyconfig = json.load(f)
        self.__change_nodesize(g_status, cyconfig, self.options)
        ncx.set_opaque_aspect("cartesianLayout", certesian)
        ncx.set_opaque_aspect(
            "cyVisualProperties", cyconfig['cyVisualProperties'])

    def __change_nodesize(self, g_status, cyconfig, options):
        nodesizeprop = cyconfig['cyVisualProperties'][1]['mappings']['NODE_SIZE']['definition']
        nodesizeprop = nodesizeprop.split(',')
        tmp = nodesizeprop[0].split('=')
        tmp[1] = options['nodesize']
        tmp = '='.join(tmp)
        nodesizeprop[0] = tmp
        tmp = nodesizeprop[9].split('=')
        tmp[2] = str(int(options['maxnodesize']))
        tmp = '='.join(tmp)
        nodesizeprop[9] = tmp
        nodesizeprop = ','.join(nodesizeprop)
        print(nodesizeprop)
        cyconfig['cyVisualProperties'][1]['mappings']['NODE_SIZE']['definition'] = nodesizeprop
