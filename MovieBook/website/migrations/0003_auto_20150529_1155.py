# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20150529_1008'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='actors',
            field=models.CharField(default='none', max_length=300),
        ),
        migrations.AddField(
            model_name='movie',
            name='genres',
            field=models.CharField(default=datetime.datetime(2015, 5, 29, 11, 55, 45, 628625, tzinfo=utc), max_length=300),
            preserve_default=False,
        ),
    ]
