# Generated by Django 3.2 on 2022-02-23 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_account_access_token_secret'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='access_token',
            field=models.TextField(),
        ),
    ]
