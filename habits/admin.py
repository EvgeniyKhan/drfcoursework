from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('place', 'time', 'action', 'time_to_complete', 'get_periodicity', 'nice_habit', 'user')

    def get_periodicity(self, obj):
        return obj.get_periodicity_display()
    get_periodicity.short_description = 'Periodicity'

