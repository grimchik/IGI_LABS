import requests

def get_weather(city):
    api_key = 'fe68c44f89aa2613e18c115c46431c82'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        return None
