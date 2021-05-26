# Generated by Django 3.2.3 on 2021-05-25 09:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_apps', '0008_order_paid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meson',
            name='event_end',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='meson',
            name='event_start',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
    ]