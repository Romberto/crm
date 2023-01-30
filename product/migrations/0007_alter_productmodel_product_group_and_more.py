# Generated by Django 4.1.5 on 2023-01-30 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_rename_declination_productmodel_declaration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productmodel',
            name='product_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.groupproductmodel'),
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='product_name',
            field=models.CharField(max_length=250),
        ),
    ]