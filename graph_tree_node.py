import json


class VertexEdgeData:
    def __init__(self, file_path_name = None):
        self.__vertexes = []
        self.__edges = []
        if file_path_name != None:
            self.load_from_file( file_path_name)

    def clear(self) -> None:
        self.__vertexes.clear()
        self.__edges.clear()

    def add_vertex(self, id, data) -> None:
        self.__vertexes.append((id, data) )

    def add_edge(self, id_1, id_2, weight = None) -> None:
        self.__edges.append((id_1, id_2, weight))

    def add_vertexes(self, vertexes) -> None:
        self.__vertexes += vertexes

    def add_edges(self, edges) -> None:
        self.__edges += edges

    def set_data(self, index, key, value) -> None:
        vertex = self.get_vertex_by_index(index)
        if vertex != None:
            if vertex[1] != None:
                vertex[1][key] = value
            else:
                vertex[1] = { key, value}

    def get_data(self, index, key):
        vertex = self.get_vertex_by_index(index)
        if vertex != None:
            if vertex[1] != None:
                return vertex[1].get(key)
        return None

###################################################################################################

    def load_from_file(self, file_path_name) -> None:
        file_path_name = file_path_name.strip()

        if file_path_name[-5:].lower() == ".json":
            self.load_from_json_file( file_path_name )
        elif file_path_name[-4:].lower() == ".txt":
            self.load_from_txt_file( file_path_name)
        else:
            raise NameError( "File Name Error! Only JSON File(*.josn) or Text File(*.txt) is ok!\r\n{}".format( file_path_name ) )


    def load_from_json_file(self, json_file) -> None:
        self.clear()

        with open(json_file, 'r') as file:
            j = json.loads( file.read() )

            vertexes = j.get("VERTEX") if j.get("VERTEX") != None else j.get("vetrex") if j.get("vetrex") != None else j.get("Vetrex")
            edges = j.get("EDGE") if j.get("EDGE") != None else j.get("edge") if j.get("edge") != None else j.get("Edge")

            if vertexes != None:
                self.__vertexes = [ (vertex["id"], vertex["data"]) for vertex in vertexes ]

            if edges != None:
                self.__edges = [ ( edge["id1"], edge["id2"], edge.get("weight")) for edge in j["EDGE"] ]


    def load_from_txt_file(self, txt_file) -> None:
        self.clear()

        with open(txt_file, 'r') as file:
            id_auto = 1

            for line in file.readlines():
                pos = line.find( "#" )
                if pos != -1:
                    line = line[:pos]

                items = [ item.strip(" \t\r\n") for item in line.split(',') ]
                item_count = len(items)

                if len( items[0] ) > 0:
                    match item_count:
                        case 1: # one item
                            if len(items[0]) > 0:
                                self.add_vertex( id = "S{:03}".format(id_auto), data = { 0: items[0] } )
                                id_auto += 1 # automatically generate a random id number
                        case _: # multiple items
                            dict_data = { i : item for i, item in enumerate(items[1:])}
                            self.add_vertex( id = items[0], data = dict_data )


###################################################################################################

    def get_list_vertex(self) -> list:
        return self.__vertexes

    def get_list_edge(self) -> list:
        return self.__edges

    def get_vertex_count(self) -> int:
        return len(self.__vertexes)

    def get_edge_count(self) -> int:
        return len(self.__edges)

###################################################################################################

    def get_vertex_by_index(self, index) -> tuple:
        if index >= 0 and index < len( self.__vertexes ):
            return self.__vertexes[index]
        return None

    def get_vertex_by_id(self, id) -> tuple:
        for vertex in self.__vertexes:
            if id == vertex[0]:
                return vertex
        return None

    def get_children_by_id(self, id) -> list:
        ids = [ edge[1] for edge in self.__edges if edge[0] == id ]
        return [ vertex for vertex in self.__vertexes if vertex[0] in ids ]

    def find_vertex_root(self) -> tuple:
        if self.get_vertex_count() < 1:
            return None
        if self.get_edge_count() < 1:
            return self.__vertexes[0]

        root_id = self.__edges[0][0]
        loop = True
        while loop:
            loop = False
            for edge in self.__edges:
                if edge[1] == root_id :
                    root_id = edge[0]
                    loop = True
                    break

        return self.get_vertex_by_id(root_id)


###################################################################################################

    def __str__(self) -> str:
        return "".join(
            [ f"Vertex: {len(self.__vertexes)}" ] +
            [ "\r\n\t{}".format(vertex) for vertex in self.__vertexes ] +
            [ f"\r\nEdge: {len(self.__edges)}" ] +
            [ "\r\n\t{}".format(edge) for edge in self.__edges ])


###################################################################################################

