# Generated by Django 4.1.5 on 2023-02-05 12:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_alter_productpackagingmodel_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productmodel',
            name='packing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='spe_packing', to='product.productpackagingmodel', verbose_name='спецификация упаковки'),
        ),
    ]