from fastapi import FastAPI
import random
from datetime import datetime
from dotenv import load_dotenv
import os
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()
load_dotenv("./.env")  # take environment variables from .env.

# MongoDB connection details
MONGO_DETAILS = os.getenv("MONGODB_URI")  # Example: "mongodb://localhost:27017"
MONGO_DBNAME= os.getenv("MONGODB_NAME")  # Example: "mydatabase"

# MongoDB client and database
client = AsyncIOMotorClient(MONGO_DETAILS)
db = client.get_database(MONGO_DBNAME)  # Replace with your DB name if needed
questions_collection = db.questions


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
            "name": "Route 66",
            "timestamp": datetime.now().isoformat(),
            "city": "New York"
        },
         {
            "_id": 3,
            "name": "Route 101",
            "timestamp": datetime.now().isoformat(),
            "city": "London"
        },
         {
            "_id": 4,
            "name": "Route 53",
            "timestamp": datetime.now().isoformat(),
            "city": "Paris"
        }
    ]

    return {"body": routes}

def aiQuestion(prompt):
    return "What is the capital of France?"


@app.get("/api/generateQuestion")
async def getQuestions():

    # get all questions
    questions = await questions_collection.find().to_list(length=1000)

    for questionIndex in range(0, len(questions)):
        if questions[questionIndex]['aiGeneratedQuestion'] == True:
             questions[questionIndex]['questionText']  = aiQuestion(questions[questionIndex]['prompt'])   
        
     ## convert list to string
    questionString = str(questions)

    #return all questions as json
    return {"body": questionString}