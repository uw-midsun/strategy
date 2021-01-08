# Routemodel

A directory for modelling the routes the car will take, including information on elevations, navigations, and speedlimits.

## In this directory

### Data Retrieval Module

Connects and receives responses from Bing Maps APIs to form route / navigation and elevations profile.

+ `routes.py`: Methods to query Routes endpoint, collecting information on latitude, longitude, maneuver instructions, distance to maneuver, distance, and street
+ `elevations.py`: Methods to query Elevations endpoint, forming an elevation profile from a set of coordinates
+ `speedlimits.py`: Methods to query Routes endpoint, collecting information around speed limit changes. Separate call from `routes.py` due to specific route points constraints.

### Routes Module

Information on routes, previous and prospective.

+ ASC2021: Prospective, Santa Fe trail investigation
+ ASC2018
+ Heartland: Prospective, FSGP 2021 location

### Tests Module

Tests routemodel modules. To run tests, run command `pytest` in command prompt when in routemodel directory.
