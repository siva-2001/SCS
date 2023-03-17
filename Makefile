migrate: manage.py
	python manage.py makemigrations SCSapp
	python manage.py migrate

run: manage.py
	python manage.py runserver

updatedb:
	rm db.sqlite3
	rm -rf SCSapp/migrations
	python manage.py makemigrations SCSapp
	python manage.py migrate
	python manage.py createsuperuser
	python manage.py runserver

testdb:
	chromium http://127.0.0.1:8000/createTestDataset
