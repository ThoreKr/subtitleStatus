# Generated by Django 2.2.17 on 2021-01-23 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0169_auto_20210110_0240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talk',
            name='frab_id_talk',
            field=models.CharField(blank=True, default='-1', max_length=100),
        ),
    ]