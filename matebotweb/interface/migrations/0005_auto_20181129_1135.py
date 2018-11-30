# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0004_auto_20181128_2100'),
    ]

    operations = [
        migrations.AddField(
            model_name='dado',
            name='latitude',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='dado',
            name='longitude',
            field=models.FloatField(default=0.0),
        ),
    ]
