from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import Course


class CourseListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='course-detail', lookup_field='pk')

    class Meta:
        model = Course
        fields = ('name', 'url')


class CourseDetailSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='course-detail', lookup_field='pk')

    class Meta:
        model = Course
        fields = ('name', 'id', 'url', 'start_date', 'end_date', 'number_of_lectures')

    def validate(self, data):
        errors = dict()

        if 'end_date' in data and 'start_date' in data and data['end_date'] < data['start_date']:
            errors['end_date'] = "End date cannot be earlier than start date"

        if 'number_of_lectures' in data and data['number_of_lectures'] < 0:
            errors['number_of_lectures'] = "Number of lectures must be positive integer"

        if errors:
            raise ValidationError(errors)
        return data
