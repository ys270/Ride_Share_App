# Generated by Django 3.0.2 on 2020-02-02 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_users_my_rides'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rides',
            name='driver',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
