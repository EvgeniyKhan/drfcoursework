Трекер полезных привычек (Habit Tracker)

Трекер полезных привычек — это веб-приложение для отслеживания и управления вашими полезными привычками. Пользователи могут создавать, редактировать и удалять свои привычки, а также просматривать публичные привычки других пользователей.

Функциональные возможности
Регистрация и авторизация пользователей
CRUD операции для привычек
Пагинация списка привычек (по 5 на страницу)
Просмотр списка публичных привычек
Уведомления о привычках через Telegram
Безопасность с использованием CORS
Документация API
Установка
Клонирование репозитория

bash
Копировать код
git clone https://github.com/EvgeniyKhan/drfcoursework.git
cd drfhomework
Настройка виртуального окружения

bash
Копировать код
python -m venv env
source env/bin/activate  # Для Windows: env\Scripts\activate
Установка зависимостей

bash
Копировать код
pip install -r requirements.txt
Настройка базы данных
Убедитесь, что у вас установлен PostgreSQL. Создайте базу данных для вашего проекта.

bash
Копировать код
psql -U postgres
CREATE DATABASE habit_tracker;
Настройте settings.py для подключения к базе данных:

python
Копировать код
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'habit_tracker',
        'USER': 'postgres',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
Применение миграций и создание суперпользователя

bash
Копировать код
python manage.py migrate
python manage.py createsuperuser
Запуск проекта
Запуск проекта без Docker

bash
Копировать код
python manage.py runserver
Проверка работоспособности Docker

bash
Копировать код
docker run hello-world
Запуск проекта с использованием Docker и Docker-compose

Сборка контейнеров
bash
Копировать код
docker-compose build
Запуск контейнеров
bash
Копировать код
docker-compose up
Приложение будет доступно по адресу http://localhost:8000.

Использование
Регистрация и авторизация

Используйте API для регистрации и авторизации пользователей. Токены можно получить и обновить по следующим маршрутам:

Получение токена: /users/token/
Обновление токена: /users/token/refresh/
CRUD операции для привычек

Создание привычки: /habits/create/
Просмотр списка привычек: /habits/
Просмотр списка публичных привычек: /habits/public/
Просмотр конкретной привычки: /habits/view/<int:pk>/
Обновление привычки: /habits/update/<int:pk>/
Удаление привычки: /habits/delete/<int:pk>/
Уведомления через Telegram
Настройте интеграцию с Telegram для получения уведомлений о привычках. Инструкции по настройке можно найти в документации проекта.

Документация
Документация API доступна по адресу http://localhost:8000/api/schema/swagger-ui/ (Swagger UI) и http://localhost:8000/api/schema/redoc/ (ReDoc).

Лицензия
Этот проект лицензирован под лицензией MIT. См. файл LICENSE для получения подробной информации.

