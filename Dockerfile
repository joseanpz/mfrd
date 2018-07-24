FROM python:3.6.6-jessie
COPY . /app
WORKDIR /app
RUN mkdir logs
RUN pip install -r requirements.txt
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000"]