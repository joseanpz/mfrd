# Modelo de Riesgo de Fraude
Se recomienda instalar ambiente virtual con python 3.6+. Para instalar requerimintos ejecutar
```
pip install -r requirements.txt
```
Para correr el servicio en desarrollo ejecutar el comando
```
python app.py
```
Para correr el servicio en un servidor de aplicaciones wsgi ejecutar
```
gunicorn app:app -b 0.0.0.0:5000
```
