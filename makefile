django:
	python epic_event/manage.py runserver

migration:
	python epic_event/manage.py makemigrations

migrate:
	python epic_event/manage.py migrate

flush:
	python epic_event/manage.py flush
	python epic_event/manage.py loaddata epic_event/fixtures/departments.json
