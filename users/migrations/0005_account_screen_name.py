# Generated by Django 3.2 on 2022-02-18 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_account_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='screen_name',
            field=models.CharField(default='screen_name', max_length=255, unique=True),
        ),
    ]
