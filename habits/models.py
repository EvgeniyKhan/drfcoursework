from django.db import models

from config.settings import NULLABLE
from users.models import User


class Habit(models.Model):
    PERIODICITY_CHOICES = (
        (1, 'Every Day'),
        (2, 'Every Week'),
        (3, 'Every Month'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Создатель")
    place = models.CharField(max_length=200, verbose_name="Место")
    time = models.TimeField(verbose_name="Время")
    action = models.CharField(max_length=200, verbose_name="Действие")
    nice_habit = models.BooleanField(
        default=False, verbose_name="Признак приятной привычки"
    )
    related_habit = models.ForeignKey(
        "Habit",
        on_delete=models.SET_NULL,
        verbose_name="Связанная привычка",
        **NULLABLE)
    periodicity = models.IntegerField(choices=PERIODICITY_CHOICES, verbose_name="Периодичность")
    reward = models.CharField(max_length=200, verbose_name="Вознаграждение", **NULLABLE)
    time_to_complete = models.PositiveSmallIntegerField(
        default=60, verbose_name="Время на выполнение"
    )
    is_public = models.BooleanField(
        default=False, verbose_name="Признак публичности"
    )

    def __str__(self):
        return (
            f"Пользователь: {self.user}\n"
            f"Действие: {self.action}\n"
            f"Время: {self.time}\n"
            f"Место: {self.place}"
        )

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
