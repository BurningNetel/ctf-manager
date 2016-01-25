# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CTFmanager', '0003_auto_20160111_1615'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='id',
        ),
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateTimeField(default=''),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(primary_key=True, default='', max_length=20, serialize=False),
        ),
    ]
