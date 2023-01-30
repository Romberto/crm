# Generated by Django 4.1.5 on 2023-01-25 13:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('face_contact', models.CharField(blank=True, max_length=200, null=True)),
                ('phone', models.CharField(max_length=20)),
                ('phone2', models.CharField(blank=True, max_length=20, null=True)),
                ('phone3', models.CharField(blank=True, max_length=20, null=True)),
                ('mail', models.EmailField(blank=True, max_length=150, null=True)),
                ('fact_address', models.CharField(blank=True, max_length=200, null=True)),
                ('jurist_address', models.CharField(blank=True, max_length=200, null=True)),
                ('inn', models.CharField(blank=True, max_length=12, null=True)),
                ('site', models.CharField(blank=True, max_length=50, null=True)),
                ('agreement', models.BooleanField(default=False)),
                ('activity', models.TextField(blank=True, null=True)),
                ('owner_manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'контакт',
                'verbose_name_plural': 'контакты',
            },
        ),
    ]
