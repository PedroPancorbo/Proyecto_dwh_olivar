with source as (
    select * from {{ source('raw', 'deliveries') }}
),

renamed as (
    select
        id                              as delivery_id,
        campaign_id                     as campaign_id,
        member_id                       as member_id,
        plot_id                         as plot_id,
        quality_grade_id                as quality_grade_id,
        fecha_entrega                   as fecha_entrega,
        kg_netos                        as kg_netos,
        origen_recoleccion              as origen_recoleccion,
        rendimiento_teorico_pct         as rendimiento_teorico_pct,
        _ingested_at                    as ingested_at
    from source
)

select * from renamed
