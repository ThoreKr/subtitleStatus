# Generated by Django 2.1.4 on 2019-01-02 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0002_auto_20190102_2018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talk',
            name='amara_activity_last_checked',
            field=models.DateTimeField(blank=True, default='1970-01-01 00:00+01:00'),
        ),
        migrations.AlterField(
            model_name='talk',
            name='amara_complete_update_last_checked',
            field=models.DateTimeField(blank=True, default='1970-01-01 00:00+01:00'),
        ),
        migrations.AlterField(
            model_name='talk',
            name='next_amara_activity_check',
            field=models.DateTimeField(blank=True, default='1970-01-01 00:00+01:00'),
        ),
    ]