# Generated by Django 4.0.3 on 2022-03-10 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DataBase', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Param',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=256)),
                ('value', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.CharField(max_length=64, unique=True)),
                ('uid', models.CharField(max_length=64, unique=True)),
                ('title', models.CharField(max_length=256)),
                ('intro', models.CharField(max_length=256)),
                ('region', models.CharField(max_length=256)),
                ('background_image', models.FilePathField(max_length=256)),
                ('total_num', models.IntegerField()),
                ('current_num', models.IntegerField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('details', models.TextField()),
                ('price', models.FloatField()),
                ('donate_history', models.TextField()),
            ],
        ),
    ]
