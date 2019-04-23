from django.db import models
from django.utils.timezone import now
import random
import datetime

# Create your models here.


class Data(models.Model):
    title = models.CharField(max_length=128)
    number = models.IntegerField()
    create_time = models.DateTimeField(default=now)

    def __str__(self):
        return "{} {}".format(self.title,self.number)

    @classmethod
    def _delete_data(cls):
        Data.objects.all().delete()


    @classmethod
    def _create_data(cls,title,count=1000):
        for i in range(0,count):
            Data.objects.create(title=title,number=random.randint(1,1000),create_time=now()-datetime.timedelta(days=random.randint(1,100)))