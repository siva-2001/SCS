from django.shortcuts import render, redirect
from SCSapp.models.Competition import Competition
from SCSapp.models.Olympics import Olympics
from SCSapp.forms import CreateOlympicsForm
from SCSapp.forms import CreateRelatedCompetitionForm
from django.forms import formset_factory
from SportCompetitionService import settings
from django.contrib.auth.decorators import login_required
from SCSapp.func import convertDTPickerStrToDateTime

#@login_required
def createOlympicsView(request):
    userIsJudge = request.user.has_perm('SCS.control_competition')
    data = {
        "form":{
            'olymics' : CreateOlympicsForm(),
            'competitions' : formset_factory(CreateRelatedCompetitionForm,
                extra=settings.MAX_COMPETITIONS_NUM_IN_OLYMPICS),
        },
        "userAuth":True,
        "userIsJudge": userIsJudge,
        "maxCompetitionNum":settings.MAX_COMPETITIONS_NUM_IN_OLYMPICS,
    }
    if request.method == "GET": return render(request, 'createOlympics.html', data)
    else:
        try:
            newOlympics = Olympics.create(
                name=request.POST['name'],
                description=request.POST['description'],
                organizer=request.user,
                type=request.POST['type'],
            )
            for compInd in request.POST['compNum']:
                Competition.create(
                    name=request.POST['name_'.join([str(compInd)])],
                    description=request.POST['description_'.join([str(compInd)])],
                    sportType=request.POST['sportType_'.join([str(compInd)])],
                    organizer=request.user,
                    type=request.POST['type_'.join([str(compInd)])],
                    isHighLevel=False,
                    regulations=request.FILES.get('regulations_'.join([str(compInd)]), None),
                )
            return redirect(newOlympics)
        except Exception as e:
            data['error'] = "bad data, try again"
            return render(request, 'createCompetitions.html', data)
