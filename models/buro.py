import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from statsmodels import api as sm
from statsmodels.stats.outliers_influence import OLSInfluence


class DataModel(object):
    csv_file = None
    columns = []
    target = None
    scaler = None
    model_class = None
    influence_class = None

    def __init__(self, *args, **kwargs):
        self.dataframe = pd.read_csv(self.csv_file, usecols=self.columns)
        self._intecept = None
        self._data = None
        
    def validate(self):
        try:
            self.dataframe = self.dataframe.append(self._data, ignore_index=True)
        except Exception as e:
            print(e)

    def scaled_data(self):
        return self.scaler.fit_transform(self.dataframe.drop(self.target, axis=1))

    def get_results(self):
        y = self.dataframe.loc[::, self.target]
        X = self.scaled_data()
        if self._intercept:
            X = sm.add_constant(X)
        results = self.model_class(y, X).fit()
        # print(results.summary())
        return results


class FraudDataModel(DataModel):
    """
    Modelo de Infromación de buró usado para diagnosticar la posibilidad de presencia fraude en un cliente
    """

    csv_file = 'data/JAT_FRAUDES.csv'
    columns = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    target = 'UNIVERSO_11'
    scaler = StandardScaler()
    model_class = sm.OLS
    influence_class = OLSInfluence

    def __init__(self, data, intercept=True, *args, **kwargs):
        """
        
        :param data: 
        :param args: 
        :param kwargs: 
        """
        super(FraudDataModel, self).__init__(args, kwargs)
        self._intercept = intercept
        self._data = data
        
    def validate(self):
        # TODO: validar _data
        try:
            self.dataframe.loc[self.dataframe["UNIVERSO_11"] == 2, 'UNIVERSO_11'] = 1
            if self._data.get('MOP_MAXIMO_U24M_SERVSGRALES', -1) != -1:
                self._data['MOP_MAXIMO_U24M_SERVSGRALES'] = 9 - self._data['MOP_MAXIMO_U24M_SERVSGRALES']
            self.dataframe = self.dataframe.append(self._data, ignore_index=True)
            return True
        except Exception as e:
            print(e)
            return False

    def impute(self):
        self.dataframe.loc[self.dataframe["CONSULTAS_U02M_SBCBR"] == -1, 'CONSULTAS_U02M_SBCBR'] = np.NaN
        self.dataframe.loc[self.dataframe["PCT_DIR_JALGTO"] == -1, 'PCT_DIR_JALGTO'] = np.NaN
        self.dataframe.loc[self.dataframe["PCT_APERTURAS_U18M"] == -1, 'PCT_APERTURAS_U18M'] = np.NaN
        self.dataframe.loc[self.dataframe["PCT_APERTURAS_ANT_REGBC"] == -1, 'PCT_APERTURAS_ANT_REGBC'] = np.NaN
        self.dataframe.loc[self.dataframe["PCT_CTAS_BANCARIAS"] == -1, 'PCT_CTAS_BANCARIAS'] = np.NaN
        self.dataframe.loc[self.dataframe["PCT_CTAS_SERVS_GRALES"] == -1, 'PCT_CTAS_SERVS_GRALES'] = np.NaN
        self.dataframe.loc[self.dataframe["PROM_LIMCRE_MAXCRE_SERVSGRALES"] == -1, 'PROM_LIMCRE_MAXCRE_SERVSGRALES'] = np.NaN
        self.dataframe.loc[self.dataframe["PCT_ALERTAS_JUICIOS"] == -1, 'PCT_ALERTAS_JUICIOS'] = np.NaN
        self.dataframe.loc[self.dataframe["UNIVERSO_11"] == -1, 'UNIVERSO_11'] = np.NaN

        # impute using the median on each column
        self.dataframe = self.dataframe.fillna(self.dataframe.median())

    def get_response(self, cutoff):
        # imputamos
        self.impute()

        # influence object contains cooks distance
        influence = self.influence_class(self.get_results())
        a, b = influence.cooks_distance

        # format response object
        data = {
            "fraud_risk": False,
            "cook_value": a[-1]  # last item maps to input data
        }
        if data['cook_value'] > cutoff:
            data["fraud_risk"] = True

        return data


