# Generated by Django 3.1.1 on 2021-05-19 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0086_auto_20210407_1413'),
    ]

    operations = [
        migrations.AddField(
            model_name='professional_sponsers',
            name='sponser_name',
            field=models.TextField(default=''),
        ),
    ]
