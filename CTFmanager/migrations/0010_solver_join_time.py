# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CTFmanager', '0009_solvers_m2m'),
    ]

    operations = [
        migrations.AddField(
            model_name='solver',
            name='join_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
