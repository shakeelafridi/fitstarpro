# Generated by Django 3.0.4 on 2021-04-07 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0085_auto_20210407_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fitnessprofessionalprofile',
            name='note_about_training_rates',
            field=models.CharField(default='', max_length=999),
        ),
        migrations.AlterField(
            model_name='fitnessprofessionalprofile',
            name='training_methods_and_styles',
            field=models.CharField(default='', max_length=999),
        ),
    ]
