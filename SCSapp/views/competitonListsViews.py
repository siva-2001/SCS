import json

from django.shortcuts import render
from SCSapp.models.Competition import Competition
from SCSapp.models.Olympics import Olympics
from django.core.paginator import Paginator
from SportCompetitionService import settings
from django.core.serializers import serialize
def homePageView(request):
    listOfCurrentEvents = list()
    listOfAnnouncedEvents = list()
    for comp in Competition.objects.filter(status=Competition.StatusChoices.ANNOUNSED, isHighLevelSportEvent=True):
        listOfAnnouncedEvents.append(comp.getData())
    for comp in Competition.objects.filter(status=Competition.StatusChoices.CURRENT, isHighLevelSportEvent=True):
        listOfCurrentEvents.append(comp.getData())
    for olympics in Olympics.objects.filter(status=Olympics.StatusChoices.CURRENT):
        listOfCurrentEvents.append(olympics.getData())

    data = {
        'announcedEvents':listOfAnnouncedEvents,
        'currentEvents': listOfCurrentEvents,
    }

    return render(request, 'competition.html', data)



def pastEventsView(request):
    data = {
        'userAuth':request.user.is_authenticated,
        "userIsJudge": request.user.has_perm('SCS.control_competition')
    }
    pastCompetitions = Competition.objects.filter(status=Olympics.StatusChoices.PAST)
    pastOlympics = Olympics.objects.filter(status=Olympics.StatusChoices.PAST)
    events = [e.getData() for e in pastOlympics] + [e.getData for e in pastCompetitions]


    if len(events) > settings.PAST_EVENT_PAGE_LEN:
        paginator = Paginator(events, settings.PAST_EVENT_PAGE_LEN)
        page_number = request.GET.get('page', 1)
        data['page_obj'] = paginator.get_page(page_number)
        data['pageList'] = paginator.get_elided_page_range(number=page_number)
        data['paginator'] = True
    else:
        data['page_obj'] = events
        data['pageList'] = []
        data['paginator'] = False
    return render(request, 'pastCompPage.html', data)
