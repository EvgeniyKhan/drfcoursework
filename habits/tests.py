from datetime import time

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from habits.models import Habit
from users.models import User


class HabitTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="testuser@example.com", password="testpassword"
        )
        self.habit = Habit.objects.create(
            place="Дом",
            time="21:00",
            action="Спать",
            time_to_complete=100,
            periodicity=1,
            nice_habit=True,
            user=self.user,
        )

    def test_habit_create(self):
        """Создание Привычки."""
        self.client.force_authenticate(user=self.user)
        data = {
            "place": "Офис",
            "time": "09:00",
            "action": "Работать",
            "time_to_complete": 60,
            "periodicity": 1,
            "nice_habit": True,
            "user": self.user.id,
        }
        response = self.client.post(reverse("habits:create_habit"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Habit.objects.all().exists())

        habit = Habit.objects.get(id=response.data["id"])
        self.assertEqual(habit.place, data["place"])
        self.assertEqual(habit.time.strftime("%H:%M"), data["time"])
        self.assertEqual(habit.action, data["action"])
        self.assertEqual(habit.time_to_complete, data["time_to_complete"])
        self.assertEqual(habit.periodicity, data["periodicity"])
        self.assertTrue(habit.nice_habit)
        self.assertEqual(habit.user, self.user)

        self.assertEqual(
            response.json(),
            {
                "id": habit.id,
                "place": habit.place,
                "time": habit.time.strftime("%H:%M:%S"),
                "action": habit.action,
                "time_to_complete": habit.time_to_complete,
                "periodicity": habit.periodicity,
                "nice_habit": habit.nice_habit,
                "reward": habit.reward,
                "is_public": habit.is_public,
                "user": habit.user.id,
                "related_habit": None,
            },
        )

    def test_habit_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("habits:list_habit"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.habit.place)

    def test_habit_detail(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse("habits:view_habit", kwargs={"pk": self.habit.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.habit.place)

    def test_habit_update(self):
        """Обновление информации по Привычке"""
        self.client.force_authenticate(user=self.user)
        data = {
            "place": "Улица",
            "time": "18:00",
            "action": "Гулять",
            "time_to_complete": self.habit.time_to_complete,  # добавить все необходимые поля
            "periodicity": self.habit.periodicity,
            "nice_habit": True,
        }
        response = self.client.patch(
            reverse("habits:update_habit", kwargs={"pk": self.habit.pk}),
            data=data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что данные были обновлены
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.place, data["place"])
        self.assertEqual(self.habit.time, time(18, 0))
        self.assertEqual(self.habit.action, data["action"])
        self.assertEqual(self.habit.nice_habit, data["nice_habit"])

    def test_reward_and_pleasant_habit(self):
        """Тестирование создания привычки с наградой и приятной привычкой одновременно"""
        self.client.force_authenticate(user=self.user)
        data = {
            "place": "Дом",
            "time": "21:00",
            "action": "Спать",
            "time_to_complete": "100",
            "periodicity": "every_day",
            "nice_habit": True,  # Используем булево значение, а не строку
            "reward": "Мороженное",
        }
        response = self.client.post(
            reverse("habits:create_habit"), data=data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validate_reward_for_useful_habit(self):
        """Тестирование Только полезные привычки могут иметь награду"""
        self.client.force_authenticate(user=self.user)  # Аутентифицируем пользователя
        data = {
            "place": "Дом",
            "time": "21:00",
            "action": "Спать",
            "time_to_complete": "100",
            "periodicity": "every_day",
            "nice_habit": True,  # Используем булево значение
            "reward": "Мороженное",
        }
        response = self.client.post(
            reverse("habits:create_habit"), data=data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validate_related_or_reward(self):
        """Тестирование либо вознаграждение, либо приятная привычка"""
        self.client.force_authenticate(user=self.user)  # Аутентифицируем пользователя

        data = {
            "place": "Дом",
            "time": "21:00",
            "action": "Спать",
            "time_to_complete": "100",
            "periodicity": "every_day",
            "nice_habit": True,  # Используем булево значение
            "reward": "Мороженное",
        }
        response = self.client.post(
            reverse("habits:create_habit"), data=data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
