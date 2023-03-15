# Generated by Django 4.1.5 on 2023-02-09 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0024_productmodel_weigth_netto_alter_productmodel_price'),
        ('trade', '0014_tradeitemmodel_total_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tradeitemmodel',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='_product', to='product.productmodel'),
        ),
        migrations.AlterField(
            model_name='tradeitemmodel',
            name='trade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='_trade', to='trade.trademodel'),
        ),
    ]
