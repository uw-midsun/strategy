import requests
import sys
import os.path

sys.path.append(os.path.dirname(__file__))

from config import BASE_URL, API_KEY

# common getter for all files
def get_API_data(query: str):
    """
    @param query: formatted query to be requested from API
    #return: a JSON response from API
    """
    url = BASE_URL + query
    url += '&key={}'.format(API_KEY)
     # get and return response
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print("An error occured:", 
              err.response.json()['statusCode'],
              "\nAuthentication Result:",
              err.response.json()['authenticationResultCode'],
              "\nMessage:", 
              err.response.json()['errorDetails'][0])
        sys.exit()
    return response.json()

# TODO: build a common SQLite connection/insert function