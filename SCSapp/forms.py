from django import forms
from SCSapp.models.Competition import Competition
from SCSapp.models.Olympics import Olympics
from SCSapp.models.Player import Player
#from SCSapp.models.Match import Match
from django.forms.widgets import DateTimeInput, TextInput, Textarea, RadioSelect, Select, FileInput

#from crispy_forms.helper import FormHelper
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# class MatchEditForm(forms.ModelForm):
#     id = forms.IntegerField()
#     class Meta:
#         model = Match
#         fields = ['name', 'place', 'matchDateTime']
#         widgets = {
#             'place':TextInput(attrs={
#                 'id': 'id_place',
#                 'type': "text",
#                 'class': "form-control",
#                 'placeholder': "Место проведения",
#                 'required': '',
#             }),
#             'matchDateTime':DateTimeInput(attrs={
#                 'id':'id_datetimepicker',
#                 'type':"text",
#                 'class':"form-control",
#                 'placeholder':"Время проведения матча",
#                 'required':'',
#             })
#         }



class CreateCompetitionsForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = ['name', 'description', 'dateTimeStartCompetition', 'sportType', 'type', 'regulations']
        widgets = {
            'name':TextInput(attrs={
                'id': 'competition-title',
                'class': "form-control",
                'placeholder': "Томская межвузовская спартакиада",
                'required': ''
            }),
            'regulations':FileInput(attrs={
                'id':'regulations',
                'class':'competition-regulations',
                'type':'file'
            }),
            'description':Textarea(attrs={
                'id': 'competition-description',
                'class': "form-control competition-description",
                'placeholder': "Ежегодная Томская спартакиада, в которой принимают участие все вузы города",
                'cols': '30',
                'rows': '5',
                'required': ''
            }),
            'dateTimeStartCompetition':TextInput(attrs={
                 'id':'competition-date',
                 'type':"datetime-local",
                 'class':"form-control",
                 'required':'',
            }),
            'sportType':Select(attrs={
                 'id': 'competition-sport',
                 'class': 'form-select',
                 'required': '',
            }),
            'type':RadioSelect(attrs={
                'id': 'flexRadioDefault',
                'class': 'form-check-input',
                'name': 'flexRadioDefault',
                'checked': '',
                'required': '',
            }),
        }


class CreateRelatedCompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = ['name', 'description', 'dateTimeStartCompetition', 'sportType', 'type', 'regulations']
        widgets = {
            'regulations':FileInput(attrs={
                'id':'regulations',
                'class':'competition-regulations',
                'type':'file'
            }),
            'description':Textarea(attrs={
                'id': 'competition-description',
                'class': "form-control competition-description add-competition-input",
                'placeholder': "Ежегодная Томская спартакиада, в которой принимают участие все вузы города",
                'cols': '30',
                'rows': '5',
                'required': ''
            }),
            'dateTimeStartCompetition':TextInput(attrs={
                 'id':'competition-date',
                 'type':"datetime-local",
                 'class':"form-control add-competition-input",
                 'required':'',
            }),
            'sportType':Select(attrs={
                 'id': 'competition-sport',
                 'class': 'form-select add-competition-input',
                 'required': '',
            }),
        }
class CreateOlympicsForm(forms.ModelForm):
    class Meta:
        model = Olympics
        fields = ['name', 'description','type']
        widgets = {
            'name':TextInput(attrs={
                'id': 'competition-title',
                'class': "form-control",
                'placeholder': "Томская межвузовская спартакиада",
                'required': ''
            }),
            'description':Textarea(attrs={
                'id': 'competition-description',
                'class': "form-control competition-description",
                'placeholder': "Ежегодная Томская спартакиада, в которой принимают участие все вузы города",
                'cols': '30',
                'rows': '5',
                'required': ''
            }),
            'type':RadioSelect(attrs={
                'id': 'flexRadioDefault',
                'class': 'form-check-input',
                'name': 'flexRadioDefault',
                'checked': '',
                'required': '',
            }),
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
