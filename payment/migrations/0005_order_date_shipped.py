# Generated by Django 5.2.3 on 2025-07-08 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_order_shipped'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='date_shipped',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
