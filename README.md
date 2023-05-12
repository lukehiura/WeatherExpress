# Weather Blog App

![Weather Blog App Banner](https://example.com/banner-image.png)

Welcome to the Weather Blog App! This web application allows users to access weather information, create and manage weather-related blog posts, and interact with various APIs and services. The app is designed to provide an intuitive and engaging user experience while leveraging technologies like Flask, MongoDB, AWS S3, Google Maps API, Docker, and Jenkins for seamless development, deployment, and testing processes.

## Features

### Weather Information

Users can retrieve current weather information by entering a location (city, state, country) in the app's user interface. Unlike traditional weather APIs, this app utilizes web scraping techniques to fetch data from weather websites, ensuring up-to-date and accurate information. The scraped data is then processed and displayed in a user-friendly format, providing users with comprehensive weather details for the desired location.

### Blogging Functionality

The Weather Blog App offers a powerful blogging platform where users can create, read, update, and delete blog posts related to weather. Each blog post can have a title, content, and optionally, an image. Users can view all blog posts, as well as filter and sort them by various criteria, such as date, author, or weather topic. The blog posts and associated data are stored in a MongoDB database, and images are stored in a cloud-based storage service using AWS S3.

### User Authentication

User authentication is implemented to ensure secure access to the app's features. Users can sign up with a valid email and password, log in securely, and log out when needed. Authenticated users can create, edit, and delete their own blog posts, while unauthorized users can only view blog posts.

### Google Maps API Integration

The app integrates with the [Google Maps API](https://developers.google.com/maps) to provide an interactive map that displays the location of weather information and blog posts. Users can visually explore weather information and blog posts on the map, enhancing their overall experience.

### Containerization with Docker

The Weather Blog App is containerized using [Docker](https://www.docker.com), which simplifies the deployment process and ensures consistent execution across different environments. Docker allows for the secure loading of environment variables, such as API keys and secrets, into the container for enhanced security.

### Deployment with AWS Beanstalk

The app is deployed to [AWS Beanstalk](https://aws.amazon.com/elasticbeanstalk), a scalable and managed platform for hosting web applications. Beanstalk simplifies deployment, scaling, and management, including automatic scaling based on traffic, monitoring, and logging.

### Domain Name with Route 53

The app utilizes [Amazon Route 53](https://aws.amazon.com/route53) to assign a custom domain name, providing users with a user-friendly URL for accessing the app. Route 53 simplifies domain management, DNS settings, and SSL certificate integration for enhanced security.

### Jinja2 Templating Engine

The app utilizes the [Jinja2](https://jinja.palletsprojects.com) templating engine in Flask to incorporate dynamic content into the user interface. Jinja2 allows for the easy separation of HTML and Python code, enabling dynamic rendering of content based on user inputs and application logic.

### Image Storage with AWS S3

The Weather Blog App utilizes [AWS S3](https://aws.amazon.com/s3) (Simple Storage Service) to store images uploaded by users for their blog posts.

## Usage

To run the Weather Blog App locally, follow these steps:

1. Clone the repository: `git clone https://github.com/your-username/WeatherBlogApp.git`
2. Install the required dependencies: 
  - `cd WeatherBlogApp` 
  - `pip install -r requirements.txt`



Set up the necessary configuration:

- Configure the MongoDB connection in `config.py`.
- Set up your AWS S3 credentials in `config.py` for image storage.
- Add your Google Maps API key in the appropriate location in the code.

Run the application using the provided code snippet:

```python
from WeatherExpress import application
if __name__ == '__main__':
    application.run(debug=True, port=8081)
```
    



## REST API and gRPC Server

The Weather Blog App utilizes a REST API and gRPC server for data retrieval. The server code provides the necessary data endpoints for the Weather Blog App to retrieve weather information and other related data.

# WeatherExpress

WeatherExpress is a microservice application that provides weather data for different cities around the world. This README outlines the communication contract for the Weather microservice, which allows developers to retrieve weather data programmatically.

# Using the Weather Microservice with gRPC

To use the Weather microservice in your client code, you will need to download the protobuf files provided in the serverclient zip folder and add them to your project directory. These files define the data structures and RPC methods used by the Weather service and are required to generate client and server code in the programming language of your choice.

## What is gRPC?

gRPC is a modern, high-performance framework that enables efficient communication between distributed systems. It uses Protocol Buffers, a language-agnostic binary serialization format, to define the structure of the data being exchanged and generates client and server code in multiple programming languages. The resulting code is type-safe, easy to use, and highly performant, making it ideal for building microservices and other distributed systems.

## How gRPC Works

To use gRPC in your project, you first define the data structures and RPC methods using Protocol Buffers, and then use the gRPC toolchain to generate client and server code in your chosen programming language. You can then use this generated code to communicate with your gRPC server and exchange data.

The gRPC framework handles many of the low-level details of network communication, such as establishing connections, sending data, and handling errors. It also provides built-in support for advanced features like authentication, load balancing, and distributed tracing, making it a powerful tool for building complex distributed systems.

## Using gRPC with the Weather Microservice

In the case of the Weather microservice, the protobuf files define the WeatherRequest and WeatherResponse message types, as well as the GetWeather RPC method that allows clients to request weather data for a specific city. By importing these files into your client code and using the generated gRPC client code, you can easily request weather data from the Weather microservice and use it in your application.

Using gRPC to communicate with the Weather microservice offers several advantages over other communication methods, such as REST or SOAP. For example, gRPC is more efficient than REST because it uses binary serialization rather than text-based formats like JSON or XML. This makes it faster and more compact, resulting in lower network usage and higher performance. Additionally, gRPC's built-in support for streaming allows you to easily receive continuous updates from the Weather service, making it ideal for real-time applications.

## Communication Contract

The Weather microservice uses gRPC as its main communication pipeline. To request weather data from the microservice, follow these instructions:

### Requesting Data



1. Create a gRPC channel to connect to the Weather microservice.

    ```python
    channel = grpc.insecure_channel('localhost:50051')
    ```

2. Create a stub object for the Weather service.

    ```python
    stub = weather_pb2_grpc.WeatherServiceStub(channel)
    ```

3. Create a request object with the city name and unit.

    ```python
    request = weather_pb2.WeatherRequest(city=city, unit=unit)
    ```

4. Call the `GetWeather` method on the Weather service stub, passing in the request object.

    ```python
    response = stub.GetWeather(request)
    ```

5. Convert the response to a JSON object.

    ```python
    json_response = {
        'weather_summary': response.weather_summary,
        'weather_description':response.weather_description, 
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
    ```

6. Return the JSON response.

    ```python
    return json.dumps(json_response)
    ```

Here's an example call to retrieve the weather data for New York City in Celsius:

```python
import grpc
import weather_pb2
import weather_pb2_grpc
import json

channel = grpc.insecure_channel('localhost:50051')
stub = weather_pb2_grpc.WeatherServiceStub(channel)

request = weather_pb2.WeatherRequest(city='New York', unit='c')
response = stub.GetWeather(request)

json_response = {
    'weather_summary': response.weather_summary,
    'weather_description':response.weather_description, 
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

print(json_response)
```

Receiving Data from the Weather Microservice

The Weather microservice can also send data to clients using gRPC's streaming capabilities. To receive data from the microservice in real-time, you can use the server-side streaming feature to stream weather updates to your client. Here are the steps:

1. Define a streaming RPC method in the Weather service that sends weather updates to clients.
2. Implement the streaming method on the server side to send weather updates at regular intervals.
3. Use the gRPC client code to call the streaming method on the server and receive the weather updates.

Here's an example of how to receive weather updates in Python:

```python
import grpc
import weather_pb2
import weather_pb2_grpc

def weather_updates(stub):
    """
    A generator function that receives weather updates from the server.
    """
    request = weather_pb2.WeatherRequest(city='San Francisco')
    for response in stub.StreamWeather(request):
        yield response.temperature

# create a gRPC channel and stub
channel = grpc.insecure_channel('localhost:50051')
stub = weather_pb2_grpc.WeatherStub(channel)

# call the weather_updates generator function to receive weather updates
for temperature in weather_updates(stub):
    print('Current temperature in San Francisco: ', temperature)
    
   ```
   
# UML Sequence Diagram

![alt text](uml.png)

1. The client sends a request for weather data to the WeatherService.
2. The WeatherService receives the request and retrieves the relevant weather data.
3. The WeatherService creates a WeatherResponse message containing the weather data.
4. The WeatherService sends the WeatherResponse message to the client.
5. The client receives the WeatherResponse message containing the weather data.






