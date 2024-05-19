import requests
from config import Config

def get_current_rate():
    url = f'https://openexchangerates.org/api/latest.json?app_id={Config.OPENEXCHANGERATES_API_KEY}&symbols=UAH'
    response = requests.get(url)
    data = response.json()
    return data['rates']['UAH']
