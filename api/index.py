from fastapi import FastAPI
import random
from datetime import datetime
from dotenv import load_dotenv
import os
from motor.motor_asyncio import AsyncIOMotorClient
import json
from openai import OpenAI

app = FastAPI()
load_dotenv("./.env")  # take environment variables from .env.

# MongoDB connection details
MONGO_DETAILS = os.getenv("MONGODB_URI")  # Example: "mongodb://localhost:27017"
MONGO_DBNAME= os.getenv("MONGODB_NAME")  # Example: "mydatabase"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# MongoDB client and database
client = AsyncIOMotorClient(MONGO_DETAILS)
openAIClient = OpenAI(api_key=OPENAI_API_KEY)
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

def getPlaceTypes():
    placetypes = """art_gallery
    art_studio
    auditorium
    cultural_landmark
    historical_place
    monument
    museum
    performing_arts_theater
    sculpture
    library
    adventure_sports_center
    amphitheatre
    amusement_center
    amusement_park
    aquarium
    banquet_hall
    barbecue_area
    botanical_garden
    bowling_alley
    casino
    childrens_camp
    comedy_club
    community_center
    concert_hall
    convention_center
    cultural_center
    cycling_park
    dance_hall
    dog_park
    event_venue
    ferris_wheel
    garden
    hiking_area
    historical_landmark
    internet_cafe
    karaoke
    marina
    movie_rental
    movie_theater
    national_park
    night_club
    observation_deck
    off_roading_area
    opera_house
    park
    philharmonic_hall
    picnic_ground
    planetarium
    plaza
    roller_coaster
    skateboard_park
    state_park
    tourist_attraction
    video_arcade
    visitor_center
    water_park
    wedding_venue
    wildlife_park
    wildlife_refuge
    zoo
    acai_shop
    afghani_restaurant
    african_restaurant
    american_restaurant
    asian_restaurant
    bagel_shop
    bakery
    bar
    bar_and_grill
    barbecue_restaurant
    brazilian_restaurant
    breakfast_restaurant
    brunch_restaurant
    buffet_restaurant
    cafe
    cafeteria
    candy_store
    cat_cafe
    chinese_restaurant
    chocolate_factory
    chocolate_shop
    coffee_shop
    confectionery
    deli
    dessert_restaurant
    dessert_shop
    diner
    dog_cafe
    donut_shop
    fast_food_restaurant
    fine_dining_restaurant
    food_court
    french_restaurant
    greek_restaurant
    hamburger_restaurant
    ice_cream_shop
    indian_restaurant
    indonesian_restaurant
    italian_restaurant
    japanese_restaurant
    juice_shop
    korean_restaurant
    lebanese_restaurant
    meal_delivery
    meal_takeaway
    mediterranean_restaurant
    mexican_restaurant
    middle_eastern_restaurant
    pizza_restaurant
    pub
    ramen_restaurant
    restaurant
    sandwich_shop
    seafood_restaurant
    spanish_restaurant
    steak_house
    sushi_restaurant
    tea_house
    thai_restaurant
    turkish_restaurant
    vegan_restaurant
    vegetarian_restaurant
    vietnamese_restaurant
    wine_bar
    beach
    place_of_worship
    asian_grocery_store
    auto_parts_store
    bicycle_store
    book_store
    butcher_shop
    cell_phone_store
    clothing_store
    convenience_store
    department_store
    discount_store
    electronics_store
    food_store
    furniture_store
    gift_shop
    grocery_store
    hardware_store
    home_goods_store	
    home_improvement_store
    jewelry_store
    liquor_store
    market
    pet_store
    shoe_store
    shopping_mall
    sporting_goods_store
    store
    supermarket
    warehouse_store
    wholesaler
    arena
    athletic_field
    fishing_charter
    fishing_pond
    fitness_center
    golf_course
    gym
    ice_skating_rink
    playground
    ski_resort
    sports_activity_location
    sports_club
    sports_coaching
    sports_complex
    stadium
    swimming_pool"""
    placetypes = placetypes.splitlines()
    placetypes = {" ".join([word.capitalize() for word in placetype.split("_")]) : placetype for placetype in placetypes}
    return placetypes


def aiQuestion(seed: int ,staticQuestions: list):

    print("seed: ", seed)
    #print("staticQuestions: ", staticQuestions)
    placetypeliststr = "\n".join(getPlaceTypes().keys())
    systemprompt = f'You are trying to help the user plan a route between places. The user will provide some sample questions to narrow down the place types they want to visit. Write 1 more sample question that can help narrow down the place types. Respond only a new sample question ending with a "?".\n\nPossible place types:\n'
    systemprompt += f'{placetypeliststr}'
    userprompt = "Sample questions:\n"
    userprompt += "\n".join((question['questionText'] for question in staticQuestions))
    
    response = openAIClient.chat.completions.create(
        messages=[
            {
            "role": "system",
            "content": systemprompt,
            },
            {
            "role": "user",
            "content": userprompt,
            },
        ],
        model="gpt-4o-mini",
        max_completion_tokens=50,
        seed=seed
    )
    output = response.choices[0].message.content.strip()
    return output


@app.get("/api/generateQuestions")
async def getQuestions():

    # get all questions
    questions = await questions_collection.find().to_list(length=1000)

    staticQuestions= []
    # get questions where aiGeneratedQuestion is false
    for questionIndex in range(0, len(questions)):
        if questions[questionIndex]['aiGeneratedQuestion'] == False:
            staticQuestions.append(questions[questionIndex])

    for questionIndex in range(0, len(questions)):
        if questions[questionIndex]['aiGeneratedQuestion'] == True:
             questions[questionIndex]['questionText']  = aiQuestion(questions[questionIndex]['seed'], staticQuestions)   
        
    #return all questions as json
    for question in questions:
        question['_id'] = str(question['_id'])

    return {"body": questions}

@app.post("/api/createRoute")
def createRoute(questionsList: dict):
    print(questionsList)
    return {"message": "Route created", "route": questionsList}