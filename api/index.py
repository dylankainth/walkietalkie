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
import time
import uuid
from duckduckgo_search import DDGS
import sys
from api.podcastfy.podcastfy import client  # Import the client module
from api.podcastfy.podcastfy.client import generate_podcast
import re
import pathlib
import io
import dotenv
import zipfile
from os.path import basename
import base64


app = FastAPI()
load_dotenv("./.env")  # take environment variables from .env.

#generate actual distance and route between starting and ending point
def generate_route(origin, destination, waypoints, mode, api_key):
    base_url = "https://maps.googleapis.com/maps/api/directions/json"
    param = {
        "origin": f"{origin[0]},{origin[1]}",
        "destination": f"{destination[0]},{destination[1]}",
        "waypoints": "|".join([f"{lat},{lon}" for lat, lon in waypoints]),
        "mode": mode,
        "key": api_key
    }

    response = requests.get(base_url, params = param)  
    result = response.json()

    
    #print(result)

    if result["status"] == "OK":
        try:
            # You can return the route details such as distance and duration here
            legs = result["routes"][0]["legs"]
            # List to hold all the turn-by-turn directions
            turn_by_turn_directions = []

            megaMapArray = []

            # Loop through each leg and step
            for leg in legs:
                for step in leg["steps"]:
                    # Append the instruction (HTML-formatted)
                    turn_by_turn_directions.append(step["html_instructions"])
                    megaMapArray.append([step['start_location'],step['end_location']])
            
            # Return the turn-by-turn directions

            total_distance = sum(leg["distance"]["value"] for leg in legs) / 1000  # Convert to km
            total_duration = sum(leg["duration"]["value"] for leg in legs) / 60  # Convert to minutes

            hours = total_duration//60
            minutes = round(total_duration%60)

            return {  
                "coordinates": megaMapArray,
                "distance": total_distance,
                "duration": total_duration,
                "hours": hours,
                "minutes": minutes
            }
        except (KeyError, IndexError):
            return None
    return None

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

