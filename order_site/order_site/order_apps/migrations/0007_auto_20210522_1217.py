# Generated by Django 3.1.1 on 2021-05-22 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order_apps', '0006_auto_20210522_1032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemorder',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='order_apps.order'),
        ),
    ]
