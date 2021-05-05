from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request

import json
import datetime

from courses.models import Course
from .serializers import CourseListSerializer


class DeleteCourseTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.course = Course.objects.create(
            name="New course",
            start_date="2021-05-05",
            end_date="2021-05-10",
            number_of_lectures=10
        )

        cls.client = Client()

    def test_delete_not_existing_object(self):
        """ Delete not existing course """
        url = reverse('course-detail', kwargs={'pk': '123'})
        response = self.client.delete(url)

        courses_count = Course.objects.all().count()

        self.assertEqual(courses_count, 1)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_existing_object(self):
        """ Successful delete existing course """

        url = reverse('course-detail', kwargs={'pk': self.course.id})
        response = self.client.delete(url)

        courses_count = Course.objects.all().count()

        self.assertEqual(courses_count, 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class DetailCourseTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.course = Course.objects.create(
            name="New course",
            start_date="2021-05-05",
            end_date="2021-05-10",
            number_of_lectures=10
        )

        cls.client = Client()

    def test_existing_course(self):
        """ Get request to existing course """
        response = self.client.get(reverse('course-detail', kwargs={'pk': self.course.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_existing_course(self):
        """ Get request to not existing course """
        response = self.client.get(reverse('course-detail', kwargs={'pk': '123'}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class EditCourseTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.course = Course.objects.create(
            name="New course",
            start_date="2021-05-05",
            end_date="2021-05-10",
            number_of_lectures=10
        )

        cls.client = Client()

    def test_patch_course_name(self):
        """ Patch request to change course name """
        data = json.dumps({'name': 'New patched course'})
        response = self.client.patch(reverse('course-detail', kwargs={'pk': self.course.id}), data, content_type='application/json')

        course = Course.objects.all().first()
        self.assertEqual(course.name, 'New patched course')
        self.assertEqual(response.data['name'], 'New patched course')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_course_start_date(self):
        """ Patch request to change start date """
        data = json.dumps({'start_date': '2021-05-07'})
        response = self.client.patch(reverse('course-detail', kwargs={'pk': self.course.id}), data, content_type='application/json')

        course = Course.objects.all().first()
        self.assertEqual(course.start_date, datetime.date.fromisoformat('2021-05-07'))
        self.assertEqual(response.data['start_date'], '2021-05-07')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_course_end_date(self):
        """ Patch request to change end date """
        data = json.dumps({'end_date': '2021-06-07'})
        response = self.client.patch(reverse('course-detail', kwargs={'pk': self.course.id}), data, content_type='application/json')

        course = Course.objects.all().first()
        self.assertEqual(course.end_date, datetime.date.fromisoformat('2021-06-07'))
        self.assertEqual(response.data['end_date'], '2021-06-07')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_course_lectures(self):
        """ Patch request to change number of lectures """
        data = json.dumps({'number_of_lectures': 43})
        response = self.client.patch(reverse('course-detail', kwargs={'pk': self.course.id}), data, content_type='application/json')

        course = Course.objects.all().first()
        self.assertEqual(course.number_of_lectures, 43)
        self.assertEqual(response.data['number_of_lectures'], 43)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ListCourseTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(15):
            cls.course = Course.objects.create(
                name="New course{}".format(i),
                start_date="2021-05-{}".format(i+1),
                end_date="2021-05-{}".format(i+7),
                number_of_lectures=10+i
            )

        cls.client = Client()
        cls.factory = RequestFactory()

    def test_list_courses(self):
        """ Test courses list """
        response = self.client.get(reverse('course-list'))

        response_data = []
        response_data.extend(response.data['results'])
        while response.data['next']:
            response = self.client.get(response.data['next'])
            response_data.extend(response.data['results'])


        request = self.factory.get(reverse('course-list'))
        test_request = Request(request)

        serializer_data = CourseListSerializer(Course.objects.all(), many=True, context={'request': test_request}).data

        self.assertEqual(repr(serializer_data), repr(response_data))

    def test_search_by_start_date(self):
        response = self.client.get('{}{}'.format(reverse('course-list'), '?start_date=2021-05-09'))

        request = self.factory.get(reverse('course-list'))
        test_request = Request(request)

        serializer_data = CourseListSerializer(Course.objects.filter(start_date__gte='2021-05-09'), many=True, context={'request': test_request}).data

        self.assertEqual(repr(serializer_data), repr(response.data['results']))

    def test_search_by_end_date(self):
        response = self.client.get('{}{}'.format(reverse('course-list'), '?end_date=2021-05-09'))

        request = self.factory.get(reverse('course-list'))
        test_request = Request(request)
        serializer_data = CourseListSerializer(Course.objects.filter(end_date__lte='2021-05-09'), many=True, context={'request': test_request}).data

        self.assertEqual(repr(serializer_data), repr(response.data['results']))

    def test_search_by_name(self):
        response = self.client.get('{}{}'.format(reverse('course-list'), '?name=1'))

        request = self.factory.get(reverse('course-list'))
        test_request = Request(request)
        serializer_data = CourseListSerializer(Course.objects.filter(name__icontains='1'), many=True, context={'request': test_request}).data

        self.assertEqual(repr(serializer_data), repr(response.data['results']))
