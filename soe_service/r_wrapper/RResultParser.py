# -*- coding:utf-8 -*-
from soe_service.r_wrapper.REmbeddingResult import REmbeddingResult


class RResultParser(object):

    BEGIN_RESULT = '''[1] "== BEGIN RESULT =="'''
    END_RESULT = '''[1] "== END RESULT =="'''

    @staticmethod
    def parse_embedding_result(r_script_result):
        i, j = RResultParser.get_start_stop_index_embedding_points(r_script_result)
        return REmbeddingResult(r_script_result[i:j+1])

    @staticmethod
    def get_start_stop_index_embedding_points(r_script_result):
        begin_idx = r_script_result.index(RResultParser.BEGIN_RESULT)
        end_idx = r_script_result.index(RResultParser.END_RESULT)
        return begin_idx, end_idx

    @staticmethod
    def parse_iterations_result(r_script_result):
        iteration_elements = [element for element in r_script_result if 'iter ' in element or 'initial' in element]

        while True:
            total_character_length_before = sum([len(e) for e in iteration_elements])
            iteration_elements = [e.replace("  ", " ") for e in iteration_elements]
            total_character_length_after = sum([len(e) for e in iteration_elements])

            if total_character_length_after == total_character_length_before:
                break

        iteration_elements = [e.split(" ") for e in iteration_elements]
        iteration_elements = [[1, iteration_elements[0][2]]] + [[e[1], e[3]] for e in iteration_elements[1:]]
        iteration_elements = [[int(e[0]), float(e[1])] for e in iteration_elements]

        return iteration_elements

