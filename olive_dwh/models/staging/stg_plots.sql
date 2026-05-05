with source as (
    select * from {{ source('raw', 'plots') }}
),

renamed as (
    select
        id                              as plot_id,
        member_id                       as member_id,
        referencia_catastral            as referencia_catastral,
        municipio                       as municipio,
        provincia                       as provincia,
        superficie_ha                   as superficie_ha,
        variedad                        as variedad,
        sistema_riego                   as sistema_riego,
        _ingested_at                    as ingested_at
    from source
)

select * from renamed
