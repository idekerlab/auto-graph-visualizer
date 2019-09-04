import unittest
from auto_graph_visualizer.utils import *
import ndex2
import os


class TestUtils(unittest.TestCase):
    def test_getCommunityEdge(self):
        testcx_in = ndex2.create_nice_cx_from_file(
            os.path.dirname(__file__)+'/test_cx/test1_in.cx')
        testcx_out = ndex2.create_nice_cx_from_file(
            os.path.dirname(__file__)+'/test_cx/test1_out.cx')

        v_community = [int(testcx_out.get_node_attribute_value(
            i, 'community')) for i in range(len(testcx_out.get_nodes()))]

        e_community = [int(testcx_out.get_edge_attribute_value(
            i, 'community')) for i in range(len(testcx_out.get_edges()))]

        # convert nice_cx -> pandas
        nice_cx_df = testcx_in.to_pandas_dataframe()
        nice_cx_df = nice_cx_df.sort_values(
            by=([nice_cx_df.columns[0], nice_cx_df.columns[2]]))

        # convert pandas -> igraph
        edgelist = nice_cx_df.iloc[:, [0, 2]]
        tuples = [tuple(x) for x in edgelist.values]
        g = igraph.Graph.TupleList(tuples, directed=False)

        # Pick largest subgraph
        subgraphs = g.decompose()
        tmp = [i.vcount() for i in subgraphs]
        largeset_subgraph = subgraphs[tmp.index(max(tmp))]
        g = largeset_subgraph.simplify(multiple=True, loops=True)

        self.assertEqual(e_community, getCommunityEdge(g, v_community))
        # self.assertListEqual([1, 2, 3, 4], getCommunityEdge(g, v_community))

    def test_communityToColors(self):
        testcx_out = ndex2.create_nice_cx_from_file(
            os.path.dirname(__file__)+'/test_cx/test1_out.cx')

        v_color = [str(testcx_out.get_node_attribute_value(
            i, 'colors_community')) for i in range(len(testcx_out.get_nodes()))]

        e_color = [str(testcx_out.get_edge_attribute_value(
            i, 'colors_community')) for i in range(len(testcx_out.get_edges()))]

        v_community = [int(testcx_out.get_node_attribute_value(
            i, 'community')) for i in range(len(testcx_out.get_nodes()))]

        e_community = [int(testcx_out.get_edge_attribute_value(
            i, 'community')) for i in range(len(testcx_out.get_edges()))]

        self.assertEqual(v_color, communityToColors('hls', v_community))
        self.assertEqual(e_color, communityToColors('hls', e_community))


if __name__ == '__main__':
    unittest.main()
