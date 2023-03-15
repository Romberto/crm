# Generated by Django 4.1.5 on 2023-02-09 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0023_productpackagingmodel_quantity_element_in'),
    ]

    operations = [
        migrations.AddField(
            model_name='productmodel',
            name='weigth_netto',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='вес нетто'),
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='цена'),
        ),
    ]
