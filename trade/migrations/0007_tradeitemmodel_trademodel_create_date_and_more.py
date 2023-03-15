# Generated by Django 4.1.5 on 2023-02-08 06:09

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0022_alter_productmodel_product_type'),
        ('trade', '0006_tradeproductbasketmodel_product3_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TradeItemModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.productmodel')),
            ],
        ),
        migrations.AddField(
            model_name='trademodel',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 8, 6, 9, 0, 223365, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AddField(
            model_name='trademodel',
            name='full_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='полная стоимость'),
        ),
        migrations.DeleteModel(
            name='TradeProductBasketModel',
        ),
        migrations.AddField(
            model_name='tradeitemmodel',
            name='trade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='trade.trademodel'),
        ),
    ]