# Generated by Django 4.1.5 on 2023-02-08 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0007_tradeitemmodel_trademodel_create_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trademodel',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
