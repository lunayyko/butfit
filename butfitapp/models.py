from django.db import models

class User(models.Model):
    phone    = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=200, null=False)
    role     = models.CharField(max_length=15, default='common')
    credit   = models.IntegerField(default=0)
    class Meta:
        db_table = 'users'

class Class(models.Model):
    name        = models.CharField(max_length=200)
    location    = models.CharField(max_length=100)
    class_type  = models.CharField(max_length=100)
    price       = models.PositiveIntegerField(default=1)
    capacity    = models.PositiveIntegerField(default=1)
    date        = models.DateField()
    start_at    = models.DateTimeField()
    end_at      = models.DateTimeField()

    class Meta:
        db_table = 'classes'