from SCSapp.models.Competition import Competition
from SCSapp.models.User import User
from django.shortcuts import redirect

def CreateTestDataView(request):
    competition_1 = Competition.objects.create(
        name = "Межфакультетские соревнования. Кубок по волейболу ТУСУР", 
        description = "Лучшие соревнования за последние 10, а то и 15 лет!",
        sportType = Competition.SportTypeChoices.VOLLEYBALL,
        type = Competition.TypeChoices.INTERCOLLEGIATE, 
        organizer = User.objects.get(username="admin")
    )

    competition_2 = Competition.objects.create(
        name = "Межфакультетские соревнования. Кубок по футболу ТУСУР", 
        description = "Вторые лучшие соревнования за последние 10, а то и 15 лет!",
        sportType = Competition.SportTypeChoices.FOOTBALL,
        type = Competition.TypeChoices.INTERNAL, 
        organizer = User.objects.get(username="admin")
    )

    competition_3 = Competition.objects.create(
        name = "Межвузовские соревнования. Кубок по футболу ТУСУР-ТПУ-ТГУ", 
        description = "Лучшие соревнования за последние 20, а то и 50 лет!",
        sportType = Competition.SportTypeChoices.FOOTBALL,
        type = Competition.TypeChoices.INTERCOLLEGIATE, 
        organizer = User.objects.get(username="admin")
    )

    competition_4 = Competition.objects.create(
        name = "Пупок по полу ТУСУР", 
        description = "Худшие соревнование, без комментариев...",
        sportType = Competition.SportTypeChoices.VOLLEYBALL,
        type = Competition.TypeChoices.INTERCOLLEGIATE, 
        organizer = User.objects.get(username="admin")
    )
    competition_1.status = Competition.StatusChoices.PAST
    competition_3.status = Competition.StatusChoices.CURRENT
    competition_1.save()
    competition_3.save()

    return redirect('homePage')
