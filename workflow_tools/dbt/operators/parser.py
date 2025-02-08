import json
import logging
import os
from typing import Optional, Dict, Any

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup


class DbtModelParser:
    """
    Парсер dbt проекта для создания групп задач в Airflow DAG

    Args:
        dag: Airflow DAG
        project_dir: Директория с dbt_project.yml
        profiles_dir: Директория с profiles.yml
        target: Целевой профиль dbt (dev, prod и т.д.)
        tag: Опциональный тег для фильтрации моделей
        run_group_name: Название группы задач для dbt run
        test_group_name: Название группы задач для dbt test
    """

    def __init__(
        self,
        dag: DAG,
        project_dir: str,
        profiles_dir: str,
        target: str,
        tag: Optional[str] = None,
        run_group_name: str = "dbt_run",
        test_group_name: str = "dbt_test",
    ):
        self.dag = dag
        self.project_dir = project_dir
        self.profiles_dir = profiles_dir
        self.target = target
        self.tag = tag

        self.run_group = TaskGroup(run_group_name)
        self.test_group = TaskGroup(test_group_name)

        self._create_task_groups()

    def _load_manifest(self) -> Dict[str, Any]:
        """Загрузка dbt manifest.json"""
        manifest_path = os.path.join(self.project_dir, "target/manifest.json")
        with open(manifest_path) as f:
            return json.load(f)

    def _create_dbt_task(self, node_name: str, operation: str) -> BashOperator:
        """
        Создание задачи для dbt операции
        
        Args:
            node_name: Имя ноды из manifest
            operation: Операция (run/test)
        """
        model_name = node_name.split(".")[-1]
        task_group = self.test_group if operation == "test" else self.run_group
        
        if operation == "test":
            node_name = node_name.replace("model", "test")

        return BashOperator(
            task_id=node_name,
            task_group=task_group,
            bash_command=(
                f"/home/airflow/.local/bin/dbt {operation} "
                f"--target {self.target} --models {model_name} "
                f"--profiles-dir {self.profiles_dir} --project-dir {self.project_dir}"
            ),
            env={
                "DBT_USER": "{{ conn.postgres.login }}",
                "DBT_ENV_SECRET_PASSWORD": "{{ conn.postgres.password }}",
                "DBT_HOST": "{{ conn.postgres.host }}",
                "DBT_SCHEMA": "{{ conn.postgres.schema }}",
                "DBT_PORT": "{{ conn.postgres.port }}",
            },
            dag=self.dag,
        )

    def _create_task_groups(self) -> None:
        """Создание групп задач на основе manifest.json"""
        manifest = self._load_manifest()
        tasks = {}

        # Создаем задачи
        for node_name, node in manifest["nodes"].items():
            if not node_name.startswith("model."):
                continue
                
            if self.tag and self.tag not in node["tags"]:
                continue

            tasks[node_name] = self._create_dbt_task(node_name, "run")
            test_node = node_name.replace("model", "test")
            tasks[test_node] = self._create_dbt_task(node_name, "test")

        # Устанавливаем зависимости
        for node_name, node in manifest["nodes"].items():
            if not node_name.startswith("model."):
                continue
                
            if self.tag and self.tag not in node["tags"]:
                continue

            for upstream in node["depends_on"]["nodes"]:
                if upstream.startswith("model."):
                    tasks[upstream] >> tasks[node_name]

    @property
    def run_task_group(self) -> TaskGroup:
        """Группа задач для dbt run"""
        return self.run_group

    @property
    def test_task_group(self) -> TaskGroup:
        """Группа задач для dbt test"""
        return self.test_group 