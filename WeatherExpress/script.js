function getWeather() {
  var city = document.getElementById("cityInput").value;
  var unit = document.getElementById("unitSelect").value;
  var url = "/get_weather?city=" + city + "&unit=" + unit;

  fetch(url)
    .then(response => response.json())
    .then(data => {
      // Access weather data from the response
      var weatherSummary = data.weather_summary;
      var weatherDescription = data.weather_description;
      var highTempPm = data.high_temp_pm;
      var highTempAm = data.high_temp_am;
      var highTempNight = data.high_temp_night;
      var lowTempPm = data.low_temp_pm;
      var lowTempAm = data.low_temp_am;
      var lowTempNight = data.low_temp_night;

      // Update DOM with weather data
      document.getElementById("weatherSummary").innerText = weatherSummary;
      document.getElementById("weatherDescription").innerText = weatherDescription;
      document.getElementById("highTempPm").innerText = "High Temp PM: " + highTempPm;
      document.getElementById("highTempAm").innerText = "High Temp AM: " + highTempAm;
      document.getElementById("highTempNight").innerText = "High Temp At Night: " + highTempNight;
      document.getElementById("lowTempPm").innerText = "Low Temp PM: " + lowTempPm;
      document.getElementById("lowTempAm").innerText = "Low Temp AM: " + lowTempAm;
      document.getElementById("lowTempNight").innerText = "Low Temp At Night: " + lowTempNight;
    })
    .catch(error => console.error(error));
}