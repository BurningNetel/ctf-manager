# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models, migrations
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.SlugField(default='', max_length=30)),
                ('points', models.IntegerField(default=0)),
                ('_pad_created', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('name', models.SlugField(primary_key=True, default='', max_length=20, serialize=False)),
                ('date', models.DateTimeField(default='')),
                ('description', models.CharField(default='No Description provided.', blank=True, max_length=5000)),
                ('location', models.SlugField(default='', blank=True, max_length=100)),
                ('username', models.CharField(default='', blank=True, max_length=200)),
                ('password', models.CharField(default='', blank=True, max_length=200)),
                ('url', models.CharField(default='', blank=True, max_length=200)),
                ('end_date', models.DateTimeField(null=True, blank=True)),
                ('creation_date', models.DateTimeField(default=datetime.datetime(2016, 1, 26, 12, 2, 12, 346717, tzinfo=utc), blank=True)),
                ('created_by', models.SlugField(default='Anonymous', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='challenge',
            name='event',
            field=models.ForeignKey(default=None, to='CTFmanager.Event'),
        ),
        migrations.AlterUniqueTogether(
            name='challenge',
            unique_together=set([('name', 'event')]),
        ),
    ]
