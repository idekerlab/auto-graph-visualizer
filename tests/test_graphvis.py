import pandas as pd
import igraph
from ndex2.nice_cx_network import NiceCXNetwork
import ndex2.client as nc
import ndex2
import networkx as nx
from fa2 import ForceAtlas2
from . import utils

SERVER = 'public.ndexbio.org'
UUID = '0dcb39d6-43b6-11e6-a5c7-06603eb7f303'


if __name__ == '__main__':
    nice_cx_network = ndex2.create_nice_cx_from_server(
        server=SEVER, uuid=UUID)
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
