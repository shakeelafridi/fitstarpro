# Generated by Django 2.2 on 2020-12-17 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0035_fitnessprofessionalprofile_number_of_reviews'),
    ]

    operations = [
        migrations.AddField(
            model_name='fitnesscenterprofile',
            name='number_of_reviews',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='fitnessmodalprofile',
            name='number_of_reviews',
            field=models.IntegerField(default=0),
        ),
    ]