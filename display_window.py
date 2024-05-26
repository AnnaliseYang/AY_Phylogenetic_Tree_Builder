import PySimpleGUI as sg
import numpy as np
import graph_tree_node as gtn
import species as bs

'''
class TreeLayoutBase
'''
class TreeLayoutBase:
    NODE_RADIUS = 18
    NODE_FONT = ( 'Helvetica', 10, 'bold')
    NODE_COLOR = "#c7adb8"
    NODE_COLOR_LEAF = "mediumaquamarine"
    NODE_COLOR_ROOT = "#b26282"
    NODE_COLOR_TEXT = "black"
    EDGE_WIDTH = 2
    EDGE_COLOR = "lightsteelblue"
    EDGE_LABLE_FONT = ( 'Helvetica', 10, 'normal')
    EDGE_LABLE_COLOR = EDGE_COLOR

    def __init__(self, width, height, graph):
        self.__width = width
        self.__height = height
        self.__graph = graph

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def graph(self):
        return self.__graph

    def draw_node_one(self, node, location, location_parent = None):
        if location_parent != None:
            self.__graph.draw_line(location, location_parent, color=self.EDGE_COLOR, width=self.EDGE_WIDTH)
            weight = node.get_data('weight')
            if weight != None:
                x = ( location[0] + location_parent[0] ) / 2
                y = ( location[1] + location_parent[1] ) / 2
                angle = np.rad2deg( np.arctan2(location[1] - location_parent[1], location_parent[0] - location[0]) )
                if location_parent[0] < location[0]:
                    angle += 180

                # Draw Edge Lable
                self.__graph.draw_text(
                    "{:0.3f}".format(weight),
                    (x, y),
                    color = self.EDGE_LABLE_COLOR,
                    font = self.EDGE_LABLE_FONT,
                    angle = angle,
                    text_location = sg.TEXT_LOCATION_BOTTOM )

        color = self.NODE_COLOR_LEAF if node.is_leaf() else self.NODE_COLOR_ROOT if node.is_root() else self.NODE_COLOR

        self.__graph.draw_circle(
            location,
            self.NODE_RADIUS,
            fill_color = color,
            line_color = color)

        self.__graph.draw_text(
            f"{node.get_id()}",
            location,
            color= self.NODE_COLOR_TEXT,
            font= self.NODE_FONT )

#######################################################################################################################
'''
class TreeLayoutA
'''
class TreeLayoutA( TreeLayoutBase ):

    def __init__(self, width, height, graph):
        super().__init__(width, height, graph)
        self.NODE_DX = super().NODE_RADIUS * 1.1
        self.NODE_DY = super().NODE_RADIUS * 4


    def __draw_node(self, node, location, depth, parent_location = None):
        for i, node_child in enumerate( node.get_children() ):
            x = location[0] + ( ( 2 ** ( depth - 2 ) ) * self.NODE_DX ) * ( i * 2 - 1 )
            y = location[1] + self.NODE_DY
            self.__draw_node(node_child, (x, y), (depth - 1), location)
        super().draw_node_one(node, location, parent_location)


    def draw_tree(self, tree, location ):
        node_root = None if tree == None else tree.get_root()
        if self.graph != None and node_root != None:
            self.__draw_node(node_root, location, node_root.get_depth() )

    ###########################################################################################################

    def __calculate_node_location(self, box, node, location, depth, parent_location = None):
        for i, node_child in enumerate( node.get_children() ):
            x = location[0] + ( ( 2 ** ( depth - 2 ) ) * self.NODE_DX ) * ( i * 2 - 1 )
            y = location[1] + self.NODE_DY
            self.__calculate_node_location(box, node_child, (x, y), depth - 1, location)
        box[0] = min( box[0], location[0] )
        box[1] = min( box[1], location[1] )
        box[2] = max( box[2], location[0] )
        box[3] = max( box[3], location[1] )


    def calculate_best_tree_location(self, tree):
        assert tree != None
        box = [0, 0, 0, 0]
        node_root = tree.get_root()
        if node_root != None:
            self.__calculate_node_location(box, node_root, (0, 0), node_root.get_depth())
        return ( super().width - (box[0] + box[2]) ) / 2, ( super().height - (box[1] + box[3]) ) / 2

