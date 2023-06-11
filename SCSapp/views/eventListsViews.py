from django.shortcuts import render
from SCSapp.models.Competition import Competition
# from SCSapp.models.Olympics import Olympics
from django.core.paginator import Paginator
from SportCompetitionService import settings
from django.views.generic import TemplateView

# class homePageView(TemplateView):
#     template_name = 'homePage.html'


def homePageView(request):
    return render(request, 'homePage.html', {
        'announcedEvents' : [comp.__dict__ for comp in Competition.announced_objects.all()],
        'currentEvents': [comp.__dict__ for comp in Competition.current_objects.all()],
    })


def pastEventsView(request):
    PAST_EVENT_PAGE_LEN = 10
    data = dict()
    events = [e.__dict__ for e in Competition.objects.filter(status=Competition.StatusChoices.PAST)]

    if len(events) > PAST_EVENT_PAGE_LEN:
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
