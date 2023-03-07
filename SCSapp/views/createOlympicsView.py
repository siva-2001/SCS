from django.shortcuts import redirect
from SCSapp.models.Competition import Competition
from django.views.generic import TemplateView
from SCSapp.forms import CompetitionFormSet
from SCSapp.forms import CreateOlympicsForm
from SCSapp.func import getUserAuthData


# #@login_required
class CreateOlympicsView(TemplateView):
    template_name = 'createOlympics.html'

    def get(self, *args, **kwargs):
        data = {
            "competitionFormSet":CompetitionFormSet(queryset=Competition.objects.none()),
            "olympicsForm":CreateOlympicsForm(),
        } | getUserAuthData(self.request.user)
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
                comp.olympics = olympics
                comp.isHighLevelSportEvent = False
                comp.save()
            return redirect('homePage')
        return self.render_to_response({
            "competitionFormset": formset,
            "olympicsForm": olympicsForm,
        } | getUserAuthData(self.request.user))

