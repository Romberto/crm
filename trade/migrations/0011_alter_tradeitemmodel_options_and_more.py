# Generated by Django 4.1.5 on 2023-02-09 07:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('trade', '0010_alter_trademodel_create_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tradeitemmodel',
            options={'verbose_name': 'товар для сделки', 'verbose_name_plural': 'товары для сделки'},
        ),
        migrations.AlterField(
            model_name='trademodel',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='manager', to=settings.AUTH_USER_MODEL, verbose_name='менеджер'),
        ),
        migrations.AlterField(
            model_name='trademodel',
            name='stage_name',
            field=models.CharField(choices=[('1', 'согласование клиента'), ('2', 'коммерческое предложение'), ('3', 'подписание договора'), ('4', 'оплата'), ('5', 'исполнение договора'), ('6', 'завершение сделки')], default=1, max_length=30, verbose_name='стадия сделки'),
        ),
    ]