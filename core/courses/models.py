from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=255, default=None)
    start_date = models.DateField()
    end_date = models.DateField()
    number_of_lectures = models.IntegerField()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
