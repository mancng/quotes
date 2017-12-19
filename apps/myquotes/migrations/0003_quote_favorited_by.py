# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-19 20:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myquotes', '0002_quote'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='favorited_by',
            field=models.ManyToManyField(related_name='fav_quotes', to='myquotes.User'),
        ),
    ]