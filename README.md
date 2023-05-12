# Weather Blog App

Welcome to the Weather Blog App! This is a web application that allows users to get weather information for a given location, create and manage blog posts related to weather, and interact with various APIs and services for authentication, image storage, and deployment.

## Features

- Weather Information: Users can enter a location (city, state, country) and retrieve current weather information by scraping data from a weather website instead of using a weather API. The scraped data is processed and displayed in a user-friendly format in the app's UI.

- Blogging Functionality: Users can create, read, update, and delete blog posts related to weather. Each blog post can have a title, content, and optionally, an image. Users can view all blog posts, as well as filter and sort them by various criteria, such as date, author, or weather topic. The blog posts and associated data are stored in a MongoDB database, and images are stored in a cloud-based storage service using AWS S3.

- User Authentication: The app supports user authentication using Flask-Bcrypt, a secure password hashing library for Flask applications. Users can sign up with a valid email and password, log in securely, and log out when needed. Authenticated users can create, edit, and delete their own blog posts, while unauthorized users can only view blog posts.

- Google Maps API Integration: The app uses the Google Maps API to load maps and display the location of the weather information and blog posts on an interactive map in the app's UI. Users can view weather information and blog posts visually on the map, enhancing their overall experience.

- Containerization with Docker: The app is containerized using Docker, allowing for easy deployment and management of the application's dependencies, including MongoDB, Flask, Flask-Bcrypt, and other libraries. Docker also allows for the secure loading of environment variables, such as API keys and secrets, into the Docker container for enhanced security.

- Deployment with AWS Beanstalk: The app is deployed to the AWS Beanstalk service, which provides a simple and scalable platform for hosting web applications. Beanstalk allows for easy deployment, scaling, and management of the app, including automatic scaling based on traffic, monitoring, and logging.

- Domain Name with Route 53: The app uses the Amazon Route 53 service to designate a custom domain name for the application, providing a user-friendly URL for accessing the app. Route 53 allows for easy management of domain names, DNS settings, and SSL certificates for enhanced security.

- Jinja2 Templating Engine: The app uses the Jinja2 templating engine in Flask to incorporate dynamic content, such as forms, pagination, and other elements of web design, into the app's UI. Jinja2 allows for easy separation of HTML and Python code, enabling dynamic rendering of content based on user inputs and application logic.

- Image Storage with AWS S3: The app uses the AWS S3 (Simple Storage Service) to store images uploaded by users for their blog posts. Images are securely uploaded to S3 and stored in a designated bucket, and the image URLs are stored in the MongoDB database for later retrieval and display in the app's UI.

## How It Works

1. Weather Information: Users can enter a location in the app's UI, and the app scrapes weather data from a weather website using web scraping techniques. The scraped data is processed and displayed in the app's UI, providing the user with up-to-date weather information.

2. Blogging Functionality: Users can create, read, update, and delete blog posts in the app's UI. Blog posts, along with their associated data, such as author, date, and image URL, which are stored in a MongoDB database.


3. New changes
