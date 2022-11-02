from django.shortcuts import render, redirect
from SCSapp.models.Competition import Competition
from SCSapp.models.Olympics import Olympics
from django.views.generic import TemplateView
from SCSapp.forms import CompetitionFormSet
from SCSapp.forms import CreateOlympicsForm
#from django.forms import formset_factory
from SportCompetitionService import settings
from django.contrib.auth.decorators import login_required
from SCSapp.func import convertDTPickerStrToDateTime

# #@login_required
class CreateOlympicsView(TemplateView):
    #template_name = 'createOlympics.html'
    template_name = 'create.html'

    def get(self, *args, **kwargs):
        data = {
            "competitionFormSet":CompetitionFormSet(queryset=Competition.objects.none()),
            "olympicsForm":CreateOlympicsForm(),
        }
        return self.render_to_response(data)

    def post(self, *args, **kwargs):
        print(self.request.POST['name'])
        formset = CompetitionFormSet(data=self.request.POST)
        olympicsForm = CreateOlympicsForm(data=self.request.POST)
        if formset.is_valid() and olympicsForm.is_valid():
            competitions = formset.save(commit=False)
            olympics = olympicsForm.save(commit=False)
            olympics.organizer = self.request.user
            olympics.save()
            for comp in competitions:
                comp.organizer = self.request.user
                print(comp.description)
                # comp.olympics = olympics
                comp.save()
            return redirect('homePage')

        return self.render_to_response({
            "competitionFormset": formset,
            "olympicsForm": CreateOlympicsForm(),
        })



# def createOlympicsView(request):
#     userIsJudge = request.user.has_perm('SCS.control_competition')
#     data = {
#         "form":{
#             'olympics' : CreateOlympicsForm(),
#             'competitions' : formset_factory(CreateRelatedCompetitionForm,
#                 extra=settings.MAX_COMPETITIONS_NUM_IN_OLYMPICS),
#         },
#         "userAuth":True,
#         "userIsJudge": userIsJudge,
#         "maxCompetitionNum":settings.MAX_COMPETITIONS_NUM_IN_OLYMPICS,
#     }
#     if request.method == "GET": return render(request, 'createOlympics.html', data)
#     else:
#         try:
#             newOlympics = Olympics.create(
#                 name=request.POST['name'],
#                 description=request.POST['description'],
#                 organizer=request.user,
#                 type=request.POST['type'],
#             )
#             for compInd in request.POST['compNum']:
#                 Competition.create(
#                     name=request.POST['name_'.join([str(compInd)])],
#                     description=request.POST['description_'.join([str(compInd)])],
#                     sportType=request.POST['sportType_'.join([str(compInd)])],
#                     organizer=request.user,
#                     type=request.POST['type_'.join([str(compInd)])],
#                     isHighLevel=False,
#                     regulations=request.FILES.get('regulations_'.join([str(compInd)]), None),
#                 )
#             return redirect(newOlympics)
#         except Exception as e:
#             data['error'] = "bad data, try again"
#             return render(request, 'createCompetitions.html', data)
