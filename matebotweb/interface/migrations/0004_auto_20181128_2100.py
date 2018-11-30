# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0003_auto_20181128_2005'),
    ]

    operations = [
        migrations.AddField(
            model_name='dado',
            name='idade',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='dado',
            name='sexo',
            field=models.TextField(default=b''),
        ),
    ]
