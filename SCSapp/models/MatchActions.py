# from django.db import models
#
# class MatchAction(models.Model):
#     class Meta:
#         verbose_name = 'Событие'
#         verbose_name_plural = 'События'
#
#     eventType = models.CharField(
#         max_length=20,
#         verbose_name='Тип события'
#     )
#
#     team = models.ForeignKey("SCSapp.Team", on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Команда')
# #     player = models.ForeignKey("SCSapp.Player", verbose_name="Игрок", on_delete=models.CASCADE, null=True, blank=True)
#     eventTime = models.TimeField(auto_now_add=True, verbose_name="Время события")
#     match = models.ForeignKey('SCSapp.AbstractMatch', on_delete=models.CASCADE, verbose_name="Матч")
#
#     def __str__(self):
#         participantName = self.team.participant.name if self.team else "NoTeam"
#         return f"{self.eventType}, {participantName} in {self.eventTime}"
#
#     def getActionMessage(self):
#         return {
#             "message_type" : "action_info",
#             "data" : {
#                 "id" : self.id,
#                 "signal" : self.eventType,
#                 "datetime" : str(self.eventTime),
#                 "team" : (self.team.participant.name if self.team else None),
#             }
#         }
