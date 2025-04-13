with raw_weather as (
    select
        city,
        forecast_for AT TIME ZONE 'Europe/Moscow' as forecast_for_moscow,
        case
            when temperature = 0 then null
            else temperature
        end as temperature,
        case
            when prec = 0 then null
            else prec
        end as prec,
        case
            when prec_type IN ('SLEET', 'RAIN') then 'RAIN'
            when prec_type = 'NO_TYPE' then 'NONE'
            else prec_type
        end as precip_category,
        humidity,
        pressure
    from src.weather_src
)

select
    city,
    forecast_for_moscow,
    temperature,
    precip_category,
    prec,
    humidity,
    pressure
from raw_weather