# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models, migrations
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('CTFmanager', '0006_auto_20160206_1811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 6, 19, 57, 42, 501835, tzinfo=utc), blank=True),
        ),
    ]
