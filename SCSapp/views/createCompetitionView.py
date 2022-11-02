from django.shortcuts import render, redirect
from SCSapp.models.Competition import Competition
from SCSapp.forms import CreateCompetitionsForm
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from SCSapp.func import convertDTPickerStrToDateTime

#@login_required

class CreateCompetitionView(TemplateView):
    template_name = 'createCompetitions.html'

    def get(self, *args, **kwargs):
        return self.render_to_response({"form":CreateCompetitionsForm()})

    def post(self, *args, **kwargs):
        competitionForm = CreateCompetitionsForm(data=self.request.POST)
        if competitionForm.is_valid():
            competition = competitionForm.save(commit=False)
            competition.organizer = self.request.user
            competition.save()
            return redirect(competition)
        return self.render_to_response({"form":competitionForm})

#
# def createCompetitionView(request):
#     userIsJudge = request.user.has_perm('SCS.control_competition')
#     data = {
#         "form":CreateCompetitionsForm(),
#         "userAuth":True,
#         "userIsJudge": userIsJudge
#     }
#     if request.method == "GET": return  render(request, 'createCompetitions.html', data)
#     else:
#         try:
#             newCompetition = Competition.create(
#                 name=request.POST['name'],
#                 description=request.POST['description'],
#                 sportType=request.POST['sportType'],
#                 startDate=request.POST['dateStartCompetition'],
#                 organizer=request.user,
#                 type=request.POST['type'],
#                 isHighLevel=True,
#                 regulations=request.FILES.get('regulations'),
#             )
#             return redirect(newCompetition)
#         except Exception as e:
#             print(e.__str__())
#             data['error'] = "Bad data, try again",
#             return render(request, 'createCompetitions.html', data)
#
#
