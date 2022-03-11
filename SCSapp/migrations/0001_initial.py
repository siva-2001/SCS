# Generated by Django 4.0.3 on 2022-03-09 11:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Announsed', 'Announsed'), ('Current', 'Current'), ('Past', 'Past')], max_length=12)),
                ('name', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('discription', models.TextField(blank=True, verbose_name='Описание')),
                ('lastTimeForApplications', models.DateTimeField(verbose_name='Заявки на участие принимаются до')),
                ('competitionEndDateTime', models.DateTimeField(blank=True, null=True, verbose_name='Соревнование завершилось')),
                ('organizerName', models.CharField(max_length=32, null=True)),
                ('theNumberOfTeamsRequiredToStartTheCompetition', models.IntegerField(default=4)),
                ('protocol', models.FileField(blank=True, null=True, upload_to='competition_protocols', verbose_name='Протокол')),
                ('organizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Организатор')),
            ],
            options={
                'verbose_name': 'Соревнование',
                'verbose_name_plural': 'Соревнования',
                'permissions': [('control_competition', 'the user must be the judge')],
            },
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('matchDateTime', models.DateTimeField(default=None, null=True)),
                ('firstTeamScore', models.IntegerField(default=0)),
                ('secondTeamScore', models.IntegerField(default=0)),
                ('place', models.CharField(blank=True, max_length=128, null=True)),
                ('status_isCompleted', models.BooleanField(default=False)),
                ('protocol', models.FileField(blank=True, null=True, upload_to='match_protocols')),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SCSapp.competition')),
            ],
            options={
                'verbose_name': 'Матч',
                'verbose_name_plural': 'Матчи',
            },
        ),
        migrations.CreateModel(
            name='VolleyballTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Название')),
                ('registratedTime', models.DateTimeField(auto_now_add=True, verbose_name='Время регистрации')),
                ('discription', models.TextField(blank=True, verbose_name='Описание')),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SCSapp.competition', verbose_name='Соревнования')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Команда',
                'verbose_name_plural': 'Команды',
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='Имя')),
                ('surename', models.CharField(max_length=32, verbose_name='Фамилия')),
                ('patronymic', models.CharField(blank=True, max_length=32, null=True, verbose_name='Отчество')),
                ('age', models.IntegerField(verbose_name='Возраст')),
                ('team', models.ManyToManyField(blank=True, to='SCSapp.volleyballteam')),
            ],
            options={
                'verbose_name': 'Игрок',
                'verbose_name_plural': 'Игроки',
                'ordering': ['surename', 'name'],
            },
        ),
        migrations.CreateModel(
            name='MatchEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eventType', models.CharField(choices=[('Goal', 'Goal'), ('Player replacement', 'Player replacement'), ('Part', 'Part'), ('Interval', 'Interval'), ('Game over', 'Game over')], max_length=20)),
                ('Team', models.IntegerField(blank=True, choices=[(1, 'first'), (2, 'second')], null=True, verbose_name='Команда')),
                ('EventTime', models.TimeField(auto_now_add=True, verbose_name='Время события')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SCSapp.match', verbose_name='Матч')),
            ],
            options={
                'verbose_name': 'Событие',
                'verbose_name_plural': 'События',
            },
        ),
        migrations.AddField(
            model_name='match',
            name='firstTeam',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='first_team', to='SCSapp.volleyballteam'),
        ),
        migrations.AddField(
            model_name='match',
            name='nextMatch',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='SCSapp.match'),
        ),
        migrations.AddField(
            model_name='match',
            name='secondTeam',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='second_team', to='SCSapp.volleyballteam'),
        ),
    ]
