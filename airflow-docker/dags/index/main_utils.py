import requests
import json
import psycopg
from index.utils import *
from index.query_storage import *
import subprocess
import os

def initial_db():
    with psycopg.connect(
            dbname=f"{DB_NAME}", user=f"{USERNAME}", password=f"{PSWD}", host=f"{HOST}"
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(initial_query)
            conn.commit()

def get_forcast_yandex(key, query):
    headers = {
        'X-Yandex-Weather-Key': key
    }

    response = requests.post('https://api.weather.yandex.ru/graphql/query', headers=headers,
                             json={'query': query})
    write_to_db_src(response.json())

def write_to_db_src(data):
    with psycopg.connect(
            dbname=f"{DB_NAME}", user=f"{USERNAME}", password=f"{PSWD}", host=f"{HOST}"
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(clear_src)
            for city, city_data in data['data'].items():
                for forecast in city_data["forecast"]["days"]:
                    forecast_for = forecast["time"]
                    temperature = forecast["summary"]["day"]["avgTemperature"]
                    prec_type = forecast["summary"]["day"]["precType"]
                    prec = forecast["summary"]["day"]["prec"]
                    humidity = forecast["summary"]["day"]["humidity"]
                    pressure = forecast["summary"]["day"]["pressure"]

                    cur.execute(insert_in_src, (city, forecast_for, temperature, prec_type, prec, humidity, pressure))
            conn.commit()


def send_telegram_notification(message, bot_token, chat_id):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
    }
    requests.post(url, data=payload)

def run_dbt():
    dbt_project_path = "/opt/airflow/dags/weather_forcast/models/transform_model"
    subprocess.run(
        ["dbt", "run", "--models", "transform"],
        cwd=dbt_project_path,
        env={
            **os.environ,
            "DBT_PROFILES_DIR": "/home/airflow/.dbt"
        },
    )

def write_to_json(data):
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def read_from_json():
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    return data
