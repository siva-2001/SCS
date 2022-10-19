from django import forms
from SCSapp.models.Competition import Competition
from SCSapp.models.Player import Player
from SCSapp.models.VolleyballTeam import VolleyballTeam
from SCSapp.models.Match import Match
from django.forms.widgets import DateTimeInput, TextInput, Textarea, Select
#from crispy_forms.helper import FormHelper
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class MatchEditForm(forms.ModelForm):
    id = forms.IntegerField()
    class Meta:
        model = Match
        fields = ['name', 'place', 'matchDateTime']
        widgets = {
            'place':TextInput(attrs={
                'id': 'id_place',
                'type': "text",
                'class': "form-control",
                'placeholder': "Место проведения",
                'required': '',
            }),
            'matchDateTime':DateTimeInput(attrs={
                'id':'id_datetimepicker',
                'type':"text",
                'class':"form-control",
                'placeholder':"Время проведения матча",
                'required':'',
            })
        }



class CreateCompetitionsForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = ['_name', '_discription', '_dateTimeStartCompetition', '_sportType', '_type']
        widgets = {
            '_name':TextInput(attrs={
                'id': 'competition-title',
                'type': "text",
                'class': "form-control",
                'placeholder': "Соревнования по волейболу",
                'required': ''
            }),
            '_discription':Textarea(attrs={
                'id': 'competition-description',
                'class': "form-control competition-description",
                'placeholder': "Описание предстоящих соревнований",
                'cols': '30',
                'rows': '10',
                'required': ''
            }),
            '_dateTimeStartCompetition':TextInput(attrs={
                 'id':'competition-date',
                 'type':"date",
                 'class':"form-control",
                 'required':'',
            }),
            '_sportType':Select(attrs={
                 'id': 'competition-sport',
                 'class': 'form-select',
                 'required': '',
            }),
            '_type':TextInput(attrs={
                'id': 'flexRadioDefault1',
                'class': 'form-check-input mt-2',
                'type': 'radio',
                'name': 'flexRadioDefault',
                'checked': '',
                'required': '',
            }),
#             '_type2':TextInput(attrs={
#                 'id': 'flexRadioDefault2',
#                 'class': 'form-check-input mt-2',
#                 'type': 'radio',
#                 'name': 'flexRadioDefault',
#                 'required': '',
#             }),
        }
        labels = {
            'name':'Заголовок:',
            'discription':'Описание:',
            '_dateTimeStartCompetition':'Заявки подаются до:',
        }

# class RegistrPlayerForm(forms.ModelForm):
#     class Meta:
#         model = Player
#         fields = ['name', 'surename', 'patronymic', 'age']
#         widgets = {
#             'name':TextInput(attrs={
#                 'class': "form-control",
#                 'placeholder': "Имя",
#                 'required': ''
#             }),
#             'surename': TextInput(attrs={
#                 'class': "form-control",
#                 'placeholder': "Фамилия",
#                 'required': ''
#             }),
#             'patronymic': TextInput(attrs={
#                 'class': "form-control",
#                 'placeholder': "Отчество",
#             }),
#             'age': TextInput(attrs={
#                 'class': "form-control",
#                 'placeholder': "Возраст",
#                 'required': ''
#             })
#         }
#
# class RegistrVolleybolTeamForm(forms.ModelForm):
#     class Meta:
#         model = VolleyballTeam
#         fields = ['name', 'discription']
#         labels = {
#             'name':"Название команды",
#             "discription":'Описание',
#
#         }
#         widgets = {
#             'name': TextInput(attrs={
#                 'id': 'id_teamName',
#                 'type': "text",
#                 'class': "form-control",
#                 'placeholder': "Название команды",
#                 'required': ''
#             }),
#             'discription': Textarea(attrs={
#                 'id': 'id_teamDiscription',
#                 'type': "text",
#                 'class': "form-control",
#                 'placeholder': "Описание команды",
#                 'required': '',
#                 'style':'resize:none;'
#             }),
#         }
#


#
# class SignUpUser(forms.ModelForm):
#     password1 = forms.CharField(widget=forms.PasswordInput)
#     password2 = forms.CharField(widget=forms.PasswordInput)
#
#     def clean_password2(self):
#         cd = self.cleaned_data
#         if cd['password1'] != cd['password2']:
#             raise forms.ValidationError('Passwords don\'t match.')
#         return cd['password2']
#
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email']
#         labels = {
#             'username': 'Логин:',
#             'email':'E-mail:',
#             'first_name': 'Имя',
#             'last_name': 'Фамилия'
#         }
#
#
