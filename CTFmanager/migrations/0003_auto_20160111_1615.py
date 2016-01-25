# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.utils.timezone
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CTFmanager', '0002_auto_20160111_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
