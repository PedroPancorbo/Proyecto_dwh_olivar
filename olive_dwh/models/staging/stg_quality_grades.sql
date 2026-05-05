with source as (
    select * from {{ source('raw', 'quality_grades') }}
),

renamed as (
    select
        id                              as quality_grade_id,
        categoria                       as categoria,
        acidity_max                     as acidity_max,
        descripcion                     as descripcion,
        _ingested_at                    as ingested_at
    from source
)

select * from renamed
