# Generated by Django 4.1.5 on 2023-02-05 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0018_remove_productpackagingmodel_packing_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productpackagingmodel',
            name='packing_name',
            field=models.CharField(blank=True, default='ящик из гофрированного картона', max_length=200, null=True, verbose_name='упаковка'),
        ),
    ]
