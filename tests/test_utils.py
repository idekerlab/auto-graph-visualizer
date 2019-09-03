import unittest
from auto_graph_visualizer.utils import *
import ndex2
import os


class TestUtils(unittest.TestCase):
    def test_getCommunityEdge(self):
        testcx = ndex2.create_nice_cx_from_file(
            os.path.dirname(__file__)+'/test_cx/test.cx')
        v_community = [int(testcx.get_node_attribute_value(
            i, 'community')) for i in range(len(testcx.get_nodes()))]

        e_community = [int(testcx.get_edge_attribute_value(
            i, 'community')) for i in range(len(testcx.get_edges()))]

        # convert nice_cx -> pandas
        nice_cx_from_server_df = testcx.to_pandas_dataframe()

        # convert pandas -> igraph
        edgelist = nice_cx_from_server_df.iloc[:, [0, 2]]
        tuples = [tuple(x) for x in edgelist.values]
        g = igraph.Graph.TupleList(tuples, directed=False)

        self.assertEqual(e_community, getCommunityEdge(g, v_community))
        # self.assertListEqual([1, 2, 3, 4], getCommunityEdge(g, v_community))


if __name__ == '__main__':
    unittest.main()
