# Generated by Django 4.1.5 on 2023-01-30 19:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_alter_productmodel_product_group_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productmodel',
            name='product_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_group', to='product.groupproductmodel'),
        ),
    ]
