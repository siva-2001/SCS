migrate: manage.py
	python manage.py makemigrations SCSapp
	python manage.py migrate

run: manage.py
    docker run -p 6379:6379 -d redis
	python manage.py runserver

updatedb:
	rm db.sqlite3
	rm -rf SCSapp/migrations
	python manage.py makemigrations SCSapp
	python manage.py migrate
	python manage.py createsuperuser

testdb:
	chromium http://127.0.0.1:8000/createTestDataset
