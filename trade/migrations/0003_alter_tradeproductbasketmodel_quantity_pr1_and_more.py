# Generated by Django 4.1.5 on 2023-02-07 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0002_tradeproductbasketmodel_full_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tradeproductbasketmodel',
            name='quantity_pr1',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='количество'),
        ),
        migrations.AlterField(
            model_name='tradeproductbasketmodel',
            name='quantity_pr2',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='количество'),
        ),
    ]
