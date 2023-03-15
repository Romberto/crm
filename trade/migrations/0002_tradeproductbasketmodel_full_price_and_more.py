# Generated by Django 4.1.5 on 2023-02-07 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0022_alter_productmodel_product_type'),
        ('trade', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tradeproductbasketmodel',
            name='full_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='полная стоимость'),
        ),
        migrations.AddField(
            model_name='tradeproductbasketmodel',
            name='product1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.productmodel', verbose_name='продукт1'),
        ),
        migrations.AddField(
            model_name='tradeproductbasketmodel',
            name='product2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='poroduct2', to='product.productmodel', verbose_name='продукт2'),
        ),
        migrations.AddField(
            model_name='tradeproductbasketmodel',
            name='quantity_pr1',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=8, verbose_name='количество'),
        ),
        migrations.AddField(
            model_name='tradeproductbasketmodel',
            name='quantity_pr2',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=8, verbose_name='количество'),
        ),
        migrations.AddField(
            model_name='tradeproductbasketmodel',
            name='trade',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='trade.trademodel'),
        ),
    ]