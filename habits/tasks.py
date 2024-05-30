import logging

from celery import shared_task
from django.utils import timezone

from habits.models import Habit
from habits.services import create_bot_telegram

logger = logging.getLogger(__name__)


@shared_task
def send_message_habit():
    """
    Функция для отправки уведомлений о привычках в Telegram.

    Эта функция запускает процесс отправки уведомлений пользователям
    о выполнении их привычек в установленное время.
    """
    logger.info("Запускаю отправку уведомления в телеграмм")
    now = timezone.now().time()

    habits = Habit.objects.filter(
        time_execute__hour=now.hour, time_execute__minute=now.minute
    )
    for habit in habits:
        try:
            text = (
                f"Напоминание о выполнении привычки\n"
                f"Выполнить: {habit.action}\n"
                f"Время: {habit.time}\n"
                f"Место: {habit.place}"
            )
            chat_id = habit.user.chat_id
            create_bot_telegram(chat_id, text)
            logger.info(
                f"Уведомление отправлено пользователю {habit.user} для привычки {habit.action}"
            )
        except Exception as e:
            logger.error(
                f"Ошибка при отправке уведомления для привычки {habit.action}: {str(e)}"
            )
