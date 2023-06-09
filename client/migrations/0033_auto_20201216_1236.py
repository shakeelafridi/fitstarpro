# Generated by Django 2.2 on 2020-12-16 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0032_auto_20201213_2041'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=150)),
            ],
        ),
        migrations.AddField(
            model_name='fitnesscenterprofile',
            name='comment',
            field=models.ManyToManyField(to='client.Comments'),
        ),
        migrations.AddField(
            model_name='fitnessmodalprofile',
            name='comment',
            field=models.ManyToManyField(to='client.Comments'),
        ),
        migrations.AddField(
            model_name='fitnessprofessionalprofile',
            name='comment',
            field=models.ManyToManyField(to='client.Comments'),
        ),
    ]
