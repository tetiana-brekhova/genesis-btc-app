import requests
from config import Config


def get_current_rate():
    url = f'https://v6.exchangerate-api.com/v6/dacee103637befefa0104478/latest/USD'

    response = requests.get(url)
    data = response.json()
    result = data["conversion_rates"]['UAH']
    return result
