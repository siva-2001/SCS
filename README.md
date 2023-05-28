<!-- Создание базы данных и админа, запуск сервера и сопутствующих служб -->
pip install -r requirements.txt
python manage.py makemigrations SCSapp
python manage.py makemigrations translationApp
python manage.py makemigrations authorizationApp
python manage.py migrate
python manage.py createsuperuser
docker run -p 6379:6379 -d redis
python manage.py runserver

<!-- Создание тестового датасета -->
http://127.0.0.1:8000/createTestDataset/


