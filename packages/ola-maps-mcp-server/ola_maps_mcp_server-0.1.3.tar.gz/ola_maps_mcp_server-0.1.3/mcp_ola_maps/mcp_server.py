from typing import Any, Dict, Optional
import httpx
import json
from mcp.server.fastmcp import FastMCP

from mcp_ola_maps.mcp_env import config

MCP_SERVER_NAME = "ola-maps-mcp-server"

deps = [
    "python-dotenv",
    "uvicorn",
    "pip-system-certs",
]

# Initialize FastMCP server
mcp = FastMCP(MCP_SERVER_NAME, dependencies=deps)

# Constants
MAPS_BASE_API = "https://api.olamaps.io"
API_KEY = config.get_api_key()

async def make_get_request(url: str, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, Any]] = None) -> dict[str, Any] | None:
    """Make a get request to the respective maps API with proper error handling."""
    if headers is None:
        headers = {"Accept": "application/geo+json"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params, timeout=300.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

async def make_post_request(url: str, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, Any]] = None) -> dict[str, Any] | None:
    """Make a post request to the respective maps API with proper error handling."""
    if headers is None:
        headers = {"Accept": "application/geo+json"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, params=params, timeout=300.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


@mcp.tool()
async def get_geocode(address: str) -> str:
    """Provides probable geographic coordinates and detailed location information including formatted address for the given address as input.

    Args:
        address: string address
    """
    url = f"{MAPS_BASE_API}/places/v1/geocode"
    params = {
        "address": address,
        "api_key": API_KEY,
    }

    data = await make_get_request(url, params=params)

    if data is None or data.get("status", "").lower() != "ok":
        return f"Geocoding failed: {data.get('reason') if data else 'No response from API'}"
           

    results = data.get("geocodingResults", [])
    if not results:
        return "No geocoding results found."
    
    result = results[0]  
    geocode_result = f"""
        location: {result["geometry"]["location"]}
        formatted_address: {result["formatted_address"]}
        place_id: {result["place_id"]}
    """

    return geocode_result.strip()

@mcp.tool()
async def reverse_geocode(location: str) -> str:
    """converts geographic coordinates back into readable addresses or place names.

    Args:
        location: The string format coordinates (lat,lng) of which you want to do the reverse geocoding to get the address. Example: 12.931316595874005,77.61649243443775
    """
    url = f"{MAPS_BASE_API}/places/v1/reverse-geocode"
    params = {
        "latlng": location,
        "api_key": API_KEY,
    }

    data = await make_get_request(url, params=params)

    if data is None or data.get("status", "").lower() != "ok":
        return f"Reverse Geocoding failed: {data.get('error_message') if data else 'No response from API'}"
           

    result = data["results"][0]
    reverse_geocode_result = f"""{
        "formatted_address": result["formatted_address"],
        "place_id": result["place_id"],
        "address_components": result["address_components"]
    }
    """

    return reverse_geocode_result.strip()

@mcp.tool()
async def get_elevation(location: str) -> str:
    """
    Retrieves elevation data for a single location.

    Args:
        location: The string format coordinates (lat,lng) of which you want to get the elevation. Example: 12.931316595874005,77.61649243443775
    """
    url = f"{MAPS_BASE_API}/places/v1/elevation"
    params = {
        "location": location,
        "api_key": API_KEY,
    }

    data = await make_get_request(url, params=params)

    if data is None or data.get("status", "").lower() != "ok":
        return f"Get Elevation request failed: {data.get('error_message') if data else 'No response from API'}"
           

    result = data["results"][0]
    elevation_result = f"""{
        "elevation": result["elevation"]
    }
    """

    return elevation_result.strip()

@mcp.tool()
async def get_placeDetails(place_id: str) -> str:
    """Provides Place Details of a particular Place/POI whose ola place_id necessarily needs to be given as an input.

    Args:
        place_id: string place ID
    """
    url = f"{MAPS_BASE_API}/places/v1/details"
    params = {
        "place_id": place_id,
        "api_key": API_KEY,
    }

    data = await make_get_request(url, params=params)

    if data is None or data.get("status", "").lower() != "ok":
        return f"Place Details failed: {data.get('reason') if data else 'No response from API'}"
           

    result = data["result"]
    place_details = {
        "name": result["name"],
        "formatted_address": result["formatted_address"],
        "location": result["geometry"]["location"],
        "formatted_phone_number": result.get("formatted_phone_number"),  # Use .get()
        "website": result.get("website"),  # Use .get()
        "rating": result.get("rating"),  # Use .get()
        "reviews": result.get("reviews"),  # Use .get()
        "opening_hours": result.get("opening_hours")  # Use .get()
    }
 
    place_details_result = f"""
        place_detail : {place_details_result}
    """

    return place_details_result.strip()

@mcp.tool()
async def nearbysearch(location: str, types=None, radius=None ) -> str:
    """The Nearby Search Api provides nearby places of a particular category/type as requested in input based on the given input location.

    Args:
        location: The latitude longitude in string format around which to retrieve nearby places information. Example : 12.931544865377818,77.61638622280486
        types: Restricts the results to places matching the specified category.Multiple values can be provided separated by a comma.
        radius: The distance (in meters) within which to return place results.
    """
    url = f"{MAPS_BASE_API}/places/v1/nearbysearch/advanced"
    params = {
        "location": location,
        "api_key": API_KEY,
    }

    if types :
        params["types"] = str(types)
    else:
        params["types"] = "restaurant"

    if radius:
        params["radius"] = int(radius)
    else : 
        params["radius"] = 5000
    
    data = await make_get_request(url, params=params)

    if data is None or data.get("status", "").lower() != "ok":
        return f"NearBySearch failed: {data.get('reason') if data else 'No response from API'}"
           
    results = data["predictions"]
    final_result = []
    for result in results:
        info = {
            "name" : result["description"],
            "place_id": result["place_id"],
            "types" : result["types"],
            "distance_meters": result["distance_meters"],
            "website": result["url"],
            "phone": result["formatted_phone_number"],
            "rating": result["rating"],
            "opening_hours": result["opening_hours"]
        }
        final_result.append(info)
 
    nearbysearch_result = f"""
        nearbysearch_detail : {final_result}
    """

    return nearbysearch_result.strip()

@mcp.tool()
async def textsearch(query: str, location=None, radius=None) -> str:
    """Provides a list of places based on textual queries without need of actual location coordinates. For eg: "Cafes in Koramangala" or "Restaurant near Bangalore".

    Args:
        query (str): The search query.
        location: Optionally, you can specify a location to search around that particular location. The location must be a string in the format of 'latitude,longitude'.
        radius: Radius to restrict the search results to a certain distance around the location.
    """
    url = f"{MAPS_BASE_API}/places/v1/textsearch"
    params = {
        "input": query,
        "api_key": API_KEY,
    }

    if location:
        params["location"] = f"{location}"
        if radius:
            params["radius"] = int(radius)
    
    data = await make_get_request(url, params=params)

    if data is None or data.get("status", "").lower() != "ok":
        return f"text search failed: {data.get('error_message') if data else 'No response from API'}"
           
    results = data["predictions"]
    final_result = []
    for result in results:
        info = {
            "name" : result["name"],
            "formatted_address": result["formatted_address"],
            "place_id": result["place_id"],
            "co-ordinates": result["geometry"]["location"],
            "types": result["types"]
        }
        final_result.append(info)
 
    textsearch_result = f"""
        querysearch_detail : {final_result}
    """

    return textsearch_result.strip()

@mcp.tool()
async def get_directions(origin: str, destination: str) -> str:
    """Provides routable path between two or more points. Accepts coordinates in lat,long format.

    Args:
        origin: Origin coordinates in the format lat,lng e.g: 12.993103152916301,77.54332622119354
        destination: Destination coordinates in the format lat,lng e.g:     
    """
    url = f"{MAPS_BASE_API}/routing/v1/directions"
    params = {
        "origin": origin,
        "destination": destination,
        "mode": "driving",
        "alternatives": "true",
        "api_key": API_KEY,
    }

    data = await make_post_request(url, params=params)

    # if data is None or data.get("status", "").lower() != "ok" or data.get("status", "").lower() != "success":
    #     return f"Directions failed: {data.get('error_message') if data else 'No response from API'}"
           

    routes = []
    for route in data["routes"]:
        route_data = {
            "summary": route["summary"],
            "legs": [],
            "overview_polyline": route["overview_polyline"]
        }
        for leg in route["legs"]:
            leg_data = {
                "distance": leg["distance"],
                "duration": leg["duration"],
                "steps": []
            }
            for step in leg["steps"]:
                step_data = {
                    "distance": step["distance"],
                    "duration": step["duration"],
                }
                leg_data["steps"].append(step_data)
            route_data["legs"].append(leg_data)
        routes.append(route_data)
 
    directions_result = f"""
        routes_information : {routes}
    """

    return directions_result.strip()

@mcp.tool()
async def distanceMatrix(origins: str, destinations: str) -> str:
    """
    Calculates travel distance and time for multiple origins and destinations.

    Args:
        origins: Pipe separated origin coordinates in the format lat1,lng1|lat2,lng2 e.g: 28.71866756826579,77.03699668376802|28.638555357785652,76.96550156007675
        destinations: Pipe separated destination coordinates in the format lat1,lng1|lat2,lng2 e.g: 28.638555357785652,76.96550156007675|28.53966907108812,77.05190669909288
    """
    url = f"{MAPS_BASE_API}/routing/v1/distanceMatrix"
    params = {
        "origins": origins,
        "destinations": destinations,
        "mode": "driving",
        "api_key": API_KEY,
    }

    data = await make_get_request(url, params=params)

    if data is None or data.get("status", "").lower() != "ok" or data.get("status", "").lower() != "success":
        return f"Distance Matrix failed: {data.get('reason') if data else 'No response from API'}"
           
    results = []

    for row in data["rows"]:
        row_results = []
        for element in row["elements"]:
            element_data = {
                "status": element["status"],
                "duration": element.get("duration"),  # Use .get()
                "distance": element.get("distance")  # Use .get()
                # "polyline": element["polyline"]
            }
            row_results.append(element_data)
        results.append({"elements": row_results})

    distanceMatrix_results= f"""
        "result": {results}
    """

    return distanceMatrix_results.strip()