# Modern Data Stack — Olive Oil Cooperative

Data Warehouse end-to-end para una cooperativa olivarera.
Centraliza datos de socios, parcelas, entregas, molturación y liquidaciones.

## Stack tecnológico

| Herramienta | Función |
|---|---|
| PostgreSQL | Base de datos (RAW / Staging / Marts) |
| Python | Generación de datos sintéticos e ingesta |
| dbt | Transformaciones SQL versionadas |
| Airflow | Orquestación del pipeline |
| Docker | Entorno reproducible |

## Arranque rápido

```bash
cp .env.example .env      # Copia y rellena las credenciales
docker compose up -d      # Levanta PostgreSQL
```

## Estructura

```
.
├── airflow/      # DAGs de Airflow
├── dbt/          # Modelos dbt (staging + marts)
├── src/          # Scripts Python (generador + ingesta)
├── data/         # Datos locales (ignorados por git)
├── docs/         # Documentación del proyecto
├── docker-compose.yml
├── .env.example
└── Makefile
```

## Capas del Data Warehouse

- **RAW** — Datos tal cual llegan al sistema
- **Staging** — Datos limpios, tipados y normalizados
- **Marts** — Modelo estrella listo para análisis
