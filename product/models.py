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
    article = models.CharField(max_length=50, unique=True)
    product_name = models.CharField(max_length=250)
    product_group = models.ForeignKey(GroupProductModel, on_delete=models.CASCADE, related_name='product_group')
    declaration = models.FileField(null=True, blank=True,
                                   upload_to=content_file_name)
    protocol = models.FileField(null=True, blank=True, upload_to=content_file_name)
    specification = models.FileField(null=True, blank=True, upload_to=content_file_name)
    quality_certificate = models.FileField(null=True, blank=True, upload_to=content_file_name)

    def __str__(self):
        return str(self.product_name)

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"

