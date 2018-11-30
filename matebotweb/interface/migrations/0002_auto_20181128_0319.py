# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dado',
            name='normal',
        ),
        migrations.AddField(
            model_name='dado',
            name='tamanho',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='dado',
            name='vel',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='dado',
            name='id',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
    ]
