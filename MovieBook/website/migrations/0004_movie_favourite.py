# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_auto_20150528_1011'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='favourite',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
