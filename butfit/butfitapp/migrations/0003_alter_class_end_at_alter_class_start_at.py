# Generated by Django 4.0.1 on 2022-01-05 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('butfitapp', '0002_alter_user_credit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='end_at',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='class',
            name='start_at',
            field=models.CharField(max_length=50),
        ),
    ]
