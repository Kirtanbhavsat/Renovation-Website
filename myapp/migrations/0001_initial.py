# Generated by Django 5.0.2 on 2024-02-19 09:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('dp', models.ImageField(upload_to='photos')),
                ('gender', models.CharField(max_length=6)),
                ('email', models.EmailField(max_length=254)),
                ('phone_no', models.BigIntegerField()),
                ('dob', models.DateField()),
                ('address', models.TextField()),
                ('r_type', models.CharField(max_length=10, null=True)),
                ('password', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sname', models.CharField(max_length=40)),
                ('sprice', models.IntegerField()),
                ('sdesc', models.TextField()),
                ('simg', models.ImageField(upload_to='photos')),
                ('email_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.registration')),
            ],
        ),
    ]
