# Generated by Django 4.0.1 on 2022-01-06 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('butfitapp', '0002_booking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credit',
            name='credit',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]