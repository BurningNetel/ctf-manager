# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CTFmanager', '0004_auto_20160114_1238'),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(default='', max_length=30)),
                ('points', models.IntegerField(default=0)),
                ('event', models.ForeignKey(default=None, to='CTFmanager.Event')),
            ],
        ),
    ]
