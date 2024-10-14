import requests
from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)

class City:
    def __init__(self, name, lat, lon, units="metric"):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.units = units
        self.current_time = self.get_current_time()
        self.get_data()

    def get_current_time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_data(self):
        try:
            response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?units={self.units}&lat={self.lat}&lon={self.lon}&appid=79007029562c2ab46617d801d8018750")
            response.raise_for_status()  # Raise an error for bad responses
            self.response_json = response.json()

            if "main" in self.response_json and "weather" in self.response_json:
                self.temp = self.response_json["main"].get("temp", "N/A")
                self.temp_min = self.response_json["main"].get("temp_min", "N/A")
                self.temp_max = self.response_json["main"].get("temp_max", "N/A")
                self.weather_description = self.response_json["weather"][0].get("description", "N/A")
            else:
                raise ValueError("Invalid response structure")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            self.temp = self.temp_min = self.temp_max = self.weather_description = "N/A"
        except ValueError as e:
            print(f"Data error: {e}")
            self.temp = self.temp_min = self.temp_max = self.weather_description = "N/A"

    def data_print(self):
        return {
            "name": self.name,
            "temp": self.temp,
            "temp_min": self.temp_min,
            "temp_max": self.temp_max,
            "weather_description": self.weather_description,
            "current_time": self.current_time
        }

@app.route('/')
def index():
    cities = [
        City("Zürich", 47.36667, 8.55),
        City("Madrid", 40.416775, -3.703790),
        City("Cali", 3.450541, -76.534630)
    ]

    city_weather = [city.data_print() for city in cities]
    return render_template('index.html', city_weather=city_weather)

if __name__ == "__main__":
    app.run(debug=True)