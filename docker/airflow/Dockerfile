FROM apache/airflow:2.9.2

USER root
RUN apt-get update && apt-get install -y git python3-venv && apt-get clean && \
    python3 -m venv /opt/pipeline-env && \
    /opt/pipeline-env/bin/pip install --no-cache-dir \
        dbt-postgres==1.10.0 \
        sqlalchemy==2.0.30 \
        pandas==2.2.2 \
        numpy==2.0.0 \
        faker==40.11.1 \
        psycopg2-binary==2.9.12 \
        python-dotenv==1.1.0 && \
    chmod -R 755 /opt/pipeline-env

USER airflow
