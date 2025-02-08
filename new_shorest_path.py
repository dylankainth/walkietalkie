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
start_location = (51.49803, -0.09012700) #gdsa
end_location = (51.518821,-0.1304266) #british museum
points = [
[(51.5155932, -0.09171789999999999),(51.5155471, -0.0914547), (51.5191136, -0.09429499999999999)],
[(51.508039, -0.128069),(51.508075999999996, -0.09719399999999999),(51.512045, -0.12282539999999999)],
 [(51.500842999999996, -0.126432), (51.5051561,-0.1337215),(51.5044918, -0.1295188)]]

path,distance = shortest_path_3(start_location,end_location,points,6)
print(path)
print(distance)
start = path[0]
waypoint = path[1:-1]
destination = path[-1]

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


directions = generate_route(start,destination,waypoint,"walking",API_KEY)
print(directions['coordinates'])