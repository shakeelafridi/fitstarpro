# Generated by Django 2.2 on 2020-11-22 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0021_auto_20201122_1050'),
    ]

    operations = [
        migrations.RenameField(
            model_name='successstories',
            old_name='image',
            new_name='before',
        ),
        migrations.AddField(
            model_name='successstories',
            name='after',
            field=models.ImageField(null=True, upload_to='success_stories'),
        ),
    ]