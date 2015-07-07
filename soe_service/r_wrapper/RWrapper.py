# -*- coding:utf-8 -*-
import subprocess


class RWrapper():
    """ This wrapper is used to automatically execute R-Scripts an read in the results """

    @staticmethod
    def read_data_file(data_file_path):
        with open(data_file_path, 'r') as f:
            data = f.read()
            data = data.split("\n")
            data = [[int(e) for e in row.split(",")] for row in data]
        return data

    @staticmethod
    def check_data(data_file_path, num_objects, dimensions, max_iterations):
        """ This method is the wrapper which transforms the data given as list of list and turns it
            into the correct string representation - it furthermore allows to check the data in a
            logic way. """

        data_as_list = RWrapper.read_data_file(data_file_path)

        len_complete = len(data_as_list)
        len_filtered = len([d for d in data_as_list if len(d) == 4])

        assert len_complete == len_filtered, "Some rows don't have four elements! {}!={}".format(len_complete,
                                                                                                 len_filtered)

        # Check that n is an integer
        assert isinstance(num_objects, int)

        assert dimensions > 0, "The number of dimensions must be greater than zero!"
        assert max_iterations > 0, "the number of iterations must be greater than zero!"

        # Check the Logical constraints on the data
        for element in data_as_list:
            for number in element:
                assert number <= num_objects, \
                    "There is an object number that is higher than n! {} >= {}".format(number, num_objects)
                assert number != 0, \
                    "The number of an object isn't allowed to be zero!"

        return num_objects

    @staticmethod
    def call_r_script_native(script, n, dimensions, max_iterations, tmp_file_name):
        sub_program = subprocess.Popen(['Rscript', script,
                                        '--N', str(n),
                                        '--dimensions', str(dimensions),
                                        '--max_iterations', str(max_iterations),
                                        '--data_filename', tmp_file_name,
                                        "--", '/dev/tty'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = []
        while True:
            line = sub_program.stdout.readline()
            if line != b'':
                value = line.rstrip()
                result.append(value)
            else:
                break
        return result




