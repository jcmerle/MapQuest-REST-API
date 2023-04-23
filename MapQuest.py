import urllib.parse
import requests

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "s289RKzpSiXWCRJhHUWeQy9AuxwxlY3k"

route_option = ""
user_avoids_option = []
user_disallows_options = []
avoids_option = []
disallows_options = []
walkingSpeed = 2.5

unit_choice = "k" #by default

def unitconf():
    print("What unit system should be used to display distance?")
    while True:
        unit_choice = str(input("Type in 'km' for kilometers or 'mi' for miles.\n"))
        if unit_choice == "km":
            print("Unit changed to kilometers.")
            unit_choice= "k"
            break
        if unit_choice == "mi":
            print("Unit changed to miles.")
            unit_choice= "m"
            break
        else:
            print("Unit not recognized. Kilometers will be used as default settings.")
            unit_choice= "m"
            break

def printParams(name, params):
    print("route type to " + name + ":")
    if params == []:
        print(" - none")
    for elem in params:
        print(" - " + elem)


def roadConf(name, param, avoids, disallows):
    while True:
        choice = input(
name + " behavior:\n\
    - '0' : accept (default)\n\
    - '1' : avoid\n\
    - '2' : disallow\n\
$> ")
        if (choice == "0" or choice == "1" or choice == "2" or choice == ""):
            break
    if choice == "1":
        avoids.append(param)
    if choice == "2":
        disallows.append(param)

def carBasicConfig(avoid, disallows):
    roadConf("Limited access road (highways)", "Limited Access", avoid, disallows)
    roadConf("Toll road", "Toll Road", avoid, disallows)

def carExtendedConfig(avoid, disallows):
    carBasicConfig(avoid, disallows)
    roadConf("Unpaved road", "Unpaved", avoid, disallows)
    roadConf("Approximate seasonal closure road", "Approximate Seasonal Closure", avoid, disallows)
    roadConf("Tunnel road", "Tunnel", avoid, disallows)
    roadConf("Bridge road", "Bridge", avoid, disallows)
    roadConf("Country border crossing road", "Country Border Crossing", avoid, disallows)

def carCustomConfig():
    avoids_option = user_avoids_option
    disallows_options = user_disallows_options

def customUserConfig():
    print("[Custom user configuration]")
    carExtendedConfig(user_avoids_option, user_disallows_options)
    avoids_option = user_avoids_option
    disallows_options = user_disallows_options

def printUserConf():
    print("Current user configuration:")
    printParams("avoid", user_avoids_option)
    printParams("disallow", user_disallows_options)

def carOption():
    while True:
        printUserConf()
        choice = input("\
Car route configuration:\n\
    - '0' : No configuration (default)\n\
    - '1' : Custom user configuration\n\
    - '2' : Basic configuration\n\
    - '3' : Extended configuration\n\
    - '4' : Define custom user configuration\n\
$> ")
        if choice == "0" or choice == "1" or choice == "2" or choice == "3" or choice == "4" or choice == "":
            break
    if choice == "0" or choice == "":
        return
    if choice == "1":
        carCustomConfig()
    if choice == "2":
        carBasicConfig(avoids_option, disallows_options)
    if choice == "3":
        carExtendedConfig(avoids_option, disallows_options)
    if choice == "4":
        customUserConfig()

    print("[Your road options]")
    printParams("avoid", user_avoids_option)
    printParams("disallow", user_disallows_options)

def walkingConf():
    while True:
        global walkingSpeed
        choice = input("\
Choose your walking speed:\n\
    -       '0'      : " + str(walkingSpeed) + " (default)\n\
    - '[Your value]' : enter a default value up to 0.42 and under 42\n\
                       you can use a decimal point '.' one number after it (ex: 2.5)\n\
$> ")
        if choice == "" or choice == "0":
            break
        else:
            try:
                temp = float(choice)
                if temp >= 0.42 and temp <= 42.0:
                    walkingSpeed = temp
                    break
                print("/!\ bad value, please refer to the instruction and try again.")
            except:
                print("/!\ bad value, please refer to the instruction and try again.")

def routeOption():
    #Route options
    while True:
        choice = input("\
Enter a route option: \n\
    - '0' : Car with quickest drive time route (default)\n\
    - '1' : Car shortest driving distance route. \n\
    - '2' : Walking\n\
    - '3' : Bicycling\n\
$> ")
        if choice == "0" or choice == "1" or choice == "2" or choice == "3" or choice == "":
            break

    if choice == "0" or choice == "":
        route_option = "fastest"
        carOption()
    if choice == "1":
        route_option = "shortest"
        carOption()
    if choice == "2" :
        route_option = "pedestrian"
        walkingConf()
    if choice == "3" :
        route_option = "bicycle"

    return route_option

def main():

    # Loop to get user inputs and fetch directions
    while True:
        # Get origin location input
        orig = input("Starting Location: ")
        if orig == "quit" or orig == "q":
            break
        if orig == "":
            orig = "Washington, D.C."
        # Get destination inputs
        dest_list = []
        # Get units preferences:
        unitconf()
        while True:
            dest = input("Enter Destination (type 'done' or 'd' when finished): ")
            if dest == "quit" or dest == "q" or dest == "done" or dest == "d":
                break
            if dest == "":
                dest_list.append("Baltimore, Md")
            else:
                dest_list.append(dest)

        if not dest_list: 
            break

        route_option = routeOption()

        # Prepare API request "avoids":avoids_option, "disallows":disallows_options
        url_params = {"key": key, "from": orig, "routeType": route_option, "unit": unit_choice, "disallows": disallows_options, "avoids": avoids_option}
        if route_option == "pedestrian":
            url_params["walkingSpeed"] = walkingSpeed
        for dest in dest_list:
            url_params["to"] = url_params.get("to", []) + [dest]

        # Construct the API request URLs
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

if __name__ == "__main__":
    main()