# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0002_item_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='new_field',
            field=models.TextField(default=''),
        ),
    ]
