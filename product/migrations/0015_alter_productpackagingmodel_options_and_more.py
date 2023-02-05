# Generated by Django 4.1.5 on 2023-02-05 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_alter_productpackagingmodel_brutto_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productpackagingmodel',
            options={'verbose_name': 'Спецификация упаковки', 'verbose_name_plural': 'Спецификация упаковки'},
        ),
        migrations.AlterField(
            model_name='productpackagingmodel',
            name='netto',
            field=models.DecimalField(decimal_places=2, max_digits=8, verbose_name='нетто масса товара в одной коробке'),
        ),
        migrations.AlterField(
            model_name='productpackagingmodel',
            name='product',
            field=models.CharField(max_length=255),
        ),
    ]