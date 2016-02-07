# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('CTFmanager', '0008_auto_20160207_1312'),
    ]

    operations = [
        migrations.CreateModel(
            name='Solver',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('solve_time', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='challenge',
            name='solvers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='CTFmanager.Solver'),
        ),
        migrations.AddField(
            model_name='solver',
            name='challenge',
            field=models.ForeignKey(to='CTFmanager.Challenge'),
        ),
        migrations.AddField(
            model_name='solver',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
