import logging

import requests
from airflow.utils.context import Context

from utils.alert.alert_config.telegram_config import TELEGRAM_CONFIG

logger = logging.getLogger(__name__)


class TelegramNotifier:
    def __init__(self):
        self.token = TELEGRAM_CONFIG["BOT_TOKEN"]
        self.base_url = TELEGRAM_CONFIG["API_URL"]
        self.chat_id = TELEGRAM_CONFIG["CHAT_ID"]
        self.channel_id = TELEGRAM_CONFIG["CHANNEL_ID"]

        if not self.token:
            raise ValueError("Telegram BOT_TOKEN не настроен")
        if not self.chat_id:
            raise ValueError("Telegram CHAT_ID не настроен")

    def send_message(self, text: str):
        try:
            logger.info(f"Отправка сообщения в Telegram: {text}")
            response = requests.post(
                f"{self.base_url}{self.token}/sendMessage",
                json={
                    "chat_id": self.chat_id,
                    "text": text,
                    "parse_mode": "HTML",
                },
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при отправке сообщения в Telegram: {str(e)}")

    def send_state_message(self, state: str, context: Context):
        ti = context.get("task_instance")
        message = """
        Task: {task_id}
        DAG: {dag_id}
        Status: {state}
        Execution date: {execution_date}
        """
        message = message.format(ti.task_id, ti.dag_id, ti.state, ti.execution_date)

        if state == "failed":
            message += f"\nError: {context.get('exception')}"

        self.send_message(message)


def task_success_callback(context: Context):
    notifier = TelegramNotifier()
    notifier.send_state_message("success", context)


def task_failure_callback(context: Context):
    notifier = TelegramNotifier()
    notifier.send_state_message("failed", context)


if __name__ == "__main__":
    """Этот блок должен быть перемещен в отдельный модуль для тестирования"""

    notifier = TelegramNotifier()
    notifier.send_message("Hello, chat")
