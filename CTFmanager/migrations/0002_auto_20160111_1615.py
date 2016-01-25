# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models, migrations
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('CTFmanager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='date',
            field=models.DateTimeField(max_length=10, default=datetime.datetime(2016, 1, 11, 16, 15, 1, 51817, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=20, default=''),
        ),
    ]
