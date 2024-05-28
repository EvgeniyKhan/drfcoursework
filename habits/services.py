import json
from datetime import datetime, timedelta

import requests
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from config.settings import TOKEN_TELEGRAM_BOT


def create_bot_telegram(chat_id, text):
    """
    Отправляет сообщение в Telegram чат.

    :param chat_id: ID чата в Telegram, куда будет отправлено сообщение
    :param text: Текст сообщения
    :raises Exception: Если возникла ошибка при отправке сообщения в Telegram
    """
    token = TOKEN_TELEGRAM_BOT  # замените на ваш токен Telegram бота
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()  # вызывает ошибку, если запрос не удался
    except requests.exceptions.RequestException as e:
        raise Exception(f"Ошибка при отправке сообщения в Telegram: {str(e)}")


def create_interval(habit, task_args=None, task_kwargs=None, expires_seconds=30):
    """
    Создает интервал и периодическую задачу для привычки.

    :param habit: объект привычки, для которой создается задача
    :param task_args: аргументы для задачи
    :param task_kwargs: ключевые аргументы для задачи
    :param expires_seconds: время истечения задачи в секундах
    """
    try:
        # Создание или получение интервала с заданной периодичностью (в днях)
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=habit.periodicity,
            period=IntervalSchedule.DAYS,
        )

        # Проверка и установка аргументов для задачи
        args = json.dumps(task_args) if task_args else None
        kwargs = json.dumps(task_kwargs) if task_kwargs else None

        # Создание периодической задачи с использованием созданного интервала
        PeriodicTask.objects.create(
            interval=schedule,
            name=f"Habit {habit.id}",  # Имя задачи с ID привычки для уникальности
            task="habit.tasks.send_message_habit",  # Полный путь к задаче отправки сообщения
            args=args,  # Аргументы для задачи
            kwargs=kwargs,  # Ключевые аргументы для задачи
            expires=datetime.utcnow()
            + timedelta(seconds=expires_seconds),  # Время истечения задачи
        )
    except Exception as e:
        # Обработка ошибки при создании задачи
        print(f"Ошибка при создании периодической задачи: {e}")
