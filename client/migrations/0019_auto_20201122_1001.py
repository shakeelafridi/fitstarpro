# Generated by Django 2.2 on 2020-11-22 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0018_auto_20201122_0925'),
    ]

    operations = [
        migrations.AddField(
            model_name='fitnesscenterprofile',
            name='address',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='fitnesscenterprofile',
            name='blog_link',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='fitnesscenterprofile',
            name='facebook',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='fitnesscenterprofile',
            name='gym_used',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='fitnesscenterprofile',
            name='instagram',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='fitnesscenterprofile',
            name='phone_number',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='fitnesscenterprofile',
            name='twitter',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='fitnesscenterprofile',
            name='website',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='fitnesscenterprofile',
            name='youtube',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='fitnessmodalprofile',
            name='address',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='fitnessmodalprofile',
            name='blog_link',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='fitnessmodalprofile',
            name='facebook',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='fitnessmodalprofile',
            name='gym_used',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='fitnessmodalprofile',
            name='instagram',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='fitnessmodalprofile',
            name='phone_number',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='fitnessmodalprofile',
            name='twitter',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='fitnessmodalprofile',
            name='website',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='fitnessmodalprofile',
            name='youtube',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='fitnessprofessionalprofile',
            name='address',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='fitnessprofessionalprofile',
            name='blog_link',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='fitnessprofessionalprofile',
            name='facebook',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='fitnessprofessionalprofile',
            name='gym_used',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='fitnessprofessionalprofile',
            name='instagram',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='fitnessprofessionalprofile',
            name='phone_number',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='fitnessprofessionalprofile',
            name='twitter',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='fitnessprofessionalprofile',
            name='website',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='fitnessprofessionalprofile',
            name='youtube',
            field=models.TextField(default=''),
        ),
    ]