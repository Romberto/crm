# Generated by Django 4.1.5 on 2023-03-02 11:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0024_remove_tradeagentitemmodel_weight'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tradeagentmodel',
            name='client',
        ),
        migrations.RemoveField(
            model_name='tradeagentmodel',
            name='trade',
        ),
        migrations.DeleteModel(
            name='TradeAgentItemModel',
        ),
        migrations.DeleteModel(
            name='TradeAgentModel',
        ),
    ]
