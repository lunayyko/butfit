from django.db import models

class User(models.Model):
    phone    = models.CharField(unique=True, null=False, max_length=50)
    password = models.CharField(max_length=200, null=False)
    role     = models.CharField(max_length=30, default='common')
    credit   = models.IntegerField(default=0)

    class Meta:
        db_table = 'users'


class Class(models.Model):
    name       = models.CharField(max_length=50)
    location   = models.CharField(max_length=50)
    class_type = models.CharField(max_length=50)
    price      = models.IntegerField(default=1)
    capacity   = models.IntegerField(default=20)
    date       = models.DateField()
    start_at   = models.CharField(max_length=50)
    end_at     = models.CharField(max_length=50)

    class Meta:
        db_table = 'classes'