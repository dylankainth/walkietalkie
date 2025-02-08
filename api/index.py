from fastapi import FastAPI, Request
import random
from datetime import datetime
from dotenv import load_dotenv
import os
from motor.motor_asyncio import AsyncIOMotorClient
import json
from openai import OpenAI
from math import sin, cos, sqrt, atan2, radians
from itertools import permutations, product, combinations
import requests



#get straight line distance between two coordinates
def distanceKm(coord1,coord2):
    # Approximate radius of earth in km
    R = 6373.0

    lat1 = radians(coord1[0])
    lon1 = radians(coord1[1])
    lat2 = radians(coord2[0])
    lon2 = radians(coord2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

#shortest path for 1 group
def shortest_path_one_group(start, end, groups):
    """Finds the shortest path from start to end, passing through one point from a single group."""
    min_distance = float('inf')
    best_path = None

    # Iterate over each group
    for group in groups:
        # Iterate over each point in the selected group
        for point in group:
            # Compute total distance: Start → Chosen Point → End
            distance = distanceKm(start, point) + distanceKm(point, end)

            # Update shortest path if found
            if distance < min_distance:
                min_distance = distance
                best_path = [start, point, end]

    return min_distance, best_path

#shortest path for 2 groups
def shortest_path_2(start, end, groups):
    """Finds the shortest path from start to end, choosing one point from two of the three groups."""
    min_distance = float('inf')
    best_path = None

    # Select 2 out of the 3 groups
    for group_indices in combinations(range(len(groups)), 2):
        selected_groups = [groups[i] for i in group_indices]

        # Pick one point from each of the selected 2 groups
        for selection in product(*selected_groups):
            # Generate all orderings of the selected points
            for perm in permutations(selection):
                # Compute total distance: Start → P1 → P2 → End
                distance = distanceKm(start, perm[0]) + distanceKm(perm[0], perm[1]) + distanceKm(perm[1], end)

                # Update shortest path if found
                if distance < min_distance:
                    min_distance = distance
                    best_path = [start] + list(perm) + [end]

    return min_distance, best_path


#shortest path for 3 groups
def shortest_path_3(start,end,groups,expected_distance):
    min_distance = float('inf')
    best_path = None
    
    # Generate all possible selections (one point per group)
    for selection in product(*groups):
        # Generate all permutations of the selected points
        for perm in permutations(selection):
            # Compute path distance
            distance = sum(distanceKm(perm[i], perm[i+1]) for i in range(len(perm)-1))
            distance += distanceKm(start,perm[0])
            distance += distanceKm(perm[len(perm)-1],end)
            if distance < min_distance:
                min_distance = distance
                best_path = perm
    #if the path containing all 3 groups is too long
    if expected_distance < min_distance:
        min_distance,best_path = shortest_path_2(start,end,groups)
        #if path containing 2 groups is too long
        if min_distance > expected_distance:
            min_distance,best_path = shortest_path_one_group(start,end,groups)
    return best_path,min_distance

app = FastAPI()
load_dotenv("./.env")  # take environment variables from .env.

# MongoDB connection details
MONGO_DETAILS = os.getenv("MONGODB_URI")  # Example: "mongodb://localhost:27017"
MONGO_DBNAME= os.getenv("MONGODB_NAME")  # Example: "mydatabase"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GMAPS_API_KEY = os.getenv("GMAPS_API_KEY")
# MongoDB client and database
client = AsyncIOMotorClient(MONGO_DETAILS)
openAIClient = OpenAI(api_key=OPENAI_API_KEY)
db = client.get_database(MONGO_DBNAME)  # Replace with your DB name if needed
questions_collection = db.questions


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
    placetypes = {" ".join([word.strip().capitalize() for word in placetype.strip().split("_")]) : placetype.strip() for placetype in placetypes}
    return placetypes

placetype_dict = getPlaceTypes()
placetype_liststr = "\n".join(placetype_dict.keys())


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




def aiQuestion(seed: int ,staticQuestions: list):
    return "Are you looking for indoor or outdoor activities?"
    print("seed: ", seed)
    #print("staticQuestions: ", staticQuestions)
    
    systemprompt = f'You are trying to help the user plan a route between places. The user will provide some sample questions to narrow down the place types they want to visit. Write 1 more sample question that can help narrow down the place types. Respond only a new sample question ending with a "?".\n\nPossible place types:\n'
    systemprompt += f'{placetype_liststr}'
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

@app.get("/api/testShortest3")
def testShortest3():
    path,distance = shortest_path_3(start_location,end_location,points,6)
    print(path)
    print(distance)

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



def getPlaces(placeType: str,middle_location,radius):
    url = f"https://places.googleapis.com/v1/places:searchNearby"

    # Define the parameters for the request

    data = {"includedTypes": [placeType],
            "maxResultCount": 3,
            "locationRestriction": {
                "circle": {
                    "center": {
                        "latitude": middle_location[0],
                        "longitude": middle_location[1]
                        },
                    "radius": radius}
                }
            }

    headers = {
        'X-Goog-FieldMask': '*',#'places.id,places.displayName,places.location',
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GMAPS_API_KEY,
    }

    # Send the request to the Google Places API
    response = requests.post(url,headers=headers,data=json.dumps(data))
    return response


@app.post("/api/createRoute")
async def createRoute(request : Request):
    requestData = await request.json()
    startLocation = requestData['startLocation']
    endLocation = requestData['endLocation']
    questionsList = requestData['questionsList']
    print(requestData)
    
    start_location = (startLocation['coords']['latitude'],startLocation['coords']['longitude'])
    end_location = (endLocation['coords']['latitude'],endLocation['coords']['longitude'])
    radius= 2000

    systemprompt = f'You are planning a route between places. You must pick 3 place types from the list below to create a route based on a few questions. You must fulfil the wishes of the user based on their answers to the questions. Give your place types in a comma separated list with no other punctuation. Do not output anything else other than this list.\n\nPlace types:\n'
    systemprompt += f'{placetype_liststr}'
    userprompt = "\n".join(["Question: "+question['questionText'] + '\n' + "Answer: "+(question['answer'] if type(question['answer']) == str else ", ".join(question['answer'])) for question in questionsList])
    #print(userprompt)
    #print(systemprompt)
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
        max_completion_tokens=100
    )
    
    genMsg = response.choices[0].message.content.strip()
    generated_placetypes = set()
    for placetype in (placetype.strip() for placetype in genMsg.split(",")):
        placetypename = placetype_dict.get(placetype)
        if placetypename != None:
            generated_placetypes.add(placetypename)
    print(generated_placetypes)

    middle_location = ((start_location[0] + end_location[0])/2,(start_location[1] + end_location[1])/2)
    responses = {placetype: getPlaces(placetype,middle_location,radius) for placetype in generated_placetypes}

    points = []
    pointsmap = {start_location : 'START', end_location: 'END'}
    for (placetype,typeresponse),_ in zip(responses.items(),range(3)):
        try:
            points.append([(place['location']['latitude'],place['location']['longitude']) for place in typeresponse.json()['places']])
            print(placetype)
            for place in typeresponse.json()['places']:
                pointsmap[(place['location']['latitude'],place['location']['longitude'])] = place['displayName']['text']
                print(f"{place['displayName']['text']} - {(place['location']['latitude'],place['location']['longitude'])}")
        except KeyError:
             print(typeresponse.status_code,typeresponse.json())

    return {"message": "Route created", "route": questionsList}