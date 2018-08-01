import logging
import os
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask import request
from flask import json
from flask import Response
from models.buro import FraudDataModel

app = Flask(__name__)
logging_handler = RotatingFileHandler('logs/mfrd.log', maxBytes=10000, backupCount=1)
logging_handler.setLevel(logging.INFO)
app.logger.addHandler(logging_handler)

CUTOFF = os.environ.get('CUTOFF', 0.000032891)


@app.route('/', methods=['POST'])
def fraud_virification():

    app.logger.warning('A warning has occurred')
    app.logger.error('An error occurred')
    app.logger.info('Info')

    fraud_model = FraudDataModel(request.json)
    if fraud_model.validate():
        return Response(json.dumps(fraud_model.get_response(CUTOFF)), status=200, mimetype='application/json')
    return Response(json.dumps({"Bad": "Request"}), status=400, mimetype='application/json')
