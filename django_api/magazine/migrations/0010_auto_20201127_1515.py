# Generated by Django 3.1.2 on 2020-11-27 12:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('magazine', '0009_productreviews_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productreviews',
            name='review',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='magazine.product'),
        ),
    ]
