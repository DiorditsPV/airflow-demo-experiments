Этот проект предназначен для экспериментов, отладки Airflow DAG и тестирования гипотез, связанных с использованием Airflow и сопутствующего стека.

## Running on

- Apache Airflow
- Pyspark
- DBT (Data Build Tool)
- PostgreSQL

## Структура проекта

- `dags/` - директория с DAG
- `dbt_projects/` - директория с DBT проектами
- `workflow_tools/` - директория со вспомогательным кодом
- `.env` - файл с переменными окружения
- `.gitignore` - файл с исключениями для Git
- `docker-compose.yaml` - конфигурация Docker Compose для развертывания сервисов

## Переменные окружения

Проект использует переменные окружения для конфигурации. Основные переменные:

- `AIRFLOW_VERSION` - версия Airflow
- `DB_USER`, `DB_PASSWORD`, `DB_NAME` - реквизиты доступа к БД
- `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` - реквизиты для отправки уведомлений в Telegram
- `DBT_PROJECTS_PATH` - путь к директории с DBT проектами
- `DBT_JAFFLE_SHOP_PATH` - путь к конкретному DBT проекту (Jaffle Shop)

Переменные окружения задаются в файле `.env` и используются в `docker-compose.yaml` для конфигурации сервисов.

## Запуск проекта

Для запуска проекта необходимо:

1. Клонировать репозиторий: `git clone https://github.com/DiorditsPV/airflow-demo-experiments.git`
2. `cd airflow-experimental`
3. Создать файл `.env` на основе `.env.example`
4. Запустить сервисы: `make full_up`
5. Airflow UI на `http://localhost:8080`, DBT UI на `http://localhost:9090`, Postgres на `localhost:5432`
