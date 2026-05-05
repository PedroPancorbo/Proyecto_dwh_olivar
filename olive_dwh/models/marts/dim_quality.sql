with quality as (
    select * from {{ ref('stg_quality_grades') }}
)

select
    quality_grade_id,
    categoria,
    acidity_max,
    descripcion
from quality
