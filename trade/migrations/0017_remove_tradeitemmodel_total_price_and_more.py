# Generated by Django 4.1.5 on 2023-02-09 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0016_alter_tradeitemmodel_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tradeitemmodel',
            name='total_price',
        ),
        migrations.RemoveField(
            model_name='tradeitemmodel',
            name='total_weight_item',
        ),
    ]
