# Generated by Django 2.2 on 2020-11-17 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='sign_up_role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sign_up_role', to='client.UserRoles'),
        ),
    ]
