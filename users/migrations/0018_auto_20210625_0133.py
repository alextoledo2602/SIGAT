# Generated by Django 3.2.3 on 2021-06-25 05:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_profile_email_confirmed'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={},
        ),
        migrations.AlterModelTable(
            name='profile',
            table='profiles',
        ),
        migrations.AlterModelTable(
            name='user',
            table='users',
        ),
    ]
