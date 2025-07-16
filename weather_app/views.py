# weather_app/views.py

from django.shortcuts import render
from .forms import WeatherForm
import requests
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime

def index(request):
    form = WeatherForm()
    chart = None
    forecast_data = None

    if request.method == 'POST':
        form = WeatherForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            unit = form.cleaned_data['unit']
            graph = form.cleaned_data['graph']
            API_KEY = 'be62a54fcc5522bd4cc0a255a4d5dd29'  # 🔁 Replace with your OpenWeatherMap API key

            forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units={unit}&appid={API_KEY}"
            current_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units={unit}&appid={API_KEY}"

            forecast_res = requests.get(forecast_url)
            current_res = requests.get(current_url)

            if forecast_res.status_code == 200 and current_res.status_code == 200:
                data = forecast_res.json()
                current = current_res.json()

                min_temps = [entry['main']['temp_min'] for entry in data['list'][:6]]
                max_temps = [entry['main']['temp_max'] for entry in data['list'][:6]]
                times = [entry['dt_txt'] for entry in data['list'][:6]]

                # Plot chart
                plt.figure(figsize=(10, 4))
                if graph == 'line':
                    plt.plot(times, min_temps, marker='o', label='Min Temp')
                    plt.plot(times, max_temps, marker='o', label='Max Temp')
                else:
                    plt.bar(times, min_temps, label='Min Temp')
                    plt.bar(times, max_temps, label='Max Temp', alpha=0.5)

                plt.xticks(rotation=45)
                plt.xlabel("Time")
                plt.ylabel("Temperature")
                plt.title(f"{city} - Forecasted Min/Max Temperatures")
                plt.legend()
                plt.tight_layout()

                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                chart = base64.b64encode(buf.read()).decode('utf-8')
                buf.close()
                plt.close()

                # Weather condition alert
                condition = data['list'][0]['weather'][0]['main']
                if condition.lower() == 'snow':
                    alert = "⚠️ Snow Alert: Stay Warm!"
                elif condition.lower() == 'clouds':
                    alert = "☁️ Cloudy Skies Ahead."
                else:
                    alert = f"✅ Weather looks {condition.lower()} and clear."

                # Sunrise/sunset
                sunrise = datetime.fromtimestamp(current['sys']['sunrise']).strftime('%I:%M %p')
                sunset = datetime.fromtimestamp(current['sys']['sunset']).strftime('%I:%M %p')

                forecast_data = {
                    'temp_pairs': list(zip(min_temps, max_temps)),
                    'alert': alert,
                    'cloud_coverage': current['clouds']['all'],
                    'wind_speed': current['wind']['speed'],
                    'sunrise': sunrise,
                    'sunset': sunset,
                    'city': city
                }

    return render(request, 'weather_app/index.html', {
        'form': form,
        'chart': chart,
        'forecast_data': forecast_data
    })
