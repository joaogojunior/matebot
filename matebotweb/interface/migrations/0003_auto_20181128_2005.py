# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0002_auto_20181128_0319'),
    ]

    operations = [
        migrations.AddField(
            model_name='dado',
            name='data',
            field=models.DateTimeField(default=django.utils.timezone.now, blank=True),
        ),
        migrations.AddField(
            model_name='dado',
            name='filename',
            field=models.TextField(default=b''),
        ),
        migrations.AddField(
            model_name='dado',
            name='geo',
            field=models.TextField(default=b''),
        ),
        migrations.AddField(
            model_name='dado',
            name='ipaddr',
            field=models.GenericIPAddressField(default=b'0.0.0.0'),
        ),
        migrations.AddField(
            model_name='dado',
            name='numsil',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='dado',
            name='rotulo',
            field=models.TextField(default=b''),
        ),
        migrations.AddField(
            model_name='dado',
            name='silabas',
            field=models.TextField(default=b''),
        ),
        migrations.AddField(
            model_name='dado',
            name='texto',
            field=models.TextField(default=b''),
        ),
    ]
