import logging
import json
from functools import partial
import flask
from flask import request, Response
from flask_cors import CORS
import os
from boto3 import client

from reservation import Reservation
from lineup_queue import LineupQueue


# Create and configure the Flask app
application = flask.Flask(__name__)
CORS(application)
os.environ['APP_CONFIG'] = 'default_config'
application.config.from_envvar('APP_CONFIG', silent=True)
application.debug = application.config['FLASK_DEBUG'] in ['true', 'True']

ddb = client('dynamodb', region_name=application.config['AWS_REGION'])
RESERVATION = Reservation(ddb, application.config['TABLE_NAME'])

LINEUP_QUEUE = LineupQueue()

@application.route('/reservation', methods=['POST'])
def reservation():
    params = request.json or request.form
    if params['action'] == 'book':
        dining_no = LINEUP_QUEUE.take_showup_no()
        response = RESERVATION.book_table(
            params['phone_no'],
            str(params['time_slot']), 
            dining_no
        )
    else:
        response = RESERVATION.cancel_table(params['phone_no'])
    return flask.jsonify(response)


if __name__ == '__main__':
    application.run(host='127.0.0.1')
