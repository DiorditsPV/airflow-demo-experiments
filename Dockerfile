ARG AIRFLOW_VERSION=2.5.3
FROM apache/airflow:slim-${AIRFLOW_VERSION}-python3.10

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        vim \
        curl \
        git \
        postgresql-client \
        build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ------------- 
USER airflow
COPY --chown=airflow:root requirements.txt /opt/airflow/requirements.txt
COPY --chown=airflow:root post-entrypoint.sh /opt/airflow/scripts/post-entrypoint.sh
COPY --chown=airflow:root volumes/config/airflow.cfg /opt/airflow/airflow.cfg
# COPY --chown=airflow:root .env /opt/airflow/.env

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /opt/airflow/requirements.txt

WORKDIR ${AIRFLOW_HOME}
RUN mkdir -p \
    /opt/airflow/dags \
    /opt/airflow/logs \
    /opt/airflow/plugins \
    /opt/airflow/scripts \
    /opt/airflow/config && \
    chmod +x /opt/airflow/scripts/post-entrypoint.sh


EXPOSE 8080 9090

ENV PYTHONPATH=/opt/airflow
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

HEALTHCHECK --interval=30s --timeout=30s --retries=3 \
    CMD curl --fail http://localhost:8080/health || exit 1

ENTRYPOINT ["bash", "-c", "\
    airflow db init \
    && bash /opt/airflow/scripts/post-entrypoint.sh \
    && airflow standalone \
"]
