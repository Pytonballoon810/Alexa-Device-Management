"""
This script is used to interact with the Amazon Alexa API.

It contains two main functions: `get_entities` and `delete_entities`.

`get_entities` sends a GET request to the specified URL to retrieve entities related to the Amazon Alexa skill.
The response from the GET request is printed to the console and saved to a JSON file if it's not empty.

`delete_entities` sends a DELETE request to the specified URL to remove entities related to the Amazon Alexa skill.
The response from each DELETE request is printed to the console.

The script uses predefined headers and parameters for the requests, which are defined as global variables at the top of the script.

This script is intended to be run as a standalone file. When run, it first calls `get_entities` to retrieve the entities, 
and then calls `delete_entities` to delete them.
"""
import json
import time # only needed if you want to add a delay between each delete request
import requests

DATA_FILE = "data.json"
USE_DIFFERENT_GET_AND_DELETE_COOKIES = True
HOST = "eu-api-alexa.amazon.de" # maybe change this to your host... dont know if this is necessary

GET_COOKIE = "" # should look something like this: 'at-acbde="Atza|somereallylongtring";csrf=somenumber;sess-at-acbde="ashorterstring";session-id=threenumbers;ubid-acbde=alsothreenumbers;x-acbde="anotherstring"'
GET_X_AMZN_REQUESTID = "" # should look something like this: 'five-long-strings-separated-dashes'
GET_X_AMZN_ALEXA_APP = "" # should look something like this: 'justareallyreallylongstring'

CSRF = "" # should look something like this: 'somenumber'; not sure if this is the same as in the GET_COOKIE or DELETE_COOKIE argument
# NOTE: not tested if these are necessary. I used two different cookies for the get and delete request due to testing. If using the same as aboove leave these empty and set USE_DIFFERENT_GET_AND_DELETE_COOKIES to False
DELETE_COOKIE = "" # should look something like this: 'at-acbde="Atza|somereallylongtring";csrf=somenumber;sess-at-acbde="ashorterstring";session-id=threenumbers;ubid-acbde=alsothreenumbers;x-acbde="anotherstring"'
DELETE_X_AMZN_REQUESTID = "" # should look something like this: 'five-long-strings-separated-dashes'
DELETE_X_AMZN_ALEXA_APP = "" # should look something like this: 'justareallyreallylongstring'

if not USE_DIFFERENT_GET_AND_DELETE_COOKIES:
    DELETE_COOKIE = GET_COOKIE
    DELETE_X_AMZN_REQUESTID = GET_X_AMZN_REQUESTID
    DELETE_X_AMZN_ALEXA_APP = GET_X_AMZN_ALEXA_APP

def get_entities(url = "https://eu-api-alexa.amazon.de/api/behaviors/entities?skillId=amzn1.ask.1p.smarthome"): # maybe change this to your url... dont know if this is necessary
    """
    Sends a GET request to the specified URL to retrieve entities related to the Amazon Alexa skill.

    The method uses predefined headers and parameters for the request, and saves the response to a JSON file if it's not empty.

    Args:
        url (str, optional): The URL to send the GET request to. Defaults to "https://eu-api-alexa.amazon.de/api/behaviors/entities?skillId=amzn1.ask.1p.smarthome".

    Returns:
        None. The response from the GET request is printed to the console and saved to a JSON file if it's not empty.
    """
    GET_HEADERS = {
        "Host": HOST, 
        "Cookie": GET_COOKIE,
        "Connection": "keep-alive",
        "x-amzn-RequestId": GET_X_AMZN_REQUESTID,
        "x-amzn-alexa-app": GET_X_AMZN_ALEXA_APP,
        "Accept": "application/json; charset=utf-8",
        "User-Agent": "AppleWebKit PitanguiBridge/2.2.580942.0-[HARDWARE=iPhone13_4][SOFTWARE=17.1.2][DEVICE=iPhone]", # maybe change this to your device... dont know if this is necessary
        "Accept-Language": "de-DE,de-DE;q=1.0,en-DE;q=0.9", # maybe change this to your language... dont know if this is necessary
        "Routines-Version": "3.0.194870", # maybe change this to your version... dont know if this is necessary
        "Accept-Encoding": "gzip, deflate, br"
    }

    parameters = {
        "skillId": "amzn1.ask.1p.smarthome"
    }

    response = requests.get(url, headers=GET_HEADERS, params=parameters, timeout=15)

    print(response.text, response.status_code)

    if response.text.strip():
        # Convert the response content to JSON
        response_json = response.json()

        # Open a file for writing
        with open(DATA_FILE, 'w', encoding="utf_8") as file:
            # Write the JSON data to the file
            json.dump(response_json, file)
    else:
        print("Empty response received from server.")

def delte_entities(delete_cookie = DELETE_COOKIE):
    """
    Sends a DELETE request to the specified URL to remove entities related to the Amazon Alexa skill.

    The method uses predefined headers for the request. It reads entity data from a JSON file, and for each entity, 
    it constructs a URL and sends a DELETE request to that URL.

    Args:
        delete_cookie (str, optional): The cookie to be used in the request headers. Defaults to DELETE_COOKIE.

    Returns:
        None. The response from each DELETE request is printed to the console.
    """
    DELTE_HEADERS = {
    "Host": HOST, 
    "Content-Length": "0",
    "x-amzn-RequestId": DELETE_X_AMZN_REQUESTID,
    "x-amzn-alexa-app": DELETE_X_AMZN_ALEXA_APP,
    "Connection": "keep-alive",
    "Accept": "application/json; charset=utf-8",
    "User-Agent": "AppleWebKit PitanguiBridge/2.2.580942.0-[HARDWARE=iPhone13_4][SOFTWARE=17.1.2][DEVICE=iPhone]", # maybe change this to your device... dont know if this is necessary
    "Accept-Language": "de-DE,de-DE;q=1.0,en-DE;q=0.9", # maybe change this to your language... dont know if this is necessary
    "csrf": CSRF,
    "Accept-Encoding": "gzip, deflate, br",
    "Cookie": delete_cookie} 
    # Open the file for reading
    with open(DATA_FILE, 'r', encoding="utf_8") as file:
        # Load the JSON data from the file
        response_json = json.load(file)
        for item in response_json:
            name = str(item["description"]).replace("switch.", "").split(" ", maxsplit=1)[0]
            device_type = str(item["description"]).replace("switch.", "").split(".", maxsplit=1)[0].lower()
            manufacturer = "".join(str(item["description"]).split(" ")[-2:]).lower()
            print(name, manufacturer)
            if manufacturer.lower() == "homeassistant": # you are free to change this to the manufacturer you want to delete from. I used it to only delete entities integrated via the home assistant custom skill; this will most definitely be different if you do want to delete devices not integrated via Home Assistant 
                name = name.lower().replace(" ", "_")
                url = f"__URL__%3D%3D_{device_type}%23{name}" # replace __URL__ with the url you got from the http catcher. Should look something like this: https://eu-api-alexa.amazon.de/api/phoenix/appliance/SKILL_a_really_long_string_probably_the_skill_id%3D%3D

                response = requests.delete(url, headers=DELTE_HEADERS, timeout=10)

                print(name)
                print("\t", response.status_code, response.text)
                # uncomment the following line if you want to add a delay between each delete request
                # time.sleep(.2)

if __name__ == "__main__":
    get_entities()
    delte_entities()
            
