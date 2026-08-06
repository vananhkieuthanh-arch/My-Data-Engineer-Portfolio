with daily as (
    select * from {{ ref('fct_weather_daily') }}
)

select
    country_code,
    year_month_key,
    location_key,
    avg(temp_mean_c) as avg_temp_mean_c,
    avg(temp_max_c)  as avg_temp_max_c,
    avg(temp_min_c)  as avg_temp_min_c,
    max(temp_max_c)  as max_temp_max_c,   -- hottest day in the month
    min(temp_min_c)  as min_temp_min_c,   -- coldest day in the month
    sum(precip_mm)   as total_precip_mm,
    count(*)         as days_count
from daily
group by
    country_code,
    year_month_key,
    location_key
order by
    year_month_key