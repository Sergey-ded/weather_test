from utils import *
from var import *
import requests

headers = {
    'X-Yandex-Weather-Key': WEATHER_ACCESS_KEY
}

response = requests.post('https://api.weather.yandex.ru/graphql/query', headers=headers, json={'query': WEATHER_QUERY})

print(response.json())