from django.shortcuts import render, redirect
from SCSapp.models.Competition import Competition
from SCSapp.forms import CreateCompetitionsForm
from django.contrib.auth.decorators import login_required
from SCSapp.func import convertDTPickerStrToDateTime
#
@login_required
def createCompetitionView(request):
    userIsJudge = request.user.has_perm('SCS.control_competition')
    if request.method == "GET":
        return  render(request, 'createCompetitions.html', {
            "form":CreateCompetitionsForm(),
            "userAuth":True,
            "userIsJudge": userIsJudge
        })
    else:
        try:
            Competition.create(
                name=request.POST['name'],
                discription=request.POST['discription'],
                sportType=request.POST['sportType'],
                startDate=convertDTPickerStrToDateTime(request.POST['lastTimeForApplications']),
                organizer=request.user,
                type=request.POST['type'],
                status=Competition.ANNOUNSED
            )
            return redirect(newCompetition)
        except:
            return render(request, 'createCompetitions.html', {
                "form":CreateCompetitionsForm(),
                "error":"Bad data, try again",
                "userAuth":True,
                "userIsJudge":userIsJudge,
            })


