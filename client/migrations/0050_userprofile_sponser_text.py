# Generated by Django 2.2 on 2020-12-24 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0049_professional_sponsers'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='sponser_text',
            field=models.TextField(default=''),
        ),
    ]
