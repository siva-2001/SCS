from django.shortcuts import render
from SCSapp.models.Competition import Competition
from SCSapp.models.Olympics import Olympics
from django.core.paginator import Paginator
from SportCompetitionService import settings
from SCSapp.func import getUserAuthData


def homePageView(request):
    listOfCurrentEvents = list()
    listOfAnnouncedEvents = list()
    for comp in Competition.announced_objects.all(): listOfAnnouncedEvents.append(comp.getData())
    for comp in Competition.current_objects.all(): listOfCurrentEvents.append(comp.getData())
    for olympics in Olympics.current_objects.all(): listOfCurrentEvents.append(olympics.getData())
    return render(request, 'homePage.html', {
        'announcedEvents':listOfAnnouncedEvents,
        'currentEvents': listOfCurrentEvents,
    } | getUserAuthData(request.user))


def pastCompetitionsView(request):
    data = getUserAuthData(request.user)
    pastCompetitions = Competition.objects.filter(status=Competition.StatusChoices.PAST)
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
    return render(request, 'pastEventsPage.html', data)
