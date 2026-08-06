with source as (
    select * from {{ source('raw', 'weather_daily') }}
),

renamed as (
    select
        country_code,
        observation_date,
        extract(year from observation_date)::int as year,
        extract(month from observation_date)::int as month,
        (extract(year from observation_date)::int * 100 
            + extract(month from observation_date)::int) as year_month_key,
        response_lat as latitude,
        response_long as longitude,
        elevation_m,
        temp_mean_c,
        temp_max_c,
        temp_min_c,
        precip_mm,
        time_zone as timezone,
        extracted_at
    from source
    where observation_date is not null
        and country_code is not null
    )

select * from renamed
    