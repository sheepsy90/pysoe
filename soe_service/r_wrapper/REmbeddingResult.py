# -*- coding:utf-8 -*-


class REmbeddingResult():

    def __init__(self, embedding_result):
        self.dimensions = embedding_result[1].count(',')

        interesting_stuff = embedding_result[2:-1]

        while True:
            total_character_length_before = sum([len(e) for e in interesting_stuff])
            interesting_stuff = [e.replace("  ", " ") for e in interesting_stuff]
            total_character_length_after = sum([len(e) for e in interesting_stuff])

            if total_character_length_after == total_character_length_before:
                break

        self.points = [e.lstrip().split(" ")[1:] for e in interesting_stuff]
        self.points = [[float(pi) for pi in entry] for entry in self.points]