# Generated by Django 4.2.2 on 2023-06-06 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0002_stocksalertsmodel_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='stocksalertsmodel',
            name='triggered',
            field=models.BooleanField(default=False),
        ),
    ]
