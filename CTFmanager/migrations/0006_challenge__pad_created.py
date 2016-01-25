# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CTFmanager', '0005_challenge'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='_pad_created',
            field=models.BooleanField(default=False),
        ),
    ]