#######################################################################################################################
'''
class TreeLayoutB
'''
class TreeLayoutB( TreeLayoutBase ):
    NODE_RADIUS = 18
    NODE_RADIUS_BIG = 18
    NODE_ANGLE= ( 3.1415926536 / 6.0 )
    NODE_ANGLE2= NODE_ANGLE * 2
    NODE_LINE_LENGTH = 130
    NODE_LINE_LENGTH_RATIO = 0.9
    NODE_ANGLE_RATIO = 0.9

    def __init__(self, width, height, graph):
        super().__init__(width, height, graph)

    def __draw_node(self, node, location, line_length, angle, location_parent = None, angle_parent = 0.0):
        children_count = node.get_children_count()

        if children_count > 0 :
            angle_child = angle_parent - angle * ( children_count - 1.0 )

            for node_chile in node.get_children():
                self.__draw_node(
                    node_chile,
                    ( location[0] + ( line_length * np.sin(angle_child) ), location[1] + ( line_length * np.cos(angle_child)) ),
                    line_length * self.NODE_LINE_LENGTH_RATIO,
                    angle * self.NODE_ANGLE_RATIO,
                    location,
                    angle_child)

                angle_child += ( angle * 2.0 )

        super().draw_node_one(node, location, location_parent)


    def draw_tree(self, tree, location ):
        node_root = None if tree == None else tree.get_root()
        if self.graph != None and node_root != None:
            self.__draw_node(node_root, location, self.NODE_LINE_LENGTH, self.NODE_ANGLE )

    ###########################################################################################################

    def __calculate_node_location(self, box, node, location, line_length, angle, angle_parent = 0.0):
        children_count = node.get_children_count()

        if children_count > 0 :
            angle_child = angle_parent - angle * ( children_count - 1.0 )

            for node_chile in node.get_children():
                self.__calculate_node_location(
                    box,
                    node_chile,
                    ( location[0] + ( line_length * np.sin(angle_child) ), location[1] + ( line_length * np.cos(angle_child)) ),
                    line_length * self.NODE_LINE_LENGTH_RATIO,
                    angle * self.NODE_ANGLE_RATIO,
                    angle_child)

                angle_child += ( angle * 2.0 )

        box[0] = min( box[0], location[0] )
        box[1] = min( box[1], location[1] )
        box[2] = max( box[2], location[0] )
        box[3] = max( box[3], location[1] )


    def calculate_best_tree_location(self, tree):
        assert tree != None
        box = [ 0, 0, 0, 0 ]
        if tree.get_root() != None:
            self.__calculate_node_location(box, tree.get_root(), (0, 0), self.NODE_LINE_LENGTH, self.NODE_ANGLE )

        return ( super().width - (box[0] + box[2]) ) / 2, ( super().height - (box[1] + box[3]) ) / 2

