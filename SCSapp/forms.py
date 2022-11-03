from django import forms
from SCSapp.models.Competition import Competition
from SCSapp.models.Olympics import Olympics
from SCSapp.models.Player import Player
#from SCSapp.models.Match import Match
from django.forms.widgets import DateTimeInput, TextInput, Textarea, RadioSelect, Select, FileInput
from django.forms import modelformset_factory

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
            'type': RadioSelect(attrs={
                'id': 'flexRadioDefault',
                'class': 'form-check-input',
                'name': 'flexRadioDefault',
                'checked': '',
                'required': '',
            }),

        }


CompetitionFormSet = modelformset_factory(
    Competition,
    fields=['description', 'dateTimeStartCompetition', 'sportType', 'regulations'],
    labels={},
    widgets= {
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
)

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
