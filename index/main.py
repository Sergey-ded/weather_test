from main_utils import *
from var import *
from utils import BOT_TOKEN, CHAT_ID


# data = get_forcast_yandex(WEATHER_ACCESS_KEY, WEATHER_QUERY)

data = read_from_json()

write_to_db_src(data)

send_telegram_notification(notif_message, BOT_TOKEN, CHAT_ID)
