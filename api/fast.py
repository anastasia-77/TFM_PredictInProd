from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import pytz
import pandas as pd
import joblib

#---CORS 'Cross-Origin Resource Sharing' allow API to be quite open
# and to allow developers to plug it in the code,
# that is going to run inside of a browser.

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

#--- Create a root endpoint to welcome the developers using our API.
@app.get("/")
def index():
    return {"greeting": "Hello world"}


@app.get("/predict_test")
def predict_test(pickup_datetime,
            pickup_longitude,
            pickup_latitude,
            dropoff_longitude,
            dropoff_latitude,
            passenger_count):

    return {
            "pickup_datetime": "2013-07-06 17:18:00",
            "pickup_longitude": "-73.950655",
            "pickup_latitude": "40.783282",
            "dropoff_longitude": "-73.984365",
            "dropoff_latitude": "40.769802",
            "passenger_count": "1"
            }

# ---Create an API predict
@app.get("/predict")
def predict(
                pickup_datetime,
                pickup_longitude,
                pickup_latitude,
                dropoff_longitude,
                dropoff_latitude,
                passenger_count):

    # create a datetime object from the user provided datetime
    pickup_datetime = datetime.strptime(pickup_datetime, "%Y-%m-%d %H:%M:%S")
    # localize the user datetime with NYC timezone
    eastern = pytz.timezone("US/Eastern")
    localized_pickup_datetime = eastern.localize(pickup_datetime, is_dst=None)
    # localize the datetime to UTC
    utc_pickup_datetime = localized_pickup_datetime.astimezone(pytz.utc)
    # convert to object from datetime64
    formatted_pickup_datetime = utc_pickup_datetime.strftime("%Y-%m-%d %H:%M:%S UTC")
    
    #convert float


     
    # predict with users values ---> df
    X_pred = pd.DataFrame(data = [['2021-06-03 14:00:00.00',
                                    formatted_pickup_datetime,
                                    pickup_longitude, #float(pickup_longitude)
                                    pickup_latitude,
                                    dropoff_longitude,
                                    dropoff_latitude,
                                    passenger_count
                                    ]],
                        columns=['key',
                                'pickup_datetime',
                                'pickup_longitude',
                                'pickup_latitude',
                                'dropoff_longitude',
                                'dropoff_latitude',
                                'passenger_count'
                                ])

    # load a model model.joblib trained locally
    pipeline = joblib.load('model.joblib')
    
    # need a predict function
    res = pipeline.predict(X_pred)

    # return type: dict
    return {'prediction' : res[0]}


