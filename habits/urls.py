from django.urls import path
from rest_framework.routers import DefaultRouter

from habits.apps import HabitsConfig
from habits.views import (
    HabitCreateAPIView,
    HabitDestroyAPIView,
    HabitListAPIView,
    HabitPublicListAPIView,
    HabitRetrieveAPIView,
    HabitUpdateAPIView,
)

app_name = HabitsConfig.name

router = DefaultRouter()

urlpatterns = [
    path("", HabitListAPIView.as_view(), name="list_habit"),
    path("create/", HabitCreateAPIView.as_view(), name="create_habit"),
    path("public/", HabitPublicListAPIView.as_view(), name="public_habit_list"),
    path("view/<int:pk>/", HabitRetrieveAPIView.as_view(), name="view_habit"),
    path("update/<int:pk>/", HabitUpdateAPIView.as_view(), name="update_habit"),
    path("delete/<int:pk>/", HabitDestroyAPIView.as_view(), name="delete_habit"),
]
