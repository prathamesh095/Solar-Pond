import requests
from flask import Flask, render_template, request

app = Flask(__name__)

def get_weather_info(city):
    api_key = "7ad972ec5eae50b49e2580e0dc9b08ae"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

    try:
        response = requests.get(url)
        data = response.json()
        temperature_kelvin = data["main"]["temp"]
        temperature_celsius = temperature_kelvin - 273.15
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        return round(temperature_celsius, 2), humidity, wind_speed
    except Exception as e:
        print("Error fetching weather information:", e)
        return None, None, None

def calculate_pond_dimensions(temperature):
    # Example calculation for dimensions (you can adjust these according to your requirements)
    # This is just a placeholder
    length = temperature * 2
    width = temperature * 1.5
    depth = temperature / 2
    
    return length, width, depth

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
        temperature, humidity, wind_speed = get_weather_info(city)
        if temperature:
            length, width, depth = calculate_pond_dimensions(temperature)
            return render_template('index.html', temperature=temperature, humidity=humidity, wind_speed=wind_speed, length=length, width=width, depth=depth, city=city)
        else:
            return render_template('index.html', error="Failed to fetch weather information for the city.")
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
