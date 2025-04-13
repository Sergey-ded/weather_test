WEATHER_QUERY = """
{
  Moscow: weatherByPoint(request: { lat: 55.755864, lon: 37.617698 }) {
    ...WeatherData
  }
  Belgorod: weatherByPoint(request: { lat: 50.595414, lon: 36.587277 }) {
    ...WeatherData
  }
  Sochi: weatherByPoint(request: { lat: 43.585472, lon: 39.723098 }) {
    ...WeatherData
  }
}

fragment WeatherData on Weather {
  forecast {
    days {
      time
      summary {
        day {
          avgTemperature
          precType
          prec
          humidity
          pressure
        }
      }
    }
  }
}
"""

clear_src = """DELETE FROM src.weather_src"""

insert_in_src = """
INSERT INTO src.weather_src (city, forecast_for, temperature, prec_type, prec, humidity, pressure)
VALUES (%s, %s, %s, %s, %s, %s, %s);
"""

initial_query = """
CREATE SCHEMA IF NOT EXISTS odc;
CREATE SCHEMA IF NOT EXISTS src;

CREATE TABLE IF NOT EXISTS src.weather_src (
    ID SERIAL,
    city TEXT NOT NULL,
    forecast_for TIMESTAMPTZ NOT NULL,
    temperature INT,
    prec_type TEXT,
    prec FLOAT,
    humidity INT,
    pressure INT
);
"""