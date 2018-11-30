# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0005_auto_20181129_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='dado',
            name='polarity',
            field=models.FloatField(default=0.0),
        ),
    ]
