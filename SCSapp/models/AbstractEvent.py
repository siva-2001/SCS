from django.db import models


class AbstractEvent(models.Model):
    class TypeChoices(models.TextChoices):
        INTERNAL = 'INT', 'Внутреннее'
        INTERCOLLEGIATE = 'IC', 'Межвузовское'

    class StatusChoices(models.TextChoices):
        ANNOUNSED = "AN", 'Анонсированное'
        CURRENT = 'CR', 'Текущее'
        PAST = 'P', 'Прошедшее'

    status = models.CharField(
        max_length=2,
        choices = StatusChoices.choices,
        default = StatusChoices.ANNOUNSED,
        verbose_name = 'Статус',
    )

    type = models.CharField(
        max_length=3,
        choices = TypeChoices.choices,
        default = TypeChoices.INTERCOLLEGIATE,
    )