# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CTFmanager', '0006_challenge__pad_created'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='challenge',
            unique_together=set([('name', 'event')]),
        ),
    ]
