# Modern Data Stack — Cooperativa Olivarera de Jaén

Data Warehouse end-to-end para una cooperativa olivarera de Jaén.
Centraliza datos de socios, parcelas, entregas y liquidaciones de 5 campañas (2019-2024).

## Stack tecnológico

| Herramienta | Versión | Función |
|---|---|---|
| PostgreSQL | 16 | Base de datos (RAW / Staging / Marts) |
| Python | 3.x | Generación de datos sintéticos e ingesta |
| dbt | 1.10.0 | Transformaciones SQL versionadas y tests |
| Airflow | 2.9.2 | Orquestación del pipeline |
| Metabase | 0.52.6 | Visualización y dashboards |
| Docker | - | Entorno reproducible |

## Arranque rápido

```bash
# 1. Copia y rellena las credenciales
cp .env.example .env

# 2. Levanta todo el stack
docker-compose up -d

# 3. Accede a las herramientas
# Airflow:  http://localhost:8080  (admin / admin)
# Metabase: http://localhost:3000
```

## Estructura

```
.
├── airflow/
│   └── dags/
│       └── olive_pipeline.py   # DAG principal
├── docker/
│   ├── airflow/
│   │   ├── Dockerfile          # Imagen custom con dbt en venv
│   │   └── requirements.txt    # Dependencias del pipeline
│   └── postgres/
│       └── init.sql            # Crea la base de datos de Airflow
├── olive_dwh/                  # Proyecto dbt
│   ├── models/
│   │   ├── staging/            # Vistas de limpieza y tipado
│   │   └── marts/              # Tablas finales (modelo estrella)
│   ├── macros/
│   └── dbt_project.yml
├── src/
│   ├── generator/
│   │   └── generate_data.py    # Genera CSVs sintéticos
│   └── ingestion/
│       └── load_raw.py         # Carga CSVs en raw.*
├── dbt_profiles/
│   └── profiles.yml            # Conexión dbt → PostgreSQL
├── data/                       # Datos locales (ignorados por git)
├── docs/                       # Documentación del proyecto
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

## Pipeline

El DAG `olive_pipeline` en Airflow ejecuta 4 pasos en orden:

```
generar_datos → ingestar_raw → dbt_run → dbt_test
```

1. **generar_datos** — genera CSVs sintéticos con Faker y NumPy
2. **ingestar_raw** — carga los CSVs en el schema `raw.*` de PostgreSQL
3. **dbt_run** — transforma los datos en `staging.*` y `marts.*`
4. **dbt_test** — ejecuta 52 tests de calidad sobre los datos

## Capas del Data Warehouse

| Capa | Schema | Tipo | Descripción |
|---|---|---|---|
| RAW | `raw` | Tablas | Datos tal cual llegan al sistema |
| Staging | `staging` | Vistas | Datos limpios, tipados y normalizados |
| Marts | `marts` | Tablas | Modelo estrella listo para análisis |

### Tablas en Marts

| Tabla | Descripción |
|---|---|
| `dim_campaigns` | Campañas olivareras 2019-2024 |
| `dim_members` | Socios de la cooperativa |
| `dim_plots` | Parcelas agrícolas |
| `dim_quality` | Categorías de calidad del aceite |
| `fct_deliveries` | Entregas de aceituna por socio y parcela |
| `fct_settlements` | Liquidaciones económicas por campaña |

## Datos sintéticos

El generador produce datos realistas para la provincia de Jaén:

- **200 socios**, **~2.200 parcelas**, **~85.000 entregas**, **~970 liquidaciones**
- Variedad predominante: Picual (90%)
- Calidad: Virgen Extra (59%), Virgen (32%), Lampante (9%)
- Precio kg: de 0.44€ (2019) a 1.05€ (2024) — refleja la sequía real
