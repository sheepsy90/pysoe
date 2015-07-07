# -*- coding:utf-8 -*-


class SOEProcess(object):

    def __init__(self, job_id, comparison_file, object_count, embedding_dimension, max_iterations):
        self.data_file_path = comparison_file
        self.job_id = job_id
        self.num_objects = object_count
        self.dimensions = embedding_dimension
        self.max_iterations = max_iterations

        # Result View Fields
        self.success = False
        self.embedding_file = None
        self.iterations_file = None
        self.error_message = None

    def get_response_view_dictionary(self):
        return {
            "success": self.success,
            "embedding_file": self.embedding_file,
            "iterations_file": self.iterations_file,
            "error_message": self.error_message
        }