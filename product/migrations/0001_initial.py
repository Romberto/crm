# Generated by Django 4.1.5 on 2023-01-28 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GroupProductModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_title', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'группа продукта',
                'verbose_name_plural': 'группы продуктов',
            },
        ),
    ]
