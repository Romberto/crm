from django.db import models


# Create your models here.

class GroupProductModel(models.Model):
    group_title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.group_title)

    class Meta:
        verbose_name = "группа продукта"
        verbose_name_plural = "группы продуктов"


def content_file_name(instance, filename):
    return '/'.join(['doc', instance.article, filename])



class ProductModel(models.Model):
    article = models.CharField(max_length=20, verbose_name='Артикул')
    product_name = models.CharField(max_length=250, verbose_name='Наименование проукта')
    price = models.PositiveIntegerField(verbose_name="цена", null=True, blank=True)
    product_group = models.ForeignKey(GroupProductModel, on_delete=models.CASCADE, related_name='product_group', blank=True, null=True, verbose_name='Группа продукта')
    declaration = models.FileField(null=True, blank=True,
                                   upload_to=content_file_name, verbose_name='Декларация')
    protocol = models.FileField(null=True, blank=True, upload_to=content_file_name, verbose_name='Протокол')
    specification = models.FileField(null=True, blank=True, upload_to=content_file_name, verbose_name='Спецификация продукта')
    quality_certificate = models.FileField(null=True, blank=True, upload_to=content_file_name, verbose_name='Сертификат качества')

    def __str__(self):
        return str(self.product_name)

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"



