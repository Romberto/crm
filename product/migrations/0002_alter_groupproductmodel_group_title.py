# Generated by Django 4.1.5 on 2023-01-28 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupproductmodel',
            name='group_title',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]