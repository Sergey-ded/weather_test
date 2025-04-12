from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from main_utils import get_forcast_yandex, run_dbt, send_telegram_notification
from utils import *
from query_storage import WEATHER_QUERY
from var import notif_message


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 4, 12),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'weather_data_ingestion',
    default_args=default_args,
    description='DAG для загрузки данных погоды',
    schedule_interval=timedelta(days=1),
)

fetch_data_task = PythonOperator(
    task_id='fetch_weather_data',
    python_callable=get_forcast_yandex(WEATHER_ACCESS_KEY, WEATHER_QUERY),
    dag=dag,
)

transfer_to_ods_task = PythonOperator(
    task_id='load_data_to_src',
    python_callable=run_dbt(),
    dag=dag,
)

notify_task = PythonOperator(
    task_id='send_notification',
    python_callable=send_telegram_notification(notif_message, BOT_TOKEN, CHAT_ID),
    dag=dag,
)

fetch_data_task >> transfer_to_ods_task >> notify_task