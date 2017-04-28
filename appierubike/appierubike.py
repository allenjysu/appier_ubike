#! /usr/bin/env python
"""
:author: Allen Su <civin.su@gmail.com>
:test_connand :  curl "http://127.0.0.1:9888/v1/ubike-station/taipei?lat=25.034153&lng=121.568" 
                -X GET -i 
                -H "Content-Type:application/json" 
                -H "Accept:application/json"

"""
import json
import sys

from auth import client
from flask import Flask, request, jsonify
from werkzeug.serving import run_simple
from auth.client import ubike_check
from _mysql import result

app = Flask(__name__)


@app.route('/v1/ubike-station/taipei', methods=['GET'])
def get_object_usage():
    raw_data = {}
    code = 0
    try:
        float(request.args['lat'])
        float(request.args['lng'])
        result = ubike_check(request.args)
        if result['full'] == True:
            code = 1
        if result['taipei'] == False:
            code = -2
    except ValueError:
        code = -1
    except:
        print("Unexpected error:", sys.exc_info()[0])
        code = -3
    finally:
        if code in [0, 1]:
            raw_data = {
                "code": code,
                "result": [result['station'][0], result['station'][1]]
            }
        else:
            raw_data = {
                "code": code,
                "result": []
            }
        return jsonify(raw_data)


if __name__ == '__main__':
    # app.run(threaded=True, host='0.0.0.0')
    run_simple('0.0.0.0', 9888, app, use_reloader=True, threaded=True)
