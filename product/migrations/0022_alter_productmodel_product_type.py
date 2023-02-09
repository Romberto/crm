# Generated by Django 4.1.5 on 2023-02-06 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0021_productmodel_product_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productmodel',
            name='product_type',
            field=models.CharField(choices=[('T', 'продукт тарированный'), ('W', 'продукт весовой'), ('S', 'продукт сыпучий'), ('N', 'тип тары не указан не указан')], default='N', max_length=20, verbose_name='тип тары'),
        ),
    ]