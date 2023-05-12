import requests
from flask import jsonify

def get_weather(city, unit):
    # Prepare the URL for the REST API endpoint
    url = f"http://ec2-35-161-97-196.us-west-2.compute.amazonaws.com:8080/weather?city={city}&unit={unit}"

    # Send an HTTP GET request to the server
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        json_response = response.json()
        return (response.text, response.status_code, response.headers.items())
    else:
    # Return an error response
        error_response = {'error': 'Bad Request'}
        return (jsonify(error_response), 400, {'Content-Type': 'application/json'})

