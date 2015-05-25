# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0004_list'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='new_field',
            new_name='list',
        ),
    ]
