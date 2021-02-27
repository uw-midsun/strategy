import sys
import os.path
from routes import build_routes_points, format_routes_query,parse_routing_data
from common import get_API_data
from config import BASE_URL, API_KEY
sys.path.append(os.path.dirname(__file__))

def Time_to(speed: int,curLat: float, curLon: float, finLat: float, finLon: float ):
    params = build_routes_points([{curLat:curLon},{finLat:finLon}])
    query = format_routes_query(params)
    jasonFile = get_API_data(query)
    route_df = parse_routing_data(jasonFile)
    return route_df.get('Distance to Manuever') / speed 
    
    
    
    




