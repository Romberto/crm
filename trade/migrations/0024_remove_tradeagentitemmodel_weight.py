# Generated by Django 4.1.5 on 2023-03-01 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0023_tradeagentmodel_tradeagentitemmodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tradeagentitemmodel',
            name='weight',
        ),
    ]