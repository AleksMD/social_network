# Generated by Django 3.0.2 on 2020-01-28 12:12

from django.db import migrations, models
import sn_network.models


class Migration(migrations.Migration):

    dependencies = [
        ('sn_network', '0006_auto_20200127_2039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_of_join',
            field=models.DateTimeField(default=sn_network.models.pretty_datetime),
        ),
    ]
