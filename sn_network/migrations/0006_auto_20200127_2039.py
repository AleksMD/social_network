# Generated by Django 3.0.2 on 2020-01-27 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sn_network', '0005_auto_20200127_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='users_likes',
            field=models.ManyToManyField(blank=True, related_name='like_it', to='sn_network.User'),
        ),
    ]