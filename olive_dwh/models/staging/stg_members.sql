with source as (
    select * from {{ source('raw', 'members') }}
),

renamed as (
    select
        id                              as member_id,
        nombre                          as nombre,
        apellidos                       as apellidos,
        nif                             as nif,
        municipio                       as municipio,
        provincia                       as provincia,
        fecha_alta                      as fecha_alta,
        estado                          as estado,
        _ingested_at                    as ingested_at
    from source
)

select * from renamed