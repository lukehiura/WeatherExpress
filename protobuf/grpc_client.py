from flask import Flask, request, jsonify
from protobuf import weather_pb2
from protobuf import weather_pb2_grpc
import grpc
import json

app = Flask(__name__)

@app.route('/weather', methods=['POST'])
def get_weather():
    data = request.get_json()
    city = data.get('city')
    unit = data.get('unit', 'C')

    # Create a gRPC channel to connect to the weather microservice
    channel = grpc.insecure_channel('localhost:50051')

    # Create a stub object for the weather service
    stub = weather_pb2_grpc.WeatherServiceStub(channel)

    # Create a request object with the cityname and unit
    request = weather_pb2.WeatherRequest(city=city, unit=unit)

    if request is None:
        return jsonify({'error': 'Bad Request'})

    # Call the getWeather method on the weather service stub, passing in the request object
    response = stub.GetWeather(request)

    # Convert the response to a JSON object
    json_response = {
        'weather_summary': response.weather_summary,
        'weather_description': response.weather_description,
        'high_temp_pm': response.high_temp_pm,
        'high_temp_am': response.high_temp_am,
        'high_temp_night': response.high_temp_night,
        'low_temp_pm': response.low_temp_pm,
        'low_temp_am': response.low_temp_am,
        'low_temp_night': response.low_temp_night,
        'humidity_pm': response.humidity_pm,
        'humidity_am': response.humidity_am,
        'humidity_night': response.humidity_night
    }
    return jsonify(json_response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
