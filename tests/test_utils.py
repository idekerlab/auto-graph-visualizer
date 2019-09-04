import unittest
from auto_graph_visualizer.utils import *
import ndex2
import os
import glob


class TestUtils(unittest.TestCase):
    def test_getCommunityEdge(self):
        filelist = glob.glob(os.path.dirname(__file__)+'/test_cx/*')
        for a in filelist:
            testcx= ndex2.create_nice_cx_from_file(a)
            # convert nice_cx -> pandas
            nice_cx_df = testcx.to_pandas_dataframe()
        
            # convert pandas -> igraph
            edgelist = nice_cx_df.iloc[:, [0, 2]]
            tuples = [tuple(x) for x in edgelist.values]
            g = igraph.Graph.TupleList(tuples, directed=False)

            # Pick largest subgraph
            subgraphs = g.decompose()
            tmp = [i.vcount() for i in subgraphs]
            largeset_subgraph = subgraphs[tmp.index(max(tmp))]
            g = largeset_subgraph.simplify(multiple=True, loops=True)

            # Match two different labels

            source_node_name_list= [value['n'] for key,value in list(testcx.get_nodes())]
            node_id_list = []
            for a in g.vs['name']:
                for i , b in enumerate (source_node_name_list):
                    if a==b:
                        node_id_list.append(i)
        
            v_community = [int(testcx.get_node_attribute_value(a, 'community')) for a in node_id_list]

            source_edge_list= [(node_id_list.index(value['s']),node_id_list.index(value['t'])) for key,value in list(testcx.get_edges())]

            edge_id_list = []
            for a in g.get_edgelist():
                for i , b in enumerate (source_edge_list):
                    if sorted(a)==sorted(b):
                        edge_id_list.append(i)
        
            e_community = [int(testcx.get_edge_attribute_value(a, 'community')) for a in edge_id_list]

            self.assertEqual(e_community, getCommunityEdge(g, v_community))
            # self.assertListEqual([1, 2, 3, 4], getCommunityEdge(g, v_community))

    def test_communityToColors(self):
        filelist=glob.glob(os.path.dirname(__file__)+'/test_cx/*')
        for a in filelist:
            testcx_out = ndex2.create_nice_cx_from_file(a)

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
