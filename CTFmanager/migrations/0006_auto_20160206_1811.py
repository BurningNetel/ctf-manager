# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models, migrations
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('CTFmanager', '0005_auto_20160130_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 6, 18, 11, 30, 280825, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(default='', max_length=5000, blank=True),
        ),
    ]
