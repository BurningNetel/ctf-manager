# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models, migrations
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('CTFmanager', '0004_auto_20160129_2036'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='flag',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='event',
            name='creation_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2016, 1, 30, 15, 4, 15, 414861, tzinfo=utc)),
        ),
    ]
