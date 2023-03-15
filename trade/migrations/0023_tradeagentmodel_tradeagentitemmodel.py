# Generated by Django 4.1.5 on 2023-03-01 11:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0006_clientmodel_trend_licetin_clientmodel_trend_manez_and_more'),
        ('trade', '0022_trademodel_logistic'),
    ]

    operations = [
        migrations.CreateModel(
            name='TradeAgentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('endDate', models.DateField(verbose_name='дата поставки')),
                ('full_price', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='полная стоимость')),
                ('full_weight', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='общий вес')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.clientmodel', verbose_name='поставщик')),
                ('trade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trade.trademodel')),
            ],
        ),
        migrations.CreateModel(
            name='TradeAgentItemModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(verbose_name='количество')),
                ('product', models.CharField(max_length=255, verbose_name='продукт')),
                ('price', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='цена')),
                ('weight', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='вес')),
                ('tradeAgent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trade.tradeagentmodel')),
            ],
        ),
    ]
