from django.shortcuts import render, redirect
from SCSapp.models.Competition import Competition
from SCSapp.forms import CreateCompetitionsForm
from django.contrib.auth.decorators import login_required
from SCSapp.func import convertDTPickerStrToDateTime

#@login_required
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
            newCompetition = Competition.create(
                name=request.POST['name'],
                description=request.POST['description'],
                sportType=request.POST['sportType'],
                #startDate=convertDTPickerStrToDateTime(request.POST['competition-date']),
                startDate=request.POST['dateStartCompetition'],
                organizer=request.user,
                type=request.POST['type'],
                isHighLevel=True,
                regulations=request.FILES.get('regulations'),
            )
            return redirect(newCompetition)
        except Exception as e:
            print(e.__str__())
            return render(request, 'createCompetitions.html', {
                "form":CreateCompetitionsForm(),
                "error":"Bad data, try again",
                "userAuth":True,
                "userIsJudge":userIsJudge,
            })


