# Generated by Django 4.1.5 on 2023-02-15 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0026_alter_productpackagingmodel_quantity_element_in'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productpackagingmodel',
            name='quantity_element_in',
            field=models.PositiveIntegerField(default=1, verbose_name='количество единиц в упакове'),
        ),
    ]
