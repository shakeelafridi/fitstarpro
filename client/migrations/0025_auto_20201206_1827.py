# Generated by Django 2.2 on 2020-12-06 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0024_fitnesscenterratinginput_fitnessmodalratinginput_fitnessprofessionalratinginput'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fitnesscenterprofile',
            name='member_ship_plans',
            field=models.TextField(default=''),
        ),
    ]
