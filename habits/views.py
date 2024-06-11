from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from habits.models import Habit
from habits.paginations import HabitPaginator
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer


class HabitCreateAPIView(generics.CreateAPIView):
    """
    API View для создания новой привычки.

    Использует сериализатор HabitSerializer и разрешение AllowAny,
    что позволяет любому пользователю создать привычку.
    """

    serializer_class = HabitSerializer
    permission_classes = [AllowAny]


class HabitListAPIView(generics.ListAPIView):
    """
    API-представление для получения списка привычек для аутентифицированного пользователя.

    - Доступ к этому представлению имеют только аутентифицированные пользователи.
    - Пользователи могут видеть только свои собственные привычки.
    - Результаты пагинируются с использованием кастомного класса HabitPaginator.

    Атрибуты:
        serializer_class (HabitSerializer): Класс сериализатора, используемый для представления привычек.
        permission_classes (list): Список классов разрешений, которые должен удовлетворить пользователь для доступа к этому представлению.
        pagination_class (HabitPaginator): Класс пагинации для управления пагинацией результатов.
    """

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = HabitPaginator

    def get_queryset(self):
        """
        Возвращает набор данных привычек для аутентифицированного пользователя.

        Этот метод фильтрует объекты Habit, чтобы включить только те,
        которые принадлежат текущему пользователю, выполняющему запрос.

        Возвращает:
            QuerySet: Набор данных привычек для аутентифицированного пользователя.
        """
        return Habit.objects.filter(user=self.request.user)


class HabitPublicListAPIView(generics.ListAPIView):
    """
    API-представление для получения списка публичных привычек.

    - Доступ к этому представлению имеет любой пользователь, независимо от аутентификации.
    - Показываются только те привычки, которые отмечены как публичные (is_public=True).
    - Результаты пагинируются с использованием кастомного класса HabitPaginator.

    Атрибуты:
        queryset (QuerySet): Набор данных, содержащий только публичные привычки.
        serializer_class (HabitSerializer): Класс сериализатора, используемый для представления привычек.
        permission_classes (list): Список классов разрешений, позволяющих доступ к этому представлению любому пользователю.
        pagination_class (HabitPaginator): Класс пагинации для управления пагинацией результатов.
    """

    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
    permission_classes = [AllowAny]
    pagination_class = HabitPaginator


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """
    API-представление для получения конкретной привычки.

    - Доступ к этому представлению имеют только аутентифицированные пользователи.
    - Пользователи могут получить доступ только к своим собственным привычкам.

    Атрибуты:
        serializer_class (HabitSerializer): Класс сериализатора, используемый для представления привычек.
        permission_classes (list): Список классов разрешений, которые должен удовлетворить пользователь для доступа к этому представлению.
        queryset (QuerySet): Набор данных, содержащий все привычки.
    """

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Habit.objects.all()


class HabitUpdateAPIView(generics.UpdateAPIView):
    """
    API-представление для обновления конкретной привычки.

    - Доступ к этому представлению имеют только аутентифицированные пользователи.
    - Пользователи могут обновлять только свои собственные привычки.

    Атрибуты:
        serializer_class (HabitSerializer): Класс сериализатора, используемый для представления привычек.
        permission_classes (list): Список классов разрешений, которые должен удовлетворить пользователь для доступа к этому представлению.
        queryset (QuerySet): Набор данных, содержащий все привычки.
    """

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Habit.objects.all()


class HabitDestroyAPIView(generics.DestroyAPIView):
    """
    API-представление для удаления конкретной привычки.

    - Доступ к этому представлению имеют только аутентифицированные пользователи.
    - Пользователи могут удалять только свои собственные привычки.

    Атрибуты:
        serializer_class (HabitSerializer): Класс сериализатора, используемый для представления привычек.
        permission_classes (list): Список классов разрешений, которые должен удовлетворить пользователь для доступа к этому представлению.
        queryset (QuerySet): Набор данных, содержащий все привычки.
    """

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Habit.objects.all()
