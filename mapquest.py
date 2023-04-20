import urllib.parse
import requests

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "3vVAToG1jRZVLBtLMDdyciN3z2jmpgen"

# Loop to get user inputs and fetch directions
while True:
    # Get origin location input
    orig = input("Starting Location: ")
    if orig == "quit" or orig == "q":
        break
    # Get destination inputs
    dest_list = []
    while True:
        dest = input("Enter Destination (type 'done' when finished): ")
        if dest == "quit" or dest == "q" or dest == "done":
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