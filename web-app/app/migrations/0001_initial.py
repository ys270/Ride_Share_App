# Generated by Django 3.0.2 on 2020-01-31 03:58

import django.contrib.postgres.fields
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rides',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=200)),
                ('owner_party_size', models.IntegerField(default=0)),
                ('driver', models.CharField(max_length=200)),
                ('car_seat', models.IntegerField(default=0)),
                ('sharer', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=200, null=True), blank=True, null=True, size=None)),
                ('sharer_party_size', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(default=0), blank=True, null=True, size=None)),
                ('is_sharable', models.BooleanField(default=True)),
                ('remaining_size', models.IntegerField(default=0)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('is_complete', models.BooleanField(default=False)),
                ('destination', models.CharField(default='destination', max_length=200)),
                ('arrival_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('is_loggedin', models.BooleanField(default=False)),
                ('is_driver', models.BooleanField(default=False)),
                ('is_owner', models.BooleanField(default=True)),
                ('is_sharer', models.BooleanField(default=True)),
                ('car_size', models.IntegerField(default=0)),
                ('plate_id', models.CharField(default='a', max_length=200)),
                ('my_rides', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(default=0), blank=True, null=True, size=None)),
            ],
        ),
    ]
