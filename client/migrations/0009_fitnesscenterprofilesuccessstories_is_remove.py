# Generated by Django 2.2 on 2020-11-19 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0008_fitnesscenterprofile_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='fitnesscenterprofilesuccessstories',
            name='is_remove',
            field=models.BooleanField(default=False),
        ),
    ]
