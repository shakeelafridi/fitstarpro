# Generated by Django 3.1.3 on 2021-02-24 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0062_auto_20210224_1032'),
    ]

    operations = [
        migrations.AddField(
            model_name='fitnessprofessionalprofile',
            name='profession',
            field=models.TextField(default=''),
        ),
    ]