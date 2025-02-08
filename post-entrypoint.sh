echo "Creating airflow user"
airflow users create \
    --role Admin \
    --username  user \
    --firstname user \
    --lastname user \
    --email user@example.com \
    --password ${AIRFLOW_USER_PASSWORD:-password0}
echo "Creating airflow user done"

if [ ! -f /opt/airflow/config/airflow.cfg ]; then
    cp /opt/airflow/airflow.cfg /opt/airflow/config/airflow.cfg
fi
