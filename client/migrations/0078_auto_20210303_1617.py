# Generated by Django 3.0.4 on 2021-03-03 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0077_auto_20210303_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='heart_modal',
            name='user',
            field=models.IntegerField(default=0),
        ),
    ]
