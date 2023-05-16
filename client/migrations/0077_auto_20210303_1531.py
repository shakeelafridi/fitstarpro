# Generated by Django 3.0.4 on 2021-03-03 10:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0076_auto_20210303_1527'),
    ]

    operations = [
        migrations.CreateModel(
            name='Heart_Modal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hearts_counter', models.IntegerField(default=0)),
                ('user_session', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.UserProfile')),
            ],
        ),
        migrations.DeleteModel(
            name='Heart',
        ),
    ]