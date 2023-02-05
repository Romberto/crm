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
    product_group = models.ForeignKey(GroupProductModel, on_delete=models.CASCADE, related_name='product_group',
                                      blank=True, null=True, verbose_name='Группа продукта')
    declaration = models.FileField(null=True, blank=True,
                                   upload_to=content_file_name, verbose_name='Декларация')
    protocol = models.FileField(null=True, blank=True, upload_to=content_file_name, verbose_name='Протокол')
    specification = models.FileField(null=True, blank=True, upload_to=content_file_name,
                                     verbose_name='Спецификация продукта')
    quality_certificate = models.FileField(null=True, blank=True, upload_to=content_file_name,
                                           verbose_name='Сертификат качества')

    def __str__(self):
        return str(self.product_name)

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"


class ProductPackagingModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='product')
    packing = models.CharField(max_length=255, default='ящик из гофрированного картона',
                               verbose_name='упаковка')  # упаковка
    netto = models.DecimalField( max_digits=8,decimal_places = 2,
        verbose_name='нетто масса товара в одной единице упаковки')  # нетто масса товара в одной единице упаковки
    brutto = models.DecimalField(max_digits=8,decimal_places = 2,
        verbose_name='брутто масса одной коробки с товаром')  # брутто масса одной коробки с товаром
    quantity_box = models.PositiveIntegerField(
        verbose_name='количество коробок на поддоне')  # количество коробок на поддоне
    pallet_weight_netto = models.DecimalField(max_digits=8,decimal_places = 2, verbose_name='масса поддона нетто', blank=True, null=True)  # масса поддона нетто
    pallet_weight_brutto = models.DecimalField(max_digits=8,decimal_places = 2,verbose_name='масса поддона брутто', blank=True, null=True)  # масса поддона брутто


    def netto_sum(self):
        return self.quantity_box * self.netto

    def brutto_sum(self):
        return  self.quantity_box * self.brutto

    def save(self, *args, **kwargs):
        self.pallet_weight_netto = self.netto_sum()
        self.pallet_weight_brutto = self.brutto_sum()
        super(ProductPackagingModel, self).save(*args, **kwargs)

    def __str__(self):
        return f"Упаковка : {self.product}"


    class Meta:
        verbose_name = "Спецификация упаковки"
        verbose_name_plural = "Спецификация упаковки"
