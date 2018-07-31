import logging
import os
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask import request
from flask import json
from flask import Response
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from statsmodels import api as sm
from statsmodels.stats.outliers_influence import OLSInfluence
from models.buro import InformacionBuroModel

app = Flask(__name__)
logging_handler = RotatingFileHandler('logs/mfrd.log', maxBytes=10000, backupCount=1)
logging_handler.setLevel(logging.INFO)
app.logger.addHandler(logging_handler)


CUTOFF = os.environ.get('CUTOFF', 0.000032891)


@app.route('/', methods=['POST'])
def verificacion_fraude():
    print(request)
    app.logger.warning('A warning has occurred')
    app.logger.error('An error occurred')
    app.logger.info('Info')

    #TODO: validar json de la peticion reasignar el parámetro NEW_OBS$MOP_MAXIMO_U24M_SERVSGRALES
    #NEW_OBS$MOP_MAXIMO_U24M_SERVSGRALES = 9 - NEW_OBS$MOP_MAXIMO_U24M_SERVSG


    jat_fraudes = pd.read_csv("JAT_FRAUDES.csv", usecols=[3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

    if request.json['MOP_MAXIMO_U24M_SERVSGRALES'] != -1:
        request.json['MOP_MAXIMO_U24M_SERVSGRALES'] = 9 - request.json['MOP_MAXIMO_U24M_SERVSGRALES']

    jat_fraudes = jat_fraudes.append(request.json, ignore_index=True)

    jat_fraudes.loc[jat_fraudes["CONSULTAS_U02M_SBCBR"] == -1, 'CONSULTAS_U02M_SBCBR'] = np.NaN
    jat_fraudes.loc[jat_fraudes["PCT_DIR_JALGTO"] == -1, 'PCT_DIR_JALGTO'] = np.NaN
    jat_fraudes.loc[jat_fraudes["PCT_APERTURAS_U18M"] == -1, 'PCT_APERTURAS_U18M'] = np.NaN
    jat_fraudes.loc[jat_fraudes["PCT_APERTURAS_ANT_REGBC"] == -1, 'PCT_APERTURAS_ANT_REGBC'] = np.NaN
    jat_fraudes.loc[jat_fraudes["PCT_CTAS_BANCARIAS"] == -1, 'PCT_CTAS_BANCARIAS'] = np.NaN
    jat_fraudes.loc[jat_fraudes["PCT_CTAS_SERVS_GRALES"] == -1, 'PCT_CTAS_SERVS_GRALES'] = np.NaN
    jat_fraudes.loc[jat_fraudes["PROM_LIMCRE_MAXCRE_SERVSGRALES"] == -1, 'PROM_LIMCRE_MAXCRE_SERVSGRALES'] = np.NaN
    jat_fraudes.loc[jat_fraudes["PCT_ALERTAS_JUICIOS"] == -1, 'PCT_ALERTAS_JUICIOS'] = np.NaN
    jat_fraudes.loc[jat_fraudes["UNIVERSO_11"] == -1, 'UNIVERSO_11'] = np.NaN

    # imputacion a nulos o vacios por la mediana
    jat_fraudes = jat_fraudes.fillna(jat_fraudes.median())

    # homologar banderas fraude a 1
    jat_fraudes.loc[jat_fraudes["UNIVERSO_11"] == 2, 'UNIVERSO_11'] = 1

    # escalamos a dispersion normal de la muestra
    scaler = StandardScaler()
    scaled_params = scaler.fit_transform(jat_fraudes.drop('UNIVERSO_11', axis=1))

    y = jat_fraudes.loc[::, 'UNIVERSO_11']
    X = sm.add_constant(scaled_params)
    model = sm.OLS(y, X)
    results = model.fit()
    print(results.summary())

    influence = OLSInfluence(results)

    # se calcula la distancia de cook
    a, b = influence.cooks_distance

    # summary = influence.summary_frame()
    data = {
        "riesgo_fraude": False,
        "cook_value": a[-1]
    }
    if data['cook_value'] > CUTOFF:
        data["riesgo_fraude"] = True

    return Response(json.dumps(data), status=200, mimetype='application/json')

