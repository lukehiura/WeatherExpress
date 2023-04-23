# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the app runs on
EXPOSE 5000

# Set the environment variables
ENV GOOGLE_API_KEY="AIzaSyAaccF2c64kfnoJFy8G4RmhYGI7ohOKrE4"
ENV SECRET_KEY='5791628bb0b13ce0c676dfde280ba245'
ENV SQLALCHEMY_DATABASE_URI=sqlite:///site.db
ENV MONGO_URI='mongodb+srv://lhiur001:0pemDaAuQTiqvR9L@profiles-db.jovxyhy.mongodb.net/profiles-db?retryWrites=true&w=majority'

# Start the app
CMD ["python", "app.py"]