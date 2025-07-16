# weather_app/forms.py

from django import forms

class WeatherForm(forms.Form):
    city = forms.CharField(label='City Name', max_length=100)
    unit = forms.ChoiceField(label='Temperature Unit', choices=[('metric', 'Celsius'), ('imperial', 'Fahrenheit')])
    graph = forms.ChoiceField(label='Graph Type', choices=[('line', 'Line Graph'), ('bar', 'Bar Graph')])
