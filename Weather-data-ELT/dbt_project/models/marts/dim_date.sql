with daily as (
    select * from {{ ref('stg_weather_daily') }}
)

select distinct
    year,
    month,
    year_month_key,
    observation_date
from daily