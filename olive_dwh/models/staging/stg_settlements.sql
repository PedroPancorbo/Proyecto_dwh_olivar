with source as (
    select * from {{ source('raw', 'settlements') }}
),

renamed as (
    select
        id                              as settlement_id,
        campaign_id                     as campaign_id,
        member_id                       as member_id,
        fecha_liquidacion               as fecha_liquidacion,
        kg_totales                      as kg_totales,
        precio_kg                       as precio_kg,
        importe_final                   as importe_final,
        _ingested_at                    as ingested_at
    from source
)

select * from renamed
