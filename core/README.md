This project is my test task for Yalantis Python school.

## Setup

`git@github.com:zagorboda/django-test-task.git`
    

	python -m venv env
	source env/bin/activate
	cd django-test-task
	pip install -r requirements.txt


Run migrations

	python manage.py migrate
    
Start server

	python manage.py runserver

## Versions
Python 3.8\
Django 2.2 \
Django Rest Framework 3.12

## Usage
Main page (/) return paginated list of courses()only name and detail view url), allow filtering results with query parameters and receive post request to create new course.

Post request  must include next fields: `name (string(255)); start_date, end_date (DateField(YYYY-MM-DD)); number_of_lectures (integer)`.

To filter result use next query params: name, start_date, end_date. Start_date will include courses that start after that date, end_date will include courses that ends before that date.
Example: `GET /?name=car&start_date=2021-05-05&end_date=2021-10-05` will return course, that contain 'car' in name, start after 2021-05-05 and end before 2021-10-05, `GET /start_date=2021-05-05`
will return courses that starts after 2021-05-05 and so on.

Course detail page (/{id}/) provide retrieve, put and patch actions.
GET request return full info about course (name, id, both dates, number of lectures and self url). Both put and patch actions are supported, we can change every field except id.
 

### Tests
To run tests 

	python manage.py test

### Database
Repo include sqlite db file. It already include superuser `admin: admin`, and several objects.
To populate db automatically i had wrote simple script populate_db.py using Faker library.