def generatePlaceTypes(qnaText: str):
    systemprompt = f'You are planning a route between places. You must pick 3 place types from the list below to create a route based on a few questions. You must fulfil the wishes of the user based on their answers to the questions. Give your place types in a comma separated list with no other punctuation. Do not output anything else other than this list.\n\nPlace types:\n'
    systemprompt += f'{placetype_liststr}'

    response = openAIClient.chat.completions.create(
        messages=[
            {
            "role": "system",
            "content": systemprompt,
            },
            {
            "role": "user",
            "content": qnaText,
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
    return generated_placetypes

def searchPlaces(generated_placetypes,start_location, end_location, radius):
    middle_location = ((start_location[0] + end_location[0])/2,(start_location[1] + end_location[1])/2)
    responses = {placetype: getPlaces(placetype,middle_location,radius) for placetype in generated_placetypes}

    points = []
    pointsmap = {start_location : 'START', end_location: 'END'}
    for (placetype,typeresponse),_ in zip(responses.items(),range(3)):
        try:
            print(placetype)
            currentType = []
            for place in typeresponse.json()['places']:
                loc = (place['location']['latitude'],place['location']['longitude'])
                if loc not in pointsmap:
                    currentType.append(loc)
                pointsmap[loc] = place['displayName']['text']
                print(f"{place['displayName']['text']} - {loc}")
            if (len(currentType)):
                points.append(currentType)
        except KeyError:
             print(typeresponse.status_code,typeresponse.json())
    return points

@app.post("/api/createRoute")
async def createRoute(request : Request):

    requestData = await request.json()
    startLocation = requestData['startLocation']
    endLocation = requestData['endLocation']
    questionsList = requestData['questionsList']
    radius= requestData['walkingDistance']
    #print(requestData)
    
    start_location = (startLocation['coords']['latitude'],startLocation['coords']['longitude'])
    end_location = (endLocation['coords']['latitude'],endLocation['coords']['longitude'])
    
    qnaText = "\n".join(["Question: "+question['questionText'] + '\n' + "Answer: "+(question['answer'] if type(question['answer']) == str else ", ".join(question['answer'])) for question in questionsList])
    generated_placetypes = generatePlaceTypes(qnaText)
    print(generated_placetypes)
    points = searchPlaces(generated_placetypes,start_location,end_location,radius)
    print(f"Num points: {len(points)}")
    
    
    path,distance = shortest_path_3(start_location,end_location,points,6)
    print("Best Distance: "+str(distance))
    start = path[0]
    waypoint = path[1:-1]
    destination = path[-1]

    route = generate_route(start, destination, waypoint, "walking", GMAPS_API_KEY)
    print(len(route['coordinates']))
    return {"message": "Route created", "route": questionsList}


def search_wikipedia(search_query):
    # Python 3
    # Choose your language, and search for articles.

    language_code = 'en'
    number_of_results = 1
    headers = {
    # 'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
    'User-Agent': 'Walkie Talkie (wtalkie@keanuc.net)'
    }

    base_url = 'https://api.wikimedia.org/core/v1/wikipedia/'
    endpoint = '/search/page'
    url = base_url + language_code + endpoint
    parameters = {'q': search_query, 'limit': number_of_results}
    response = requests.get(url, headers=headers, params=parameters)

    response = json.loads(response.text)

    page_titles = []
    page_urls = []

    for page in response['pages']:
        page_titles.append(page['title'])
        page_urls.append('https://' + language_code + '.wikipedia.org/wiki/' + page['key'])

    most_relevant_page = get_most_relevant_page(search_query, page_titles)

    print(page_titles)
    print(page_urls)
    print(most_relevant_page)

    relevant_page_index = page_titles.index(most_relevant_page)

    print(relevant_page_index)

    return page_urls[relevant_page_index]

def get_most_relevant_page(query, titles):
    prompt = f"Here is a list of Wikipedia page titles: {titles}. Which one is the most relevant to the search query?"

    prompt = f"""
    Task:
    Identify the most relevant Wikipedia article title from the given list based on the search query. Your answer should be returned as a single structured string.

    Search Query: "{query}"
    Wikipedia Titles: {titles}

    Evaluation Criteria:

        Exact Match (30%) – Direct or near match with the query.
        Semantic Similarity (30%) – Does the title capture the same concept, even if phrased differently?
        Wikipedia Naming Conventions (20%) – Would Wikipedia typically use this title?
        Contextual Relevance (20%) – Is this the most likely intended topic?

    Instructions:

        Select the Best Match – Pick the title with the highest relevance score.
        Provide a Confidence Score (0-100%) – Estimate how well the selected title fits the query.
        Rank the Top 3 Matches (if applicable) – If multiple titles are strong candidates, list them.
        Handle Ambiguities – If the query is unclear, suggest refinements.

    Output Format (Single String):
    "Best Match: [Title] (Confidence: X%). Alternative Matches: 1. [Title] (X%), 2. [Title] (X%). Ambiguity Notes: [Explanation, if applicable]."

    If no alternative matches or ambiguity exist, omit those sections.
    """

    # Make the request to OpenAI API
    try:
        response = openAIClient.chat.completions.create(
            model="gpt-4o",  # Use the suitable GPT model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        # Log the full response for debugging

        # Extract the result from the response
        result = response.choices[0].message.content
        if result:
            print("Full AI Response: %s", result)
            result = result.strip()

            match = re.search(r'Best Match: ([^\(]+)', result)
            if match:
                final_result = match.group(1).strip()
                return final_result
            else:
                return ""

    except Exception as e:
        # If parsing or any other error occurs, print the error message and the full response
        print("Error while parsing AI response: %s", e)
        print("Full AI Response: %s", response)  # Log the full response for further analysis
        return ""  # Fallback to empty data

@app.get("/api/createLocationTrack")
def createLocationTrack():

    place_name = "King's College, University of London"

    # Search Wikipedia for URL
    wikipedia_search_url = search_wikipedia(place_name)
    if wikipedia_search_url == "":
        return {"message": "No Wikipedia results found"}

    print(wikipedia_search_url)
    
    # Search DuckDuckGo
    # search_results = DDGS().text(place_name, max_results=5)
    # if not search_results:
    #     return {"message": "No Wikipedia results found"}

    # Aggregate URLs
    #+ [result['href'] for result in search_results]

    # Generate podcast
    audio_file, transcript_file = generate_podcast(urls=[wikipedia_search_url], tts_model='elevenlabs')

    #read the transcript file as json
    with open(transcript_file) as f:
        transcriptData = json.load(f)
    
    #return the audio file as a base64 string
    with open(audio_file, "rb") as audio:
        audioData = base64.b64encode(audio.read()).decode("utf-8")

    return {"data": {
        "audio_file": audioData,
        "transcript_file": transcriptData
    }}