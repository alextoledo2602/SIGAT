# Generated by Django 3.2.3 on 2021-09-06 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_auto_20210625_0133'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_valid_profile',
            field=models.BooleanField(default=False),
        ),
    ]
