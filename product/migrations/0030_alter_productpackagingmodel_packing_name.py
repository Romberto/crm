# Generated by Django 4.1.5 on 2023-02-16 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0029_alter_productmodel_weigth_netto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productpackagingmodel',
            name='packing_name',
            field=models.CharField(choices=[('AJ', 'ящик из гофрированного картона'), ('K', 'канистра'), ('P', 'пластиковое ведро с крышкой')], default='AJ', max_length=200, verbose_name='упаковка'),
        ),
    ]
