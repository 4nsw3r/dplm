# Generated by Django 3.1.2 on 2020-11-25 14:33

import builtins
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magazine', '0006_auto_20201124_1850'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='title',
            field=models.CharField(default=0, max_length=100),
        ),
    ]
