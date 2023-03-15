# Generated by Django 4.1.5 on 2023-03-02 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0006_clientmodel_trend_licetin_clientmodel_trend_manez_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientmodel',
            name='role',
            field=models.CharField(choices=[('P', 'покупатель'), ('S', 'поставщик')], default='P', max_length=50),
        ),
    ]
