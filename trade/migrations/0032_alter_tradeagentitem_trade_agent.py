# Generated by Django 4.1.5 on 2023-03-06 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0031_alter_tradeagentitem_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tradeagentitem',
            name='trade_agent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trade_agent', to='trade.tradeagent', verbose_name='заявка'),
        ),
    ]
