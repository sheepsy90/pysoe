# -*- coding:utf-8 -*-
import os
import threading
import uuid
import time

from multiprocessing import Queue
from soe_service.JobThread import JobThread
from soe_service.SOEProcess import SOEProcess


class SOEService(threading.Thread):

    MAX_THREADS = 5

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

        # The queueing for requested jobs
        self.job_queue = Queue()

        # The result stuff
        self.result_lock = threading.RLock()
        self.result_storage = {}

        # Num of threads
        self.thread_count_lock = threading.RLock()
        self.current_thread_count = 0

    def get_job_result(self, job_id):
        self.result_lock.acquire()
        has_such_job_id = self.result_storage.__contains__(job_id)
        job_result = self.result_storage.get(job_id, None)
        self.result_lock.release()

        if not has_such_job_id:
            raise KeyError("Job Id not present")
        else:
            return job_result

    def schedule_request(self, comparison_file, object_count, embedding_dimension, max_iterations):
        if not os.path.isfile(comparison_file):
            raise OSError("Not a file!")

        job_id = str(uuid.uuid4())
        self.result_lock.acquire()
        self.result_storage[job_id] = None
        self.result_lock.release()
        soe_process = SOEProcess(job_id, comparison_file, object_count, embedding_dimension, max_iterations)
        self.job_queue.put(soe_process)
        print("Added Job to Buffer")
        return job_id

    def run(self):
        while True:

            if not self.job_queue.qsize() == 0:
                can_start_a_thread = False
                self.thread_count_lock.acquire()
                if self.current_thread_count < SOEService.MAX_THREADS:
                    can_start_a_thread = True
                    self.current_thread_count += 1
                self.thread_count_lock.release()

                if can_start_a_thread:
                    job = self.job_queue.get()
                    job_thread = JobThread(job, self)
                    job_thread.start()
                    print("Started a Embedding Thread")
            else:
                time.sleep(0.1)
