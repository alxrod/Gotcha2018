# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-12 10:14
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('apiApp', '0017_auto_20181112_0532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='timeTagged',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 12, 10, 14, 35, 408080, tzinfo=utc), verbose_name='date tagged'),
        ),
    ]