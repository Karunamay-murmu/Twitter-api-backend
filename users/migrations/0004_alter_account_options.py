# Generated by Django 3.2 on 2022-02-18 06:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_rename_user_account'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'ordering': ['-twitter_user_id'], 'verbose_name': 'Twitter User', 'verbose_name_plural': 'Twitter Users'},
        ),
    ]