class Node:
    def __init__(self, id, data = None, parent = None):
        self.__id = id
        self.__data = data
        self.__parent = parent  # parent node
        self.__children = []    # list of this node's children

        if parent != None:
            if self not in parent.__children:
                parent.__children.append(self)

###############################################################################################

    def get_id(self) -> str:
        return self.__id

    def get_data(self) -> dict:
        return self.__data

    def get_parent(self) -> object:
        return self.__parent

    def get_root(self) -> object:
        node = self
        while node.__parent != None:
            node = node.__parent
        return node

    def get_data(self, key):
        return self.__data.get(key) if self.__data != None else None

    def set_data(self, key, value):
        if self.__data == None:
            self.__data = { key: value }
        else:
            self.__data[key] = value

    def is_leaf(self) -> bool:
        return len(self.__children) == 0

    def is_root(self) -> bool:
        return self.__parent == None

###############################################################################################

    def get_children(self) -> list:
        return self.__children

    def get_children_count(self) -> int:
        return len(self.__children)

    def get_child_by_index(self, index) -> int:
        if index >= 0 and index < len(self.__node_children):
            return self.__children[index]
        return None

    def get_child_by_id(self, id) -> object:
        for child in self.__children:
            if child.__id == id:
                return child
        return None

    def get_offspring_count(self) -> int:
        count = len(self.__children)
        for child in self.__children:
            count += child.get_offspring_count()
        return count

    def get_depth(self) -> int:
        depth_child_max = 0
        for child in self.__children:
            depth_child = child.get_depth()
            if depth_child_max < depth_child:
                 depth_child_max = depth_child
        return depth_child_max + 1

###############################################################################################

    def set_parent(self, parent) -> None:
        """
        Set the parent of the current node
        """
        self.__parent = parent
        if parent != None:
            if self not in parent.__children:
                parent.__children.append(self)

    def add_child(self, child) -> None:
        """
        Add a child to the current node's children list
        """
        if child != None:
            child.__parent = self
            if child not in self.__children:
                self.__children.append(child)


###############################################################################################

    def find_node_by_id(self, id) -> object:
        if self.__id == id:
            return self

        for child in self.__children:
            node = child.find_node_by_id(id)
            if node != None:
                 return node

        return None

    def find_node_ancestor_by_id(self, id_1, id_2) -> object:
        node_1 = self.find_node_by_id(id_1)
        if id_1 == id_2:
            return node_1

        node_2 = self.find_node_by_id(id_2)
        nodes = []

        while node_1 != None:
            nodes.append( node_1)
            node_1 = node_1.__parent

        while node_2 != None:
            if node_2 in nodes:
                return node_2
            node_2 = node_2.__parent

        return None

    def calculate_distance_by_id(self, id_1, id_2) -> int:
        node_1 = self.find_node_by_id(id_1)
        node_2 = self.find_node_by_id(id_2)

        if( node_1 == None or node_2 == None):
            return None

        if id_1 == id_2:
            return 0

        nodes = []

        while node_1 != None:
            nodes.append( node_1)
            node_1 = node_1.__parent

        distance_1 = 0

        while node_2 != None:
            if node_2 in nodes:
                id = node_2.__id
                distance_2 = 0
                for node_3 in nodes:
                    if node_3.__id == id:
                        break
                    weight_3 = node_3.get_data('weight')
                    distance_2 += ( 1 if weight_3 == None else weight_3 )
                return distance_1 + distance_2
            weight_2 = node_2.get_data('weight')
            distance_1 +=  ( 1 if weight_2 == None else weight_2 )
            node_2 = node_2.__parent

        return None

###############################################################################################

    def __to_string(self, depth = 0) -> str:
        prefix = "\t" * depth

        strings1 = [
            f"[Node] ID: {self.__id}  Data: {self.__data}  CC: {self.get_children_count()}  OC: {self.get_offspring_count()}  ",
            f"Parent: {self.__parent.__id}" if self.__parent != None else "None" ]

        strings2 = [ "\r\n\t{}{}".format( prefix, child.__to_string(depth + 1) ) for child in self.__children ]

        return "".join( strings1 + strings2 )

    def __str__(self) -> str:
        return self.__to_string()

###################################################################################################
###################################################################################################

class Tree:
    def __init__(self, parameter = None):
        self.__root = None
        if type(parameter) == str:
            ved = VertexEdgeData(parameter)
            self.create(ved)
        elif isinstance( parameter, VertexEdgeData):
            self.create(parameter)

    def get_root(self) -> object:
        return self.__root

    def set_root(self, root) -> None:
        self.__root = root

