# Generated by Django 3.0.4 on 2021-03-03 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0069_auto_20210303_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='heartmodel',
            name='user_id',
            field=models.IntegerField(default=0, max_length=10),
        ),
        migrations.AlterField(
            model_name='heartmodel',
            name='user_session_id',
            field=models.IntegerField(default=0, max_length=20),
        ),
    ]
