from django.db import models

class VolleyballPlayer(models.Model):
    class Meta:
        # ordering = ['surename', 'name']
        ordering = ['FIO']
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'

    # name = models.CharField(max_length=32, verbose_name='Имя')
    # surename = models.CharField(max_length=32, verbose_name='Фамилия')
    # patronymic = models.CharField(max_length=32, blank=True, null=True, verbose_name='Отчество')
    #
    FIO = models.CharField(max_length=128, verbose_name='ФИО', default="III")
    age = models.IntegerField(verbose_name='Возраст')
    height = models.IntegerField(verbose_name='Рост')
    weight = models.IntegerField(verbose_name='Вес')
    trainer = models.BooleanField(verbose_name='Тренер', null=True, default=False)

    team = models.ForeignKey("SCSapp.VolleyballTeam", on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return f'{self.name}  {self.surename}'

    @classmethod
    def create(cls, name, surname, patronymic, age, height, weight, trainer):
        object = cls()
        object.name = name
        object.surname = surname
        object.patronymic = patronymic
        object.age = age
        object.height = height
        object.weight = weight
        object.trainer = trainer
        object.save()
        return object

    def editPlayer(self, name, surname, patronymic, age, height, weight, trainer):
        if name and len(name) > 0: self.name = name
        if surname and len(surname) > 0: self.surname = surname
        if patronymic and len(patronymic) > 0: self.patronymic = patronymic
        if age and len(age) > 0: self.age = age
        if height and len(height) > 0: self.height = height
        if weight and len(weight) > 0: self.weight = weight
        if trainer: self.trainer = trainer
        self.save()

    def getData(self):
        data = {
            'name': self.name,
            'surname': self.surname,
            'patronymic': self.patronymic,
            'age': self.age,
            'height': self.height,
            'weight': self.weight,
            'trainer': self.trainer,
        }
        return data
