import numpy as np
import numpy.matlib as matrix
import species as bs

class SmithWaterman:

    def __init__(self, score_match = 3, score_mismatch = -2, score_gap = -2, score_gap_ratio = -2):
        assert score_match > 0
        assert score_mismatch < 0
        assert score_gap < 0
        # assert compare_gap >= 0.0 and compare_gap <= 1.0

        self.__SW_SCORE_MATCH = score_match
        self.__SW_SCORE_MISMATCH = score_mismatch
        self.__SW_SCORE_GAP = score_gap
        self.__SW_SCORE_GAP_RATIO = score_gap_ratio


###################################################################################################
    def compare(self, dna_sequence_1, dna_sequence_2, match_score = 1, mismatch_score = 0, gap_penalty = -1):

        assert match_score > 0, "Match score must be greater than 0"
        assert gap_penalty < 0, "Gap penalty must be less than 0"

        str_alignment_1, str_alignment_2 = self.align( dna_sequence_1, dna_sequence_2 )
        if str_alignment_1 == None or str_alignment_2 == None:
            return 8

        score = 0
        for i in range( len( str_alignment_1 ) ):
            if str_alignment_1[i] == '_' or str_alignment_2[i] == '_':
                score += gap_penalty
            elif str_alignment_1[i] == str_alignment_2[i]:
                score += match_score
            else:
                score += mismatch_score


        max_length = max(len(dna_sequence_1), len(dna_sequence_2), len(str_alignment_1))

        return 1 - ((score/match_score) / max_length)

    def align( self, dna_sequence_1, dna_sequence_2 ):
#        print( "DNA_1 : ", dna_sequence_1)
#        print( "DNA_2 : ", dna_sequence_2)
        matrix_sw, matrix_sw_path, location_max = self.__create_matrix( dna_sequence_1, dna_sequence_2 )
        if location_max == None:
            return None, None
        if location_max[0] == 0 or location_max[1] == 0:  # If the alignment string is not found
            return None, None

        path_sw = self.__find_path( matrix_sw_path, location_max )

        return self.__make_alignment_string( dna_sequence_1, dna_sequence_2, matrix_sw_path, path_sw )

