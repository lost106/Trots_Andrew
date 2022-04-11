from django.db import models


class Subscriber(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=126)

    def __str__(self):
        return f"Пользователь - {self.name}, {self.email}"

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'


# Create your models here.