#######################################################################################################################
'''
class PhylogeneticWindow
'''
class PhylogeneticWindow:
    PHYLOGENETIC_ICON = b'iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAACXBIWXMAAAsTAAALEwEAmpwYAAAEJUlEQVR4nO1aXWgcVRS+6dwzMVKL/w/qg/RBtC2pkp1zNiWwWBGDP4iCiApCRaigPlgQtaiIWEXENwWpVETog4I+WEWrVqQqKrQoaFGLWHbOmYTEpBQVTWzNyN0kbbNzZ5O0504q9IN52Z35znz3/N2fMeY0/qcA5C+BJD96IX9esb0vdIhJJucQk+Rm1Q+xCYFGbtttAfJhFW5AGS8ISeQ8J8YS/1QwrH0h/64ixBI328m7afjSlhDkHysQMqIlZF/RAPeaAADi3nZbbrC0yHe3k8dJeosJgIj4es+gfaJCblG2FkaJ5An3X1yXm3zFQPOyxK/rCCHZ5HH3m0eFoEwEFYLycEB3y7Ax+TKjirzLoki7rYiya3X4+7LzAflIYaQS6TeKABrq81SsI2ageY6iEfnKk4QvtP4M2U9QvjaasChPeoyMGxxbEbKfWJLHVYVA0lwNxFOepN+swW+RN3s8PtVqvNoA5I88XjnYg3zJyfD2rGteBMh/eDzyoQmBkurlEvJjV3HcPRb5MSD+VyOsIuSrgwhxL+vr8jNinmkJIX5URwjvNCEBtXQNkPxTkpibFsM1LdpbqSbi/uxyExpA/FTJKLpisGU2zDpyoDxXWqmQHzLVIF9mkd/tUDLfMfX03BPpMZZk+0IGQg84tsIi7y0fVRHol6sW1WNQ3jd9e8BUjrUHzi7p+GM2kfvMbXnkbnPl2ZK8NY+Iz0xfdqZZMqz77SwXSjMCXLV6pbUMPhZWror92TGckF8zg/u7zdIj77L19EE36Zv9JUrkRkv8c2cv8OEKE3txiBO5DFA+WEBSf2+TZs2ccmjk1hI/Aih/zyPC9aAtp0gozUV3rbkSiPcsoDJ9GuPQqmMlXO4Hkvd66unFZqkR1dNB375XoRRjdsfsM5DIlYDyzXG5Mhohr18yEa7E+laOc8OInzeNkeWtBxojywH5RZfknnsnIUnvrFwEIN/daXLYapbIa+c8Q9xrSb4rF85TUE/vqkxEjNnNJaM63UuQn3bJ7314cH83EL/UwYuTUSLXVJTYcqikOx+MkG9w9wHKPfOEXaf+Mmr6hy8MKgRIdpWIGD8+lIBkQ7nX5r8sytvBRMTEt5YYPnSizS1K0uvKBEdhKpnbPCud7d5+MswWswdKeHfpvf+ssXraKJlqbA+5B2y1pzGWeJsnL/4yA0MXhN0D5ulNQB3kXe6wxZOQW5U3AV8tepx/VTPgVnre0aqla3RnCs2az05MQ1foGEDe6PHGL1Wdj4DW1AWQX/Yk+RtVnY8AybM6Qoh3Fj3CG1XI223V03s9Cb9Dhdyt5ooeyQZUyAu2sgFPwn+rQu7mPsW4ba6u6pzdzuSjhpDCTrnbQa/wnH1US0hhLmQaB84wlX3CIRMq3O6jlrbk261CvFB7GPYjntMwyvgPV8VLcB0gKVQAAAAASUVORK5CYII='
    WINDOW_WIDTH = 1500
    WINDOW_HEIGHT = 750

    def __init__(self, show_flag = 0):
        self.__show_flag = show_flag

        sg.theme("DarkGray12")

        size_screen = sg.Window.get_screen_size()
        self.WINDOW_WIDTH = size_screen[0]
        self.WINDOW_HEIGHT = size_screen[1] - 80

        layout = [[sg.Graph(canvas_size=(self.WINDOW_WIDTH, self.WINDOW_HEIGHT),
                            graph_bottom_left=(0, self.WINDOW_HEIGHT),
                            graph_top_right=(self.WINDOW_WIDTH, 0),
#                            background_color='lightblue',
#                            enable_events=True,
                            key='graph')]]

        self.__window = sg.Window(
            'Phylogenetic',
            layout, font = ('Helvetica', '24'),
            margins = (0,0),
            location = (0,0),
            icon = self.PHYLOGENETIC_ICON,
            size = (self.WINDOW_WIDTH, self.WINDOW_HEIGHT),
            resizable = True,
            finalize = True )

        self.__window.maximize()

        self.__graph = self.__window['graph']         # type: sg.Graph


