# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20150527_1900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='length',
            field=models.CharField(max_length=100),
        ),
    ]
