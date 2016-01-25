# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CTFmanager', '0008_auto_20160125_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='name',
            field=models.SlugField(default='', max_length=30),
        ),
    ]
