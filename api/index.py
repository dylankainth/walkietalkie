from fastapi import FastAPI
import random
from datetime import datetime
app = FastAPI()

@app.get("/api")
def hello_world():
    return {"message": "Hello World", "api": "Python"}

@app.get("/api/getRoutes")
def getRoutes():

    routes = [
        {
            "_id": 1,
            "name": "Route 1",
            "timestamp": datetime.now().isoformat(),
            "city": "New York"
        },
         {
            "_id": 2,
            "name": "Route 1",
            "timestamp": datetime.now().isoformat(),
            "city": "New York"
        },
         {
            "_id": 3,
            "name": "Route 1",
            "timestamp": datetime.now().isoformat(),
            "city": "London"
        },
         {
            "_id": 4,
            "name": "Route 1",
            "timestamp": datetime.now().isoformat(),
            "city": "Paris"
        }
    ]

    return {"body": routes}