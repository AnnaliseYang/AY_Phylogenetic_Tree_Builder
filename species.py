import json
import numpy as np
import numpy.matlib as matrix

import smith_waterman as sw
import graph_tree_node as gtn

'''
function: make_alignment_flag_string( str_alignment_1, str_alignment_2)
sample:
    str_alignment_1 = "AGCT_AGCT"
    str_alignment_2 = "AGTCAAGCT"
    return          = "||.._||||"
'''
def make_alignment_flag_string( str_alignment_1, str_alignment_2):
    assert str_alignment_1 != None
    assert str_alignment_2 != None

    len1 = len(str_alignment_1)
    len2 = len(str_alignment_1)
    if len1 != len2:
        return None
    
    flag = []

    for i in range(len1):
        if str_alignment_1[i] == str_alignment_2[i]:
            flag.append( '|' )
        elif str_alignment_1[i] == '_' or str_alignment_2[i] == '_':
            flag.append( ' ' )
        else:
            flag.append( '.')

    return "".join( flag )

'''
class: Species
'''
class Species:
    def __init__(self, id, name, dna ):
        self.__id = id
        self.__name = name
        self.__dna = dna

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_dna(self):
        return self.__dna

    def compare(self, species):
        return sw.SmithWaterman().compare( self.__dna, species.__dna )

    def __str__(self):
        return f"Species  ID: {self.__id}  Name: {self.__name}  DNA: {self.__dna}"
    
'''
class: VertexEdgeDataBS (based on gtn.VertexEdgeData )
'''
class VertexEdgeDataBS( gtn.VertexEdgeData ):
    def create_species_by_vertex_id(self, i):
        vertex = self.get_vertex_by_index(i)
        if vertex != None:
            id = vertex[0]      # id is the first element of the tuple of vertex_1
            data = vertex[1]    # a dictionary for datas of the vertex
            name = data.get("name") if data.get("name") != None else data.get(0) if len(data) > 1 else None
            dna = data.get("dna") if data.get("dna") != None else data.get(0) if len(data) < 2 else data.get(1)
            return Species(id, name, dna)
        return None


    def create_matrix(self):
        vertex_count = self.get_vertex_count()
        if vertex_count == 0:
            return None
        
        mat = matrix.zeros(( vertex_count, vertex_count ))

        for i in range(0, vertex_count):
            species_1 = self.create_species_by_vertex_id(i)
            if species_1 != None:
                for j in range(i + 1, vertex_count):
                    species_2 = self.create_species_by_vertex_id(j)
                    if species_2 != None:
                        diff = species_1.compare(species_2)
                        mat[i,j] = diff
                        mat[j,i] = diff

        return mat
    

    def make_vertex_edge(self):
        def __find_min_element(mat):
            size = mat.shape[0]
            if size < 2 or size != mat.shape[1]:
                return None, None # Row, Column
            
            row = 0
            column = 1
            data_element_min = mat[row, column]

            for r in range(size):
                for c in range(r + 1, size):
                    data_element = mat[r, c]
                    if data_element < data_element_min:
                        data_element_min = data_element
                        row = r
                        column = c

            return row, column
        
        ##############################################################################

        super().get_list_edge().clear()

        mat = self.create_matrix()
        if np.any(mat) == None:
            return -1, -1
        
        size = mat.shape[0]
        list_node_index = np.arange( size ) # to mark the node index
        
        __id_new = 100 # to create a new id for a new vertex

        index = size
        while size > 1:
            __id_new += 1
            id_new = "P{:03}".format(__id_new)
            row, column = __find_min_element(mat)

            weight = mat[row, column]
            super().set_data( list_node_index[row], 'weight', weight)
            super().set_data( list_node_index[column], 'weight', weight)

            ## add_vertex & add_edge
            vertex_0 = self.get_vertex_by_index(list_node_index[row])
            vertex_1 = self.get_vertex_by_index(list_node_index[column])
            id_0 = vertex_0[0]
            id_1 = vertex_1[0]

            self.add_vertex( id = id_new, data = { 'name': f"[{id_0} & {id_1}]" } )
            self.add_edge( id_1 = id_new, id_2 = id_0, weight=weight)
            self.add_edge( id_1 = id_new, id_2 = id_1, weight=weight )

            ## matrix
            mat[row] = ( mat[row] + mat[column] ) / 2.0
            mat[:,row] = ( mat[:,row] + mat[:,column] ) / 2.0
            mat[row, row] = 0.0
            mat = np.delete(mat, column, 0) # delete the row
            mat = np.delete(mat, column, 1) # delete the column
            
            ## list
            list_node_index[row] = index
            list_node_index = np.delete(list_node_index, column)

            ## prepare the next loop
            index += 1
            size -= 1
           
        return True

###################################################################################################
###################################################################################################

def test_vertex_edge_data_bs():

    vedbs_1 = VertexEdgeDataBS()
    file_path_name = "D:/VE_Bio.json"
    vedbs_1.load_from_json_file( file_path_name )
    print( file_path_name )
    print( vedbs_1 )

    print( "============================================================")

    file_path_name = "D:/VE_Bio_20240105_NoID.txt"
    vedbs_1.load_from_txt_file( file_path_name )
    print( vedbs_1 )
    print( vedbs_1.create_matrix() )
    print( vedbs_1.make_vertex_edge() )
    print( vedbs_1 )

#    print(vedbs_1.create_matrix())

def test_species():        
    dna_1 = "TGTTACGG"
    dna_2 = "GGTTGACTA"

   
    species_1 = Species( "1001", "Dog", dna_1 )
    print(species_1)

    species_2 = Species( "8888", "Cat", dna_2 )
    print(species_2)

    print( species_1.compare( species_2 ))

if __name__ == '__main__':
#    test_species()
    test_vertex_edge_data_bs()