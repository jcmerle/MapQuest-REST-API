import urllib.parse
import requests
from PIL import Image
from io import BytesIO

main_api = "https://www.mapquestapi.com/directions/v2/route?"
static_map_api = "https://www.mapquestapi.com/staticmap/v5/map?"
key = "3vVAToG1jRZVLBtLMDdyciN3z2jmpgen"
map_options = ["map", "dark", "light", "hyb", "sat"]

# Display map function
def display_map(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img.show()
    return response


# Loop to get user inputs and fetch directions
while True:
    # Get origin location input
    orig = input("Starting Location: ")
    if orig == "quit" or orig == "q":
        break
    # Get destination inputs
    dest_list = []
    while True:
        dest = input("Enter Destination (type 'done' or 'd' when finished): ")
        if dest == "quit" or dest == "q" or dest == "done" or dest == "d":
            break
        dest_list.append(dest)

    if not dest_list: 
        break

    # Prepare API request
    url_params = {"key": key, "from": orig}
    for dest in dest_list:
        url_params["to"] = url_params.get("to", []) + [dest]

    # Construct the API request URL
    url = main_api + urllib.parse.urlencode(url_params, doseq=True)
    print("URL: " + (url))
    # Send the API request and parse the JSON response
    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]

    # Prepare map request
    map_type = input("Enter map type (map, hyb, sat, light, dark): ")
    if map_type == "q" or map_type == "quit":
        break
    elif map_type == "":
        map_type = "map"
    while map_type not in map_options:
        map_type = input("Invalid map type, try again : ")
    # Check if there are multiple locations
    if len(dest_list) > 1:
        static_map_params = {
            "key": key,
            "size": "600,400@2x",
            "locations":orig + '||' + '||'.join(map(str,dest_list)),
            "defaultMarker":"marker-num",
            "type": map_type,
            "scalebar":"true",
            "traffic":"flow|cons",
        }
    else:
        static_map_params = {
            "key": key,
            "size": "600,400@2x",
            "start": orig + "|flag-start",
            "end": dest_list[-1] + "|flag-end",
            "type": map_type,
            "scalebar":"true",
            "traffic":"flow|cons",
        }
    # Construct the API request URL
    static_map_url = static_map_api + urllib.parse.urlencode(static_map_params)
    print("Static Map URL: " + static_map_url)

    # Display map
    map_status = display_map(static_map_url)

    if json_status == 0:
        print("API Status: " + str(json_status) + " = A successful route call.\n")
        print("=============================================")
        
        total_duration = 0  # in seconds
        total_distance = 0  # in km
        # Loop through each destination and print directions for each leg
        for i, (dest, leg) in enumerate(zip(dest_list, json_data["route"]["legs"])):
            print(f"Directions from {orig if i == 0 else dest_list[i-1]} to {dest}:")
            print("Trip Duration: " + (leg["formattedTime"]))
            print("Kilometers: " + str("{:.2f}".format((leg["distance"]) * 1.61)))
            print("=============================================")
            # Print the maneuvers for each leg
            for maneuver in leg["maneuvers"]:
                print((maneuver["narrative"]) + " (" + str("{:.2f}".format((maneuver["distance"]) * 1.61)) + " km)")
            print("=============================================\n")
            # Add the leg duration and distance to the total trip duration and distance
            total_duration += leg["time"] 
            total_distance += leg["distance"] * 1.61  
        # Print the total trip duration and distance    
        print("Total Trip Duration: " + "{:02d}:{:02d}:{:02d}".format(total_duration // 3600, (total_duration % 3600) // 60, total_duration % 60))
        print("Total Trip Kilometers: " + str("{:.2f}".format(total_distance))+ "\n")

    
    # Handle other status codes (errors) and print relevant messages        
    elif json_status == 402:
        print("**********************************************")
        print("Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations.")
        print("**********************************************\n")
    elif json_status == 611:
        print("**********************************************")
        print("Status Code: " + str(json_status) + "; Missing an entry for one or both locations.")
        print("**********************************************\n")
    else:
        print("************************************************************************")
        print("For Staus Code: " + str(json_status) + "; Refer to:")
        print("https://developer.mapquest.com/documentation/directions-api/status-codes")
        print("************************************************************************\n")