import datetime
import os
import pathlib
import random
import sys

import django
from faker import Faker

sys.path.append(str(pathlib.Path(__file__).parent.absolute().parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from courses.models import Course


def create_courses(number_of_courses):
    fake = Faker()
    for i in range(number_of_courses):
        name = fake.sentence(nb_words=8)
        start_date = fake.date_between('today', '+1y')
        end_date = start_date + datetime.timedelta(days=random.randint(10, 100))
        number_of_lectures = random.randint(5, 60)

        Course.objects.create(name=name, start_date=start_date, end_date=end_date, number_of_lectures=number_of_lectures)


create_courses(120)
