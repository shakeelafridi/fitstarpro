# Generated by Django 2.2 on 2020-12-24 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0051_auto_20201224_1638'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fitnessmodalprofile',
            name='address2',
        ),
        migrations.RemoveField(
            model_name='fitnessmodalprofile',
            name='address3',
        ),
        migrations.RemoveField(
            model_name='fitnessmodalprofile',
            name='gym_used',
        ),
        migrations.RemoveField(
            model_name='fitnessmodalprofile',
            name='gym_used2',
        ),
        migrations.RemoveField(
            model_name='fitnessmodalprofile',
            name='gym_used3',
        ),
    ]