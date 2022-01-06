from django.db import models

from core.models import TimeStampModel

class User(models.Model):
    phone    = models.CharField(unique=True, null=False, max_length=50)
    password = models.CharField(max_length=200, null=False)
    role     = models.CharField(max_length=30, default='common')
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


class Credit(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    credit     = models.DecimalField(max_digits=5, decimal_places=2)
    expire_in  = models.IntegerField(default=1)

    class Meta:
        db_table = 'credits'

class Booking(models.Model):
    user     = models.ForeignKey(User, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name='class_id')

    class Meta:
        db_table = 'bookings'

class BookingLog(TimeStampModel):
    user     = models.ForeignKey(User, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    action   = models.CharField(max_length=50)

    class Meta:
        db_table = 'bookinglogs'