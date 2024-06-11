from rest_framework.serializers import ValidationError


class RewardHabitValidator:
    """
    Валидатор для проверки наличия либо связанной привычки, либо вознаграждения.
    """

    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2

    def __call__(self, value):
        related_habit = dict(value).get(self.field1)
        reward = dict(value).get(self.field2)

        if related_habit and reward:
            raise ValidationError(
                "Можно добавить связанную привычку либо вознаграждение, но не оба сразу!"
            )


class HabitRelatedIsNiceValidator:
    """
    Валидатор для проверки, что связанная привычка является приятной.
    """

    def __init__(self, field1):
        self.field1 = field1

    def __call__(self, value):
        related_habit = dict(value).get(self.field1)
        if related_habit and not related_habit.nice_habit:
            raise ValidationError(
                "Связанной привычкой может быть только приятная привычка!"
            )


class NiceHabitValidator:
    """
    Валидатор для проверки, что у приятной привычки нет связанной привычки и вознаграждения.
    """

    def __init__(self, field1, field2, field3):
        self.field1 = field1
        self.field2 = field2
        self.field3 = field3

    def __call__(self, value):
        related_habit = dict(value).get(self.field1)
        reward = dict(value).get(self.field2)
        nice_habit = dict(value).get(self.field3)

        if nice_habit:
            if related_habit:
                raise ValidationError(
                    "У приятной привычки не может быть связанной привычки!"
                )
            if reward:
                raise ValidationError(
                    "У приятной привычки не может быть вознаграждения!"
                )


class DurationValidator:
    """
    Валидатор для проверки, что время выполнения привычки не превышает 120 секунд.
    """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        time_to_complete = dict(value).get(self.field)

        if time_to_complete and time_to_complete >= 120:
            raise ValidationError(
                "Превышено время выполнения привычки, не более 120 секунд!"
            )


class PeriodicValidator:
    """
    Валидатор для проверки, что периодичность выполнения привычки находится в диапазоне от 1 до 7 дней.
    """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        periodicity = dict(value).get(self.field)

        if periodicity and (periodicity < 1 or periodicity > 7):
            raise ValidationError(
                "Интервал задания периодичности должен быть от 1 до 7 дней!"
            )
        if periodicity == 0:
            raise ValidationError("Периодичность не может быть равна нулю!")
