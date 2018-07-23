

class InformacionBuroModel(object):
    """
    Modelo de Infromación de buró usado para diagnosticar la posibilidad de presencia fraude en un cliente
    """

    def __init__(self, CONSULTAS_U02M_SBCBR=None, MOP_MAXIMO_U24M_SERVSGRALES=None,
                 PCT_DIR_JALGTO=None, PCT_APERTURAS_U18M=None, PCT_APERTURAS_ANT_REGBC=None,
                 PCT_CTAS_BANCARIAS=None, PCT_CTAS_SERVS_GRALES=None, PROM_LIMCRE_MAXCRE_SERVSGRALES=None,
                 PCT_ALERTAS_JUICIOS=None, UNIVERSO_11=None):
        """

        :param CONSULTAS_U02M_SBCBR:
        :param MOP_MAXIMO_U24M_SERVSGRALES:
        :param PCT_DIR_JALGTO:
        :param PCT_APERTURAS_U18M:
        :param PCT_APERTURAS_ANT_REGBC:
        :param PCT_CTAS_BANCARIAS:
        :param PCT_CTAS_SERVS_GRALES:
        :param PROM_LIMCRE_MAXCRE_SERVSGRALES:
        :param PCT_ALERTAS_JUICIOS:
        :param UNIVERSO_11:
        """

        self._CONSULTAS_U02M_SBCBR = CONSULTAS_U02M_SBCBR
        self._MOP_MAXIMO_U24M_SERVSGRALES = MOP_MAXIMO_U24M_SERVSGRALES
        self._PCT_DIR_JALGTO = PCT_DIR_JALGTO
        self._PCT_APERTURAS_U18M = PCT_APERTURAS_U18M
        self._PCT_APERTURAS_ANT_REGBC = PCT_APERTURAS_ANT_REGBC
        self._PCT_CTAS_BANCARIAS = PCT_CTAS_BANCARIAS
        self._PCT_CTAS_SERVS_GRALES = PCT_CTAS_SERVS_GRALES
        self._PROM_LIMCRE_MAXCRE_SERVSGRALES = PROM_LIMCRE_MAXCRE_SERVSGRALES
        self._PCT_ALERTAS_JUICIOS = PCT_ALERTAS_JUICIOS
        self._UNIVERSO_11 = UNIVERSO_11
