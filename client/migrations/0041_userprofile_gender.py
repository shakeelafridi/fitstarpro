# Generated by Django 2.2 on 2020-12-17 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0040_userprofile_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='gender',
            field=models.TextField(default=''),
        ),
    ]
