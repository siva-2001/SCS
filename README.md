<!-- Создание базы данных и админа, запуск сервера -->
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver


<!-- Создание тестового датасета -->
http://127.0.0.1:8000/createTestDataset/

<!-- Авторизация -->
http://127.0.0.1:8000/api-token-auth/

<!-- Получение данных соревнований -->
http://127.0.0.1:8000/api/v1/test