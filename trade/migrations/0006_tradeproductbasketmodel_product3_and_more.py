# Generated by Django 4.1.5 on 2023-02-07 12:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0022_alter_productmodel_product_type'),
        ('trade', '0005_alter_trademodel_stage_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='tradeproductbasketmodel',
            name='product3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='poroduct3', to='product.productmodel', verbose_name='продукт3'),
        ),
        migrations.AddField(
            model_name='tradeproductbasketmodel',
            name='product4',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='poroduct4', to='product.productmodel', verbose_name='продукт4'),
        ),
        migrations.AddField(
            model_name='tradeproductbasketmodel',
            name='product5',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='poroduct5', to='product.productmodel', verbose_name='продукт5'),
        ),
        migrations.AddField(
            model_name='tradeproductbasketmodel',
            name='product6',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='poroduct6', to='product.productmodel', verbose_name='продукт6'),
        ),
        migrations.AddField(
            model_name='tradeproductbasketmodel',
            name='quantity_pr3',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='количество'),
        ),
        migrations.AddField(
            model_name='tradeproductbasketmodel',
            name='quantity_pr4',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='количество'),
        ),
        migrations.AddField(
            model_name='tradeproductbasketmodel',
            name='quantity_pr5',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='количество'),
        ),
        migrations.AddField(
            model_name='tradeproductbasketmodel',
            name='quantity_pr6',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='количество'),
        ),
        migrations.AlterField(
            model_name='tradeproductbasketmodel',
            name='product2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='poroduct2', to='product.productmodel', verbose_name='продукт2'),
        ),
    ]
