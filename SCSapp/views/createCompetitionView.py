from django.shortcuts import render, redirect
from SCSapp.models.Competition import Competition
from SCSapp.forms import CreateCompetitionsForm
from django.views.generic import TemplateView
from SCSapp.func import getUserAuthData
from SCSapp.serializers import CompetitionSerializer
from django.contrib.auth.decorators import login_required
from rest_framework.generics import CreateAPIView

#@login_required

class CreateCompetitionView(TemplateView):
    template_name = 'createCompetitions.html'

    def get(self, *args, **kwargs):
        return self.render_to_response({"form":CreateCompetitionsForm()} | getUserAuthData(self.request.user))

    def post(self, *args, **kwargs):
        competitionForm = CreateCompetitionsForm(data=self.request.POST)
        if competitionForm.is_valid():
            competition = competitionForm.save(commit=False)
            competition.organizer = self.request.user
            competition.save()
            return redirect(competition)
        return self.render_to_response({"form":CreateCompetitionsForm()} | getUserAuthData(self.request.user))


