# Modelling Routes and Elevations

**Description:** A directory for modelling the routes the car will take, such as the elevation difference, navigation steps, and *velocity restrictions (WIP)*

## Data Retrieval Module

Connects and receives responses from Bing Maps APIs to form route / navigation and elevations profile.

### Navigation

Retrieves data from Bing Maps API pertaining to navigation of route.

1. Initialization parameters
   - REQUIRED: List of Major Checkpoints along route - also called "waypoints"
     - enter list of at least 2 waypoints for request to return a good response with usable data
       - waypoints can only be coordinates as of now: each index of the list will be a dict of a latitude and longitude, the latitude being the key
   - OPTIONAL: List of Minor Checkpoints along route - also called "viawaypoints"
     - enter list of list of coordinates only, with each index of the inner list being a dict of coordinates similar to the above
     - can be left empty
   - OPTIONAL: Distance unit
     - string 'km' or 'mi'
     - defaults to km
   - OPTIONAL: Route attribute
     - specifies the structure and types of data to be returned by the API
     - defaults to 'routePath'

2. Methods
   - *get_navigation_data():* method to request data from API using initialization parameters. No parameters to be entered.
   - *parse_navigation_data():*  method to parse through API response object. Pass in response from above getter into method call.

### Elevations

Retrieves data from Bing Maps API pertaining to elevations profile of given route.

1. Initialization parameters
   - REQUIRED: List of Major Checkpoints along route - also called "waypoints"
     - enter list of at least 2 waypoints for request to return a good response with usable data
       - waypoints can only be coordinates as of now: each index of the list will be a dict of a latitude and longitude, the latitude being the key
   - OPTIONAL: List of Minor Checkpoints along route - also called "viawaypoints"
     - enter list of list of coordinates only, with each index of the inner list being a dict of coordinates similar to the above
     - can be left empty (optional)
   - OPTIONAL: Height
     - type of model used to calculate elevations of route
     - defaults to 'sealevel' -> this model calculates elevation using the sealevel as the base

2. Methods
   - *get_elevation_data():* method to request data from API using initialization parameters. No parameters to be entered.
   - *parse_elevation_data():*  method to parse through API response object. Pass in response from above getter into method call.

## Routes Module

## Tests Module

Tests routemodel modules. To run tests, run command `pytest` in command prompt when in routemodel directory.
