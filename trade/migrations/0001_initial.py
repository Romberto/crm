# Generated by Django 4.1.5 on 2023-02-07 10:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import trade.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client', '0006_clientmodel_trend_licetin_clientmodel_trend_manez_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TradeProductBasketModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TradeStage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage_name', models.CharField(choices=[(1, 'согласование клиента'), (2, 'коммерческое предложение'), (3, 'подписание договора'), (4, 'оплата'), (5, 'исполнение договора'), (6, 'завершение сделки')], max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='TradeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('specification', models.FileField(blank=True, null=True, upload_to=trade.models.content_file_name, verbose_name='спецификация сделки')),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trade_client', to='client.clientmodel', verbose_name='клиент')),
                ('manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('stage', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trade_stage', to='trade.tradestage', verbose_name='стадия сделки')),
            ],
        ),
    ]