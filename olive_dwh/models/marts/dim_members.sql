with members as (
    select * from {{ ref('stg_members') }}
)

select
    member_id,
    nombre,
    apellidos,
    nombre || ' ' || apellidos     as nombre_completo,
    nif,
    municipio,
    provincia,
    fecha_alta,
    estado
from members
