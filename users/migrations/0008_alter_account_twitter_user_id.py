# Generated by Django 3.2 on 2022-02-22 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_account_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='twitter_user_id',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]