# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('overview', models.CharField(max_length=1000)),
                ('rating', models.FloatField()),
                ('length', models.TimeField()),
                ('release_date', models.DateField()),
                ('status', models.CharField(max_length=50)),
                ('original_title', models.CharField(max_length=200)),
                ('cover', models.CharField(max_length=300)),
                ('trailer', models.CharField(max_length=300)),
                ('actor_id', models.ManyToManyField(to='website.Actor')),
                ('genre_id', models.ManyToManyField(to='website.Genre')),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
