# Generated by Django 3.0.2 on 2020-01-29 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sn_network', '0009_auto_20200129_1144'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
