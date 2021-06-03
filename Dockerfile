
# write some code to build your image

FROM python:3.8.6-buster

# Image
COPY api /api
COPY TaxiFareModel /TaxiFareModel
COPY model.joblib /model.joblib
COPY requirements.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# CMD uvicorn requirements:requirements --host 0.0.0.0 --port $PORT
CMD uvicorn api.fast:app --reload --host 0.0.0.0 --port $PORT