migrate: manage.py
	python manage.py makemigrations SCSapp
	python manage.py migrate

run: manage.py
	python manage.py runserver

gitpush:
	git add -A
	git commit -m "$(text)"
	git push -u origin master

updatedb:
	rm db.sqlite3
	rm -rf SCSapp/migrations
	python manage.py makemigrations SCSapp
	python manage.py migrate
	python manage.py createsuperuser
