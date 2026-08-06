with daily as (
    select * from {{ ref('stg_weather_daily') }}
)

select 
    country_code,
    observation_date,
    year_month_key,
    (country_code
    || '|'
    || round(latitude::numeric, 2)::text
    || '|'
    || round(longitude::numeric, 2)::text) as location_key,
    temp_mean_c,
    temp_max_c,
    temp_min_c,
    precip_mm
from daily