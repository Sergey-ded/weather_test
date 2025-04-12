CREATE SCHEMA odc;
CREATE SCHEMA src;

create table src.weather_src(
    ID Serial
    , city text not null
    , forecast_for TIMESTAMPTZ not null
    , temperature int
    , prec_type text
    , prec float
    , humidity int
    , pressure int
);