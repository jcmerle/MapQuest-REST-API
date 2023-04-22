import urllib.parse
import requests

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "3vVAToG1jRZVLBtLMDdyciN3z2jmpgen"

# Loop to get user inputs and fetch directions
while True:
    # Get origin location input
    type_of_input = input("name for using place's name or coor to using coordinate of places (lat, longitude)\n")
    if type_of_input != "name" and type_of_input != "coor":
        print("you need to choose between name or coordinates")
        break
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

    url_params = {"key": key, "from": orig}
    for dest in dest_list:
        url_params["to"] = url_params.get("to", []) + [dest]

    # Prepare geocoding API request
    url_origin = {"key": key, "location": orig}
    url_dest= {"key": key, "location": dest}


    # Construct the API request URL
    url = main_api + urllib.parse.urlencode(url_params, doseq=True)
    print("URL: " + (url))
    # Send the API request and parse the JSON response
    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]
    print(url_origin)
    # Get coordinates by city name and print it
    if type_of_input == "name":
        print("first dest",  url_dest)
        json_geocoding = requests.get('https://www.mapquestapi.com/geocoding/v1/address?' + urllib.parse.urlencode(url_origin, doseq=True)).json()
        json_geocoding2 = requests.get('https://www.mapquestapi.com/geocoding/v1/address?' + urllib.parse.urlencode(url_dest, doseq=True)).json()
        json_origin_lng = json_geocoding["results"][0]["locations"][0]["latLng"]["lng"]
        json_origin_lat = json_geocoding["results"][0]["locations"][0]["latLng"]["lat"]
        json_dest_lng = json_geocoding2["results"][0]["locations"][0]["latLng"]["lng"]
        json_dest_lat = json_geocoding2["results"][0]["locations"][0]["latLng"]["lat"]

        print("Longitude of origin: " + str(json_origin_lng) + ", Latitude of origin: "+ str(json_origin_lat))
        print("Longitude of final dest: " + str(json_dest_lng) + ", Latitude of dest: "+ str(json_dest_lat))

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
        # print coordinates of destinations if name inputted
        if type_of_input == "name":
            a= 1
            for i, (dest) in enumerate(zip(dest_list)):
                url_dest = {"key": key, "location": dest}
                json_geocoding3 = requests.get('https://www.mapquestapi.com/geocoding/v1/address?' + urllib.parse.urlencode(url_dest, doseq=True)).json()
                json_dest_lng = json_geocoding3["results"][0]["locations"][0]["latLng"]["lng"]
                json_dest_lat = json_geocoding3["results"][0]["locations"][0]["latLng"]["lat"]
                print("Longitude of dest n°"+ str(a) + ": " + str(json_dest_lng) + ", Latitude of dest: " + str(json_dest_lat))
                a = a +1
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