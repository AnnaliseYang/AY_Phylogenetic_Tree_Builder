import numpy as np
import networkx as nx
# import sequences_file as sf
import graph_tree_node as gtn
import species as bs

class TreeGraph( gtn.Tree ):

    def tree_to_graph(self):
        graph = nx.DiGraph()

        def __graph_add_node(node):
            id = node.get_id()

            graph.add_node(id, color='mediumaquamarine' if node.is_leaf() else ( 'lightsteelblue' if node.is_root() else '#c2a3a3' ) )

            for i, child in enumerate( node.get_children() ):
                weight = child.get_data("weight")
                if weight != None:
                    graph.add_edge(id, child.get_id(), dir = 'left' if i == 0 else 'right', weight = round(weight, 3))
                else:
                    graph.add_edge(id, child.get_id(), dir = 'left' if i == 0 else 'right')

                __graph_add_node(child)

        root = super().get_root()
        __graph_add_node(root)
        return graph, root.get_id()


    def position(graph, root_id):
        '''
        returns the position dictionary of a graph with a specified root node
        '''

        G = graph
        queue = set(graph) - {root_id}
        print('QUEUE:', queue)
        pos = {}

        pos[root_id] = np.array([0, 0])  # manually specify node position at the root

        theta = 90
        R = np.array([[np.math.sin(theta), -np.math.cos(theta)], [np.math.sin(theta), np.math.cos(theta)]], np.int32)
        print('ROTATION MATRIX:', R)

        while len(pos) < len(set(G)):
            for n in queue:
                height = nx.shortest_path_length(G, root_id, n) # distance from the root to the current node
                k = 0.9**height # scaling factor based on node height
                predecessors = list(nx.DiGraph.predecessors(G, n))

                for parent in predecessors:
                    if parent in pos:

                        shift_l = np.array([-0.3 * (k**3), -0.5])
                        shift_r = np.array([0.3  * (k**3), -0.5])

                        if nx.DiGraph.get_edge_data(G, parent, n)['dir'] == 'left':
                            pos[n] = pos[parent] + shift_l
                        else:
                            pos[n] = pos[parent] + shift_r

        return pos

        # for node in tree_map:
        #     if 'P' in node.get_value():
        #         tree.add_node(node.get_value(), color = '#c2a3a3')
        #     else:
        #         tree.add_node(node.get_value(), color = 'mediumaquamarine')

        # for node in tree_map:
        #     parent = node.get_value()
        #     left_child = node.get_left_child().get_value()
        #     right_child = node.get_right_child().get_value()

        #     if left_child != None:
        #         dist = round(sf.avg_dist(sf.get_seq(node.get_value()), sequences_file.get_seq(left_child)), 2)
        #         # print('^^^^^^^^^^^^^^', f'EDGE BETWEEN {parent} AND LEFT CHILD {left_child}:', dist)
        #         tree.add_edge(parent, left_child, dir = 'left', weight = dist)
        #     if right_child != None:
        #         dist = round(sequences_file.avg_dist(sequences_file.get_seq(node.get_value()), sequences_file.get_seq(right_child)), 2)
        #         # print('^^^^^^^^^^^^^^', f'EDGE BETWEEN {parent} AND RIGHT CHILD {right_child}:', dist)
        #         tree.add_edge(parent, right_child, dir = 'right', weight = dist)
