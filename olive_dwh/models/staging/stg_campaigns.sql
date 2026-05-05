with source as (
    select * from {{ source('raw', 'campaigns') }}
),

renamed as (
    select
        id                              as campaign_id,
        nombre                          as nombre,
        anio_inicio                     as anio_inicio,
        anio_fin                        as anio_fin,
        estado                          as estado,
        _ingested_at                    as ingested_at
    from source
)

select * from renamed