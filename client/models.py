from django.contrib.auth.models import User
from django.db import models


class ClientModel(models.Model):
    owner_manager = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)# менеджер которому принадлежит контакт
    name = models.CharField(max_length=128)  # наименование клиента
    face_contact = models.CharField(max_length=200, null=True, blank=True)  # контанное лицо
    phone = models.CharField(max_length=20)  # телефон1
    phone2 = models.CharField(max_length=20, null=True, blank=True)  # телефон2
    phone3 = models.CharField(max_length=20, null=True, blank=True)  # телефон3
    mail = models.EmailField(max_length=150, null=True, blank=True)  # электронная почта
    fact_address = models.TextField(blank=True, null=True)  # фактический адрес
    jurist_address = models.TextField(blank=True, null=True)  # юридический  адрес
    inn = models.CharField(max_length=12, blank=True, null=True)  # инн
    site = models.CharField(max_length=50, blank=True, null=True)  # сайт
    agreement = models.BooleanField(default=False)  # соглосование
    activity = models.TextField(blank=True, null=True)  # примечания (комментарии)


    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"

    def __str__(self):
        return str(self.name)
