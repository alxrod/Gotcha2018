# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-12 05:27
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('apiApp', '0015_auto_20181112_0405'),
    ]

    operations = [
        migrations.RenameField(
            model_name='targetrel',
            old_name='longtitude',
            new_name='longitude',
        ),
        migrations.AlterField(
            model_name='player',
            name='timeTagged',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 12, 5, 27, 43, 455539, tzinfo=utc), verbose_name='date tagged'),
        ),
    ]
