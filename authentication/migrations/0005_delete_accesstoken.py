# Generated by Django 3.2 on 2022-02-27 12:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_auto_20220215_1525'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AccessToken',
        ),
    ]
