# Generated by Django 3.1.3 on 2021-02-13 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0014_blog_video_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='ambassadorsinfo',
            name='description',
            field=models.TextField(default=''),
        ),
    ]
