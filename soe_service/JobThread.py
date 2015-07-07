# -*- coding:utf-8 -*-
import os
import threading

from soe_service.r_wrapper.RResultParser import RResultParser
from soe_service.r_wrapper.RWrapper import RWrapper


class JobThread(threading.Thread):

    SOE_SCRIPT = os.path.abspath("SOE.r")

    def __init__(self, job, soe_service):
        threading.Thread.__init__(self)
        self.daemon = True
        self.job = job
        self.result_lock = soe_service.result_lock
        self.result_storage = soe_service.result_storage
        self.thread_count_lock = soe_service.thread_count_lock
        self.soe_service = soe_service

    def write_job_to_result_dict(self):
        self.result_lock.acquire()
        print("Written Job to result dict", self.job.job_id)
        self.result_storage[self.job.job_id] = self.job
        self.result_lock.release()

    def clean_up(self):
        self.thread_count_lock.acquire()
        self.soe_service.current_thread_count -= 1
        self.thread_count_lock.release()

    def run(self):
        try:
            RWrapper.check_data(self.job.data_file_path, self.job.num_objects,
                                self.job.dimensions, self.job.max_iterations)
        except AssertionError as e:
            self.job.success = False
            self.job.error_message = str(e)
            self.write_job_to_result_dict()
            return self.clean_up()
        except ValueError as e:
            self.job.success = False
            self.job.error_message = str(e)
            self.write_job_to_result_dict()
            return self.clean_up()

        try:
            print("Started Embedding Script")
            r_script_result = RWrapper.call_r_script_native(script=JobThread.SOE_SCRIPT,
                                                            n=self.job.num_objects,
                                                            dimensions=self.job.dimensions,
                                                            max_iterations=self.job.max_iterations,
                                                            tmp_file_name=self.job.data_file_path)
            r_script_result = [e.decode("utf-8") for e in r_script_result]

            embedding_result = RResultParser.parse_embedding_result(r_script_result)
            iteration_result = RResultParser.parse_iterations_result(r_script_result)

            # Save the results into a tmp file and attach the path to the job
            embedding_file, iterations_file = JobThread.write_embedding_results_to_disk(self.job.job_id,
                                                                                         embedding_result,
                                                                                         iteration_result)
            self.job.embedding_file = embedding_file
            self.job.iterations_file = iterations_file
            self.job.success = True
        except Exception as exc:
            self.job.error_message = str(exc)
            self.job.success = False

        self.write_job_to_result_dict()
        self.clean_up()

    @staticmethod
    def write_embedding_results_to_disk(job_id, embedding_result, iteration_result):
        embedding_file = "/tmp/{}.embedding".format(job_id)
        iterations_file = "/tmp/{}.iterations".format(job_id)

        embedding_as_string = "\n".join([",".join([str(e) for e in row]) for row in embedding_result.points])
        iteration_as_string = "\n".join([",".join([str(e) for e in row]) for row in iteration_result])

        with open(embedding_file, 'w') as f:
            f.write(embedding_as_string)

        with open(iterations_file, 'w') as f:
            f.write(iteration_as_string)

        return embedding_file, iterations_file