# Generated by Django 3.0.2 on 2020-01-27 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sn_network', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content',
            field=models.TextField(null=True),
        ),
    ]