###################################################################################################

    def create(self, vertex_edge_data) -> None:
        def __create_node(vertex_edge_data, id, data = None, parent = None):
            node = Node( id, data, parent )
            for vertex in vertex_edge_data.get_children_by_id( id ):
                __create_node(
                    vertex_edge_data,
                    vertex[0],  # id
                    vertex[1],  # data
                    node )
            return node

        vertex_root = vertex_edge_data.find_vertex_root()
        self.__root = __create_node( vertex_edge_data, vertex_root[0], vertex_root[1] ) if vertex_root != None else None

###################################################################################################

    def __str__(self) -> str:

        if( self.__root == None ):
            return "[Tree] Empty Tree!"

        return f"[Tree] Node Count: {self.__root.get_offspring_count() + 1}\r\n{self.__root}"

###############################################################################################
###############################################################################################

def test_vertex_edge_data():

    file_path_name = "D:/VE.json"
    ved_1 = VertexEdgeData(file_path_name)

    print( file_path_name )
#    ved_1.load_from_file( file_path_name )
    print(ved_1)
    ved_1.set_data( 1, 'weight', 0.865)
    print(ved_1)
    print(ved_1.get_data(1, 'weight'))
    print(ved_1.get_data(5, 'weight'))
    print(ved_1.get_data(1, 'dna'))

    id = "N1000"
    children = ved_1.get_children_by_id(id)
    print( "Children of Vertex(ID = {}): {}".format( id, len(children) ) )
    for vertex in children:
        print( "\t"+ str(vertex) )

    print("\r\n--------------------------------------------------------------------\r\n")

    index = 1
    vertex = ved_1.get_vertex_by_index(index)
    print( "Vertex(Index = {}): {}".format( index, vertex ) )
    print("Root:", ved_1.find_vertex_root())

    print("\r\n--------------------------------------------------------------------")
    print("--------------------------------------------------------------------\r\n")

    file_path_name = "D:/VE.txt"
    print( file_path_name )
    ved_1.load_from_file( file_path_name )
    print(ved_1)

    id = "2006"
    children = ved_1.get_children_by_id(id)
    print( "Children of Vertex(ID = {}): {}".format( id, len(children) ) )
    for vertex in children:
        print( "\t"+ str(vertex) )

    print("\r\n--------------------------------------------------------------------\r\n")

    print( "Vertex(id = {}): {}".format( id, ved_1.get_vertex_by_id(id) ) )
    print("Root:", ved_1.find_vertex_root())

    index = 10
    vertex = ved_1.get_vertex_by_index(index)
    print( "Vertex(Index = {}): {}".format( index, vertex ) )
    print("Root:", ved_1.find_vertex_root())

    print("\r\n--------------------------------------------------------------------\r\n")

####################################################################################################

def test_node():
#    node_root = Node( id="N0000", data={"name": "Family"} )
    node_root = Node( id="N0000" )
    node_1 = Node( id="N1000", data={"name":"Dog", "DNA": "ACTG"}, parent=node_root )
    node_2 = Node( "N2000", "Terry Yang", node_root )
    node_1_1 = Node( "N1100", "Willow Guo", node_1 )
    node_1_2 = Node( "N1200", "Hello One", node_1 )
    node_2_1 = Node( "N2100", "Julia", node_2 )
    node_2_2 = Node( "N2200", "Spring", parent=node_2_1 )

    print( node_root)
    print( node_root.get_data("name") )
    print( node_root.get_data("dna") )
    node_root.set_data("name", "Cat")
    node_root.set_data("dna", "Hello DNA")

    print( node_root.get_data("name") )
    print( node_root.get_data("dna") )

    node_root.add_child( node_1 )
    node_2.set_parent( node_root )
    print( node_root)

    print( "Parent of node_2_2:")
    print( node_2_2.get_parent() )

    print( "Root of node_2_2:")
    print( node_2_2.get_root() )

    print( "Depth: ", node_root.get_depth() )

    print( ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" )

    test_distance = [ ("N2200", "N2100"), ("N2200", "N0000"), ("N2200", "N1100"), ("N2200", "N8888")]

    for td in test_distance:
        print( td[0], td[1], node_root.calculate_distance_by_id( td[0], td[1] ))
        print( td[1], td[0], node_root.calculate_distance_by_id( td[1], td[0] ))

####################################################################################################

def test_tree():
    ved_1 = VertexEdgeData()

    file_path_name = "D:/VE.json"
    print( file_path_name )
    ved_1.load_from_file( file_path_name )
    print(ved_1)

    tree_1 = Tree()
    tree_1.create( ved_1 )

    print( "\r\n\r\n***********************************\r\n", tree_1 )

    tree_2 = Tree( "D:/VE.json" )
    print( "\r\n\r\n***********************************\r\n", tree_2 )

    tree_3 = Tree( ved_1 )
    print( "\r\n\r\n***********************************\r\n", tree_3 )

####################################################################################################

if __name__ == '__main__':
    test_vertex_edge_data()
#    test_node()
#    test_tree()
