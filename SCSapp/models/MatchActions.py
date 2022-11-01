from django.db import models



class MatchAction(models.Model):
    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    class EventTypeChoices(models.TextChoices):
        GOAL = 'Goal'
        PLAYER_REPLACEMENT = 'Player replacement'
        PART = 'Part'
        INTERVAL = 'Interval'
        END = 'Game over'
        NONE = 0
        FIRST = 1
        SECOND = 2

    eventType = models.CharField(
        max_length=20,
        choices=EventTypeChoices.choices,
        verbose_name='Тип события'
    )

    team = models.ForeignKey("SCSapp.Team", on_delete=models.SET_NULL, null=True, verbose_name='Команда')
    player = models.ForeignKey("SCSapp.Player", verbose_name="Игрок", on_delete=models.CASCADE, null=True, blank=True)
    eventTime = models.TimeField(auto_now_add=True, verbose_name="Время события")
    match = models.ForeignKey('SCSapp.AbstractMatch', on_delete=models.CASCADE, verbose_name="Матч")

    def __str__(self):
        return f"{self.eventType}, team {self.Team} in {self.EventTime}"

