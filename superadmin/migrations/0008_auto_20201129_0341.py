# Generated by Django 2.2 on 2020-11-29 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0007_landingpagedetails_banner_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='ambassadorsinfo',
            name='facebook',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='ambassadorsinfo',
            name='instagram',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='ambassadorsinfo',
            name='twitter',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='ambassadorsinfo',
            name='youtube',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='collaboratorsinfo',
            name='facebook',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='collaboratorsinfo',
            name='instagram',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='collaboratorsinfo',
            name='sub_title',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='collaboratorsinfo',
            name='title',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='collaboratorsinfo',
            name='twitter',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='collaboratorsinfo',
            name='youtube',
            field=models.TextField(default=''),
        ),
    ]
