# Generated by Django 4.1.5 on 2023-01-28 11:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('client', '0003_alter_clientmodel_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientmodel',
            name='owner_manager',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='manager', to=settings.AUTH_USER_MODEL),
        ),
    ]