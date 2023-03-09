from SCSapp.forms import CreateCompetitionsForm
from django.views.generic import TemplateView
from SCSapp.func import getUserAuthData
from django.contrib.auth.decorators import login_required, permission_required   
from django.contrib.auth.mixins import LoginRequiredMixin

# @login_required()
# @permission_required()
class CreateCompetitionView(LoginRequiredMixin, TemplateView):
    login_url = '/loginPage/'
    permission_required = 'scsapp.add_competition'
    template_name = 'createCompetitions.html'



