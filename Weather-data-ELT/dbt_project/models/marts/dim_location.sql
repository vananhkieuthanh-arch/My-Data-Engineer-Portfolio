with daily as (
    select * from {{ ref('stg_weather_daily') }}
)

select distinct
    (country_code
    || '|'
    || round(latitude::numeric, 2)::text
    || '|'
    || round(longitude::numeric, 2)::text) as location_key,
    country_code,
    round(latitude::numeric, 2) as latitude,
    round(longitude::numeric, 2) as longitude,
    elevation_m,
    timezone
from daily