###################################################################################################
    def __create_matrix( self, dna_sequence_1, dna_sequence_2 ):
        len_1 = len( dna_sequence_1 )
        len_2 = len( dna_sequence_2 )

        size_matrix_1 = len_1 + 1
        size_matrix_2 = len_2 + 1

        matrix_sw = matrix.zeros( ( size_matrix_1, size_matrix_2 ) )
        matrix_sw_path = matrix.zeros( matrix_sw.shape )

        position_max_element = None
        max_element = 0

        for row_index in range( 1, size_matrix_1 ):         # start from row 1 (the second row)
            for column_index in range( 1, size_matrix_2 ):  # start from column 1 (the second column)
                row_index_1 = row_index - 1
                column_index_1 = column_index - 1

                score = self.__SW_SCORE_MATCH if dna_sequence_1[row_index_1] == dna_sequence_2[column_index_1] else self.__SW_SCORE_MISMATCH

                data_element_left_up = matrix_sw[row_index_1, column_index_1] + score

                data_element_up = matrix_sw[row_index_1, column_index] + self.__SW_SCORE_GAP

                # move up a row
                row_index_1 -= 1
                gap_penalty = self.__SW_SCORE_GAP
                while matrix_sw_path[row_index_1, column_index] == 2:
                    gap_penalty += self.__SW_SCORE_GAP_RATIO
                    data_element_up_1 = matrix_sw[row_index_1, column_index] + gap_penalty
                    if data_element_up < data_element_up_1:
                        data_element_up = data_element_up_1
                    row_index_1 -= 1

                data_element_left = matrix_sw[row_index, column_index_1] + self.__SW_SCORE_GAP

                # move left a column
                column_index_1 -= 1
                gap_penalty = self.__SW_SCORE_GAP
                while matrix_sw_path[row_index, column_index_1] == 3:
                    gap_penalty += self.__SW_SCORE_GAP_RATIO
                    data_element_left_1 = matrix_sw[row_index, column_index_1] + gap_penalty
                    if data_element_left < data_element_left_1:
                        data_element_left = data_element_left_1
                    column_index_1 -= 1

                data_max = max( data_element_left_up, data_element_up, data_element_left )

                if data_max > 0:
                    matrix_sw[row_index, column_index] = data_max
                    matrix_sw_path[row_index, column_index] = 1 if data_max == data_element_left_up else 2 if data_max == data_element_up else 3
                        # 1: left up, 2: up, 3: left

                    if data_max > max_element:
                        max_element = data_max
                        position_max_element = (row_index, column_index)

        # return two matrices, and the coordinates (x, y) of the minimum element of the matrix_sw
        return matrix_sw, matrix_sw_path, position_max_element


    def __find_path(self, matrix_sw_path, position_max_element ):
        data_element = matrix_sw_path[position_max_element]
        smith_waterman_path = []

        row = position_max_element[0]
        column = position_max_element[1]

        while data_element != 0:
            smith_waterman_path.append((row, column))
            match data_element:
                case 1:     # 1: left up
                    row -= 1
                    column -= 1
                case 2:     # 2: up
                    row -= 1
                case 3:     # 3: left
                    column -= 1
            data_element = matrix_sw_path[row, column]

        return smith_waterman_path


    def __make_alignment_string(self, dna_sequence_1, dna_sequence_2, matrix_sw_path, path_smith_waterman ):
        str_alignment_1 = ""
        str_alignment_2 = ""

        for position in path_smith_waterman:
            match matrix_sw_path[position]:
                case 1:     # 1: left up
                    str_alignment_1 += dna_sequence_1[position[0] - 1]
                    str_alignment_2 += dna_sequence_2[position[1] - 1]
                case 2:     # 2: up
                    str_alignment_1 += dna_sequence_1[position[0] - 1]
                    str_alignment_2 += '_'
                case 3:     # 3: left
                    str_alignment_1 += '_'
                    str_alignment_2 += dna_sequence_2[position[1] - 1]

        return str_alignment_1[::-1], str_alignment_2[::-1]

###################################################################################################

    def __str__(self):
        return "Match Score: {}  Mismatch Score: {}  Gap Score: {}".format(
            self.__SW_SCORE_MATCH,
            self.__SW_SCORE_MISMATCH,
            self.__SW_SCORE_GAP)

###################################################################################################

def test():

    def test_smith_waterman(dna_sequence_1, dna_sequence_2):
        sw = SmithWaterman(score_match=5)
        print(sw)

        print( "DNA Sequence: ", dna_sequence_1, dna_sequence_2 )
        str_alignment_1, str_alignment_2 = sw.align( dna_sequence_1, dna_sequence_2 )
        print( "Alignment: ")
        print( str_alignment_1)
        print( bs.make_alignment_flag_string(str_alignment_1, str_alignment_2 ))
        print( str_alignment_2)
        dna_sequence_diff = sw.compare( dna_sequence_1, dna_sequence_2 )
        print( "Difference: ", dna_sequence_diff )


    list_dna_sequence_pair = [
#       ('ACAGCCGTCGCATCGTACGGATCCATGTC', 'ACAGCCGGTCGCAGCTACGGATCCATGTC'),
        ('ACTGCACGATCGCTACGTACGATCCATGTC','ACTGCGGAACTAATCGAACGGATCAAGTC')
        ]

    for dna_sequence_pair in list_dna_sequence_pair:
        print( "\r\n************************************************************\r\n" )

        print( dna_sequence_pair )
        print( dna_sequence_pair[0], dna_sequence_pair[1] )

        test_smith_waterman(dna_sequence_pair[0], dna_sequence_pair[1])
        print( "\r\n" )
        test_smith_waterman(dna_sequence_pair[1], dna_sequence_pair[0])


if __name__ == '__main__':
    test()
