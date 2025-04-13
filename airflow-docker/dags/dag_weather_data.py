from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from index.main_utils import get_forcast_yandex, run_dbt, send_telegram_notification, initial_db
from index.utils import *
from index.query_storage import WEATHER_QUERY
from index.var import notif_message


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

initial_task = PythonOperator(
    task_id='initial_db',
    python_callable=initial_db,
    dag=dag,
)

fetch_data_task = PythonOperator(
    task_id='fetch_weather_data',
    python_callable=get_forcast_yandex,
    op_args=[WEATHER_ACCESS_KEY, WEATHER_QUERY],
    dag=dag,
)

transfer_to_ods_task = PythonOperator(
    task_id='transfer_to_ods',
    python_callable=run_dbt,
    dag=dag,
)

notify_task = PythonOperator(
    task_id='send_notification',
    python_callable=send_telegram_notification,
    op_args=[notif_message, BOT_TOKEN, CHAT_ID],
    dag=dag,
)

initial_task >> fetch_data_task >> transfer_to_ods_task >> notify_task