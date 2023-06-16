import requests
import re
from flask import Flask, request

BASE_URL = 'https://www.weather-forecast.com/locations/'
def get_weather_summary(response, units="C"):
    if response.status_code == 200:
        txt = response.text
        pattern = r'<p class="location-summary__text"><span class="phrase">(.*?)</span></p>'
        summary = re.findall(pattern, txt)
        summary = summary[0].replace("&deg;C", '\N{DEGREE SIGN}' + units)

        if units == "F":
            numbers = re.findall(r'\d+', summary)
            new_nums = []
            for i in numbers:
                new_nums.append(celsius_to_fahrenheit(i))
            for old, new in zip(numbers, new_nums):
                summary = summary.replace(old, str(new))

        elif units == "K":
            numbers = re.findall(r'\d+', summary)
            new_nums = []
            for i in numbers:
                new_nums.append(celsius_to_kelvin(i))
            for old, new in zip(numbers, new_nums):
                summary = summary.replace(old, str(new))

        pattern = r'<span class="show-for-medium-up">(.*?)</span>'
        title = re.findall(pattern, txt)
        title = title[0]
        return [summary, title]
    else:
        print("Error: Invalid city name")
        return None

def get_temperatures(response, UnitofTemp="C"):

    if response.status_code == 200:
        txt = response.text
        patternMax = r'<tr class="b-forecast__table-max-temperature js-temp">(.*?)</tr>'
        maxliststr = re.findall(patternMax, txt)[0]
        patternMax2 = r'<td class=\"b-forecast__table-cell-max temp-color.*?>(.*?)</td>'
        maxlist = re.findall(patternMax2, maxliststr)[0:3]
        HighTempAM = re.findall(r'\d+', maxlist[0])[0]
        HighTempPM = re.findall(r'\d+', maxlist[1])[0]
        HighTempNight = re.findall(r'\d+', maxlist[2])[0]

        patternMin = r'<tr class="b-forecast__table-min-temperature js-min-temp">(.*?)</tr>'
        MinListStr = re.findall(patternMin, txt)[0]
        patternMin2 = r'<td class=\"b-forecast__table-cell-min temp-color.*?>(.*?)</td>'
        minlist = re.findall(patternMin2, MinListStr)[0:3]
        MinTempAM = re.findall(r'\d+', minlist[0])[0]
        MinTempPM = re.findall(r'\d+', minlist[1])[0]
        MinTempNight = re.findall(r'\d+', minlist[2])[0]

        if UnitofTemp == "K":
            HighTempPM = celsius_to_kelvin(HighTempPM)
            HighTempAM = celsius_to_kelvin(HighTempAM)
            HighTempNight = celsius_to_kelvin(HighTempNight)
            MinTempPM = celsius_to_kelvin(MinTempPM)
            MinTempAM = celsius_to_kelvin(MinTempAM)
            MinTempNight = celsius_to_kelvin(MinTempNight)

        elif UnitofTemp == "F":
            HighTempPM = celsius_to_fahrenheit(HighTempPM)
            HighTempAM = celsius_to_fahrenheit(HighTempAM)
            HighTempNight = celsius_to_fahrenheit(HighTempNight)
            MinTempPM = celsius_to_fahrenheit(MinTempPM)
            MinTempAM = celsius_to_fahrenheit(MinTempAM)
            MinTempNight = celsius_to_fahrenheit(MinTempNight)

        oldresult = [HighTempPM, HighTempAM, HighTempNight, MinTempPM, MinTempAM, MinTempNight]
        result = []
        for eachresult in oldresult:
            result.append(str(eachresult) + '\N{DEGREE SIGN}' + UnitofTemp)
        return result
    else:
        print("Error: Invalid city name")
        return None


def get_humidity(response):
    if response.status_code == 200:
        txt = response.text
        patternMax = r'<tr class="b-forecast__table-humidity js-humidity">(.*?)</tr>'
        maxliststr = re.findall(patternMax, txt)[0]
        patternMax2 = r'<td class=\"b-forecast__table-cell-humidity.*?>(.*?)</td>'
        maxlist = re.findall(patternMax2, maxliststr)[0:3]
        HighHumidAM = re.findall(r'\d+', maxlist[0])[0]
        HighHumidPM = re.findall(r'\d+', maxlist[1])[0]
        HighHumidNight = re.findall(r'\d+', maxlist[2])[0]

        oldresult = [HighHumidPM, HighHumidAM, HighHumidNight]
        print(oldresult)
        result = []
        for eachresult in oldresult:
            result.append(str(eachresult) + ' %')
        return result
    else:
        print("Error: Invalid city name")
        return None


def get_wind_speed(response):

    if response.status_code == 200:
        txt = response.text
        pattern = r'<p class="location-summary__text"><span class="phrase">(.*?)</span></p>'
        summary = re.findall(pattern, txt)
        summary = summary[0].replace("&deg;C", " C degrees")
        return summary
    else:
        print("Error: Invalid city name")
        return None

def get_response(rawLocation):
    if rawLocation is None:
        raise ValueError("Invalid location: Location is not provided.")

    location = rawLocation.strip().replace(" ", "-")
    if not location:
        raise ValueError("Invalid location: Location is empty.")

    SCRAPE_URL = BASE_URL + location + "/forecasts/latest"
    try:
        response = requests.get(SCRAPE_URL)
        response.raise_for_status()  # Check for HTTP errors
    except requests.RequestException as e:
        raise RuntimeError(f"Error retrieving weather data: {e}")

    return response


def average(numbers):
    """
    Function to calculate the average of a list of numbers.
    """
    if not numbers:
        raise ValueError("Input list is empty")
    numbers = list(map(float, numbers))
    total = sum(numbers)
    average = total / len(numbers)
    return average

def celsius_to_fahrenheit(celsius):
    """Converts temperature from Celsius to Fahrenheit."""
    celsius = int(celsius)
    fahrenheit = (celsius * 9/5) + 32
    return fahrenheit

def celsius_to_kelvin(celsius):
    """Converts temperature from Celsius to Kelvin."""
    celsius = float(celsius)
    kelvin = celsius + 273.15
    return kelvin




if __name__ == '__main__':
    cityname = input('Enter city name: ')
    unit = 'C'
    user_unit = input('Enter the units (Options - C/F/K | Default - C): ')
    if user_unit:
        unit = user_unit
    response = get_response(cityname)
    print(get_weather_summary(response, unit)[1], '\n')
    print(get_weather_summary(response, unit)[0], '\n')

    print("High Temp PM: ", get_temperatures(response, unit)[0])
    print("High Temp AM: ", get_temperatures(response, unit)[1])
    print("High Temp At Night: ", get_temperatures(response, unit)[2])

    print("Low Temp PM: ", get_temperatures(response, unit)[3])
    print("Low Temp AM: ", get_temperatures(response, unit)[4])
    print("Low Temp At Night: ", get_temperatures(response, unit)[5])

    print("Humid PM: ", get_humidity(response)[0])
    print("Humid AM: ", get_humidity(response)[1])
    print("Humid At Night: ", get_humidity(response)[2])



