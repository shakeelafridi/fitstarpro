# Generated by Django 3.1.3 on 2021-02-13 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0058_auto_20210211_1359'),
    ]

    operations = [
        migrations.AddField(
            model_name='fitnessprofessionalprofile',
            name='availability_for_on_line_training',
            field=models.IntegerField(default=0),
        ),
    ]
