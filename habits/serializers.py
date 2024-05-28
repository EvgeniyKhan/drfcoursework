from rest_framework import serializers

from habits.models import Habit
from habits.validators import (
    DurationValidator,
    HabitRelatedIsNiceValidator,
    NiceHabitValidator,
    PeriodicValidator,
    RewardHabitValidator,
)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"

    def validate(self, data):
        # Применение валидатора для проверки наличия либо связанной привычки, либо вознаграждения
        RewardHabitValidator("related_habit", "reward")(data)

        # Применение валидатора для проверки, что связанная привычка является приятной
        HabitRelatedIsNiceValidator("related_habit")(data)

        # Применение валидатора для проверки, что у приятной привычки нет связанной привычки и вознаграждения
        NiceHabitValidator("related_habit", "reward", "nice_habit")(data)

        # Применение валидатора для проверки, что время выполнения привычки не превышает 120 секунд
        DurationValidator("time_to_complete")(data)

        # Применение валидатора для проверки, что периодичность выполнения привычки находится в диапазоне от 1 до 7 дней
        PeriodicValidator("periodicity")(data)

        return data
