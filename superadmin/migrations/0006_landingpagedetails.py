# Generated by Django 2.2 on 2020-11-22 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0005_collaboratorsinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='LandingPageDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner', models.ImageField(upload_to='landing_page')),
                ('about_us_landing', models.ImageField(upload_to='landing_page')),
                ('about_us_text', models.TextField(default='')),
                ('main_heading', models.TextField(default='')),
                ('sub_heading', models.TextField(default='')),
                ('is_remove', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
