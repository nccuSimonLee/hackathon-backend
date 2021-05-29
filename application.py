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
from table_manager import TableManager


# Create and configure the Flask app
application = flask.Flask(__name__)
CORS(application)
os.environ['APP_CONFIG'] = 'default_config'
application.config.from_envvar('APP_CONFIG', silent=True)
application.debug = application.config['FLASK_DEBUG'] in ['true', 'True']

ddb = client('dynamodb', region_name=application.config['AWS_REGION'])
RESERVATION = Reservation(ddb, application.config['TABLE_NAME'])

LINEUP_QUEUE = LineupQueue()

TABLE_MANAGER = TableManager(6)

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

@application.route('/take-a-number', methods=['POST'])
def take_a_number():
    params = request.json or request.form
    response = {'status': 'fail'}
    if params['action'] == 'line-up':
        response['status'] = 'success'
        dining_no = LINEUP_QUEUE.take_lineup_no()
        response['dining_no'] = dining_no
        table_no = TABLE_MANAGER.get_empty_table()
        if table_no is not None:
            LINEUP_QUEUE.get_next_dining_no()
            TABLE_MANAGER.occupy_table(table_no)
            response['table_no'] = str(table_no)
    return flask.jsonify(response)

@application.route('/free-a-table', methods=['POST'])
def free_a_table():
    params = request.json or request.form
    table_no = int(params['table_no'])
    TABLE_MANAGER.free_table(table_no)
    response = {
        'status': 'success',
        'table_no': str(table_no),
        'occupation': TABLE_MANAGER.get_state(table_no)
    }
    if response['occupation'] == 'empty' and not LINEUP_QUEUE.is_empty():
        response['occupation'] = LINEUP_QUEUE.get_next_dining_no()
    return flask.jsonify(response)

@application.route('/table-status', methods=['POST'])
def table_status():
    params = request.json or request.form
    table_no = int(params['table_no'])
    remaining_time = TABLE_MANAGER.get_remaining_time(table_no)
    response = {
        'status': 'success',
        'table_no': str(table_no),
        'state': TABLE_MANAGER.get_state(table_no),
        'remain_minutes': remaining_time.minute,
        'remain_seconds': remaining_time.second
    }
    return flask.jsonify(response)

if __name__ == '__main__':
    application.run(host='127.0.0.1')
