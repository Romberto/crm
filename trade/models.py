import decimal

from django.contrib.auth.models import User
from django.db import models

from django.utils.timezone import now

from client.models import ClientModel
from product.models import ProductModel


def content_file_name(instance, filename):
    return '/'.join(['trade_doc_spe', str(instance.client.id), filename])


class TradeModel(models.Model):
    STAGES = (
        ('1', 'согласование клиента'),
        ('2', 'коммерческое предложение'),
        ('3', 'подписание договора'),
        ('4', 'оплата'),
        ('5', 'исполнение договора'),
        ('6', 'завершение сделки')
    )
    create_date = models.DateField(auto_now_add=True)
    stage_name = models.CharField(choices=STAGES, max_length=30, default=1, verbose_name='стадия сделки')
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='менеджер',
                                related_name="manager")
    is_active = models.BooleanField(default=True)
    client = models.ForeignKey(ClientModel, on_delete=models.SET_NULL, verbose_name='клиент',
                               related_name='trade_client', null=True)
    application_supplier = models.ForeignKey('TradeAgent', on_delete=models.CASCADE, related_name='supplier', verbose_name='заявка поставщикам', null=True)
    specification = models.FileField(upload_to=content_file_name, verbose_name="спецификация сделки", null=True,
                                     blank=True)
    full_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='полная стоимость', default=0)
    full_weight = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='общий вес', default=0)
    compare = models.BooleanField(default=False, verbose_name='согласование цены и количества')
    logistic = models.DecimalField(default=0, max_digits=12, decimal_places=2, verbose_name='логистика')

    def __str__(self):
        return f"{self.create_date} {self.client}"

    def save(self, *args, **kwargs):
        self.full_price = self.get_full_price()
        self.full_weight = self.get_full_weight()
        super(TradeModel, self).save(*args, **kwargs)

    def get_full_price(self):
        trade_item_list = TradeItemModel.objects.filter(trade=self)
        if trade_item_list:
            return sum([
                (trade_item.total())
                for trade_item in trade_item_list
            ])
        else:
            return 0

    def get_full_weight(self):
        return sum([
            trade_item.total_weight()
            for trade_item in TradeItemModel.objects.filter(trade=self)
        ])

    class Meta:
        verbose_name = "Сделка"
        verbose_name_plural = "Сделки"


class TradeItemModel(models.Model):
    trade = models.ForeignKey(TradeModel, on_delete=models.CASCADE, null=True, blank=True, related_name='_trade')
    product = models.ForeignKey(ProductModel, on_delete=models.SET_NULL, related_name='_product', null=True)
    count = models.PositiveIntegerField(default=0)

    def total(self):
        if self.product.price == None:
            return 0
        else:
            return self.count * self.product.price

    def total_weight(self):
        result = self.count * float(self.product.weigth_netto)
        D = decimal.Decimal
        return D(result).quantize(D("1.00"), decimal.ROUND_CEILING)

    def __str__(self):
        return f'{self.product}'

    class Meta:
        verbose_name = 'товар для сделки'
        verbose_name_plural = 'товары для сделки'


class TradeAgent(models.Model):
    trade = models.ForeignKey(TradeModel, on_delete=models.CASCADE, verbose_name="сделка")
    full_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="сумма", default=0)
    full_weight = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='общий вес', default=0)
    def save(self, *args, **kwargs):

        self.full_price = self.get_full_price()
        self.full_weight = self.get_full_weight()
        super(TradeAgent, self).save(*args, **kwargs)

    def get_full_price(self):
        trade_item_list = TradeAgentItem.objects.filter(trade_agent=self)
        if trade_item_list:
            return sum([
                (trade_item.total_price())
                for trade_item in trade_item_list
            ])
        else:
            return 0

    def get_full_weight(self):
        return sum([
            trade_item.rotal_weight()
            for trade_item in TradeAgentItem.objects.filter(trade_agent=self)
        ])

class TradeAgentItem(models.Model):
    trade_agent = models.ForeignKey(TradeAgent, on_delete=models.CASCADE, verbose_name="заявка", null=True, related_name='trade_agent')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, verbose_name="продукт", related_name='product')
    count = models.PositiveIntegerField(default=0, verbose_name="количество")
    date_delivery = models.DateField(verbose_name="дата поставки")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="цена поставщика")

    def total_price(self):
        result = self.count * float(self.price)
        D = decimal.Decimal
        return D(result).quantize(D("1.00"), decimal.ROUND_CEILING)

    def rotal_weight(self):
        result = self.count * float(self.product.weigth_netto)
        D = decimal.Decimal
        return D(result).quantize(D("1.00"), decimal.ROUND_CEILING)