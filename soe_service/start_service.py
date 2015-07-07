# -*- coding:utf-8 -*-
import flask_api.status as http_status

from flask import Flask, jsonify
from flask import request, abort
from soe_service.SOEService import SOEService

app = Flask(__name__)


@app.route('/soe/schedule', methods=['POST'])
def schedule_process():
    if request.method == 'POST':
        if request.json is None:
            return abort(http_status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

        if 'comparison_file' not in request.json or 'object_count' not in request.json:
            return abort(http_status.HTTP_412_PRECONDITION_FAILED)

        try:
            comparison_file = request.json['comparison_file']
            object_count = request.json['object_count']
            embedding_dimension = request.json.get('embedding_dimensions', 2)
            max_iterations = request.json.get('max_iterations', 1000)
            job_id = soe_service.schedule_request(comparison_file, object_count, embedding_dimension, max_iterations)
            return jsonify({'job_id': job_id}), http_status.HTTP_202_ACCEPTED
        except IOError:
            return abort(http_status.HTTP_412_PRECONDITION_FAILED)
        except BufferError:
            return abort(http_status.HTTP_503_SERVICE_UNAVAILABLE, headers={"Retry-After": 30})
    else:
        abort(http_status.HTTP_405_METHOD_NOT_ALLOWED)


@app.route('/soe/schedule_state/<string:process_id>', methods=['GET'])
def get_process_status(process_id):
    if request.method == 'GET':
        try:
            job = soe_service.get_job_result(process_id)
            if job is None:
                return "", http_status.HTTP_204_NO_CONTENT
            else:
                return jsonify(job.get_response_view_dictionary()), http_status.HTTP_201_CREATED
        except KeyError:
            return abort(http_status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)

    else:
        abort(http_status.HTTP_405_METHOD_NOT_ALLOWED)


@app.route('/soe/ping', methods=['GET'])
def ping():
    return "", http_status.HTTP_200_OK

if __name__ == '__main__':
    soe_service = SOEService()
    soe_service.start()
    app.run()