#####################################################################################################

    def draw_matrix(self, matrix, location, cell_size ):
        if self.__graph != None:
            b_symmetric = np.allclose( matrix, matrix.T)
            y = location[1]
            for r in range(matrix.shape[0]):
                y += cell_size[1]
                x = location[0]
                for c in range(matrix.shape[1]):
                    if ( not b_symmetric ) or c >= r:
                        self.__graph.draw_text(
                            "{:.3f}".format(matrix[r,c]),
                            (x, y),
                            color= "lightblue" if r == c else "lightgreen",
                            text_location=sg.TEXT_LOCATION_RIGHT )
                    x += cell_size[0]


#####################################################################################################

    def test_node_distance(self, tree, location):
        assert tree != None
        assert location != None
        assert self.__graph != None

        node_root = tree.get_root()
        if node_root != None:
            list_pair_id = [ ("S001", "S010"), ("S002", "S009"), ("S003", "S001"), ("S002", "S007") ]

            x = location[0]
            y = location[1]

            self.__graph.draw_text(
                "Distance:",
                ( x, y ),
                text_location = sg.TEXT_LOCATION_LEFT,
                color= "white",
                font=( 'Helvetica', 10, 'bold'))

            for pair_id in list_pair_id:
                y += 20
                id_1 = pair_id[0]
                id_2 = pair_id[1]

                dist = node_root.calculate_distance_by_id( id_1, id_2 )
                dist = None if dist == None else round( dist, 3 )

                self.__graph.draw_text(
                    f"({id_1}, {id_2}) = {dist}",
                    ( x, y ),
                    text_location = sg.TEXT_LOCATION_LEFT,
                    color= "white",
                    font=( 'Helvetica', 9, 'normal'))

#####################################################################################################

    def run(self):

    #    circle = graph.draw_circle((75, 75), 25, fill_color='black', line_color='white')
    #    point = graph.draw_point((75, 75), 10, color='green')
    #    oval = graph.draw_oval((25, 300), (100, 280), fill_color='purple', line_color='purple')
    #    rectangle = graph.draw_rectangle((25, 300), (100, 280), line_color='purple')
    #    line = graph.draw_line((0, 0), (100, 100))
    #    arc = graph.draw_arc((0, 0), (400, 400), 160, 10, style='arc', arc_color='blue')
    #    poly = graph.draw_polygon(((10,10), (20,0), (40,200), (10,10)), fill_color='green')

    #   node1 = draw_node(graph, (300, 300), "Hello" )
    #   node2 = draw_node(graph, (500, 500), "Cat", (300, 300) )

        filename = sg.popup_get_file(
            'Select a JSON file or text file to create phylogentic tree',
            title='Phylogenetic',
            icon=self.PHYLOGENETIC_ICON,
            file_types=(
                ("JSON Files(*.json);Text Files(*.txt)", "*.json;*.txt"),
                ("JSON Files(*.json)", "*.json"),
                ("Text Files(*.txt)", "*.txt"),),
            default_extension = ".json")

        if filename:
            vedbs_1 = bs.VertexEdgeDataBS(filename)

            # Draw Matrix
            mat = vedbs_1.create_matrix()
            if np.all(mat) != None:
                self.draw_matrix(
                    mat,
                    (self.__window.size[0] - mat.shape[0] * 40, 0),
                    (40, 20) )

            # Make Vertexes & Edges
            vedbs_1.make_vertex_edge()
            tree = gtn.Tree(vedbs_1)

            # Draw the tree
            tp = None

            match self.__show_flag:
                case 0:
                    tp = TreeLayoutA( self.WINDOW_WIDTH, self.WINDOW_HEIGHT, self.__graph)
                case 1:
                    tp = TreeLayoutB( self.WINDOW_WIDTH, self.WINDOW_HEIGHT, self.__graph)

            if tp != None:
                x, y = tp.calculate_best_tree_location(tree)
                tp.draw_tree(tree, (x, y))

            # Draw Distance
            self.test_node_distance(tree, (20, 20))

            # Event loop for your action, such as closing the window
            while True:
                event, values = self.__window.read()
                if event == sg.WIN_CLOSED:
                    break

        self.__window.close()

#####################################################################################################
#####################################################################################################

def test():
    PhylogeneticWindow(0).run()
    PhylogeneticWindow(1).run()

if __name__ == '__main__':
    test()
