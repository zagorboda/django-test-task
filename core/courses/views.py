from django.http import Http404
from rest_framework import viewsets, pagination, generics, filters
from rest_framework.exceptions import ParseError
from rest_framework.response import Response

from .serializers import CourseListSerializer, CourseDetailSerializer
from .models import Course

from datetime import datetime


class CustomPageNumberPagination(pagination.PageNumberPagination):
    """
    Custom number pagination
    """
    page_size = 10
    max_page_size = 100
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'limit': self.page_size,
            'results': data
        })


class CourseList(generics.ListCreateAPIView):
    """
        View to list and create course objects
    """
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        """
            Return list serializer on get request and detail serializer on post request.
            List serializer contain only name, detail serializer contain all fields.
        :return: serializer class
        """
        if self.request.method == 'POST':
            return CourseDetailSerializer
        return CourseListSerializer

    def get_queryset(self):
        """
            Return queryset, if there are query params (name, start_date, end_date) filter queryset
            and return it.
        :return: queryset
        """
        name = self.request.GET.get('name')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        queryset = Course.objects.all()

        query_param_error = dict()

        if not any((name, start_date, end_date)):
            #return raw queryset if no params
            return queryset

        if name:
            queryset = queryset.filter(name__icontains=name)

        if start_date:
            # Validate date: if date is in right format - return queryset, else - collect error to raise ParseError
            if not self.validate_date(start_date):
                query_param_error['start_date'] = 'Date has wrong format. Use these formats instead: YYYY-MM-DD.'
            else:
                queryset = queryset.filter(start_date__gte=start_date)
        if end_date:
            if not self.validate_date(end_date):
                query_param_error['end_date'] = 'Date has wrong format. Use these formats instead: YYYY-MM-DD.'
            else:
                queryset = queryset.filter(end_date__lte=end_date)

        if query_param_error:
            raise ParseError(query_param_error)

        return queryset

    def validate_date(self, date_string):
        """
            Check if date is valid. If yes - return True, else None
        :return: True or None
        """
        try:
            datetime.strptime(date_string, '%Y-%m-%d')
        except ValueError:
            return None
        return True


class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
