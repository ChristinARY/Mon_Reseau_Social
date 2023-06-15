from django import forms
from .models import Publication
from .models import Service
from .models import Offre
from .models import Video
#Formulaire pour l' IA blagues



class JokeForm(forms.Form):
    topic = forms.CharField(label='Sujet', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sujet de la blague'}))


class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'border border-info form-control mb-4'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }



class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'border border-info form-control'}),
            'content': forms.Textarea(attrs={'class': 'border border-info form-control mb-4'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }


class OffreForm(forms.ModelForm):
    class Meta:
        model = Offre
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'border border-info form-control'}),
            'content': forms.Textarea(attrs={'class': 'border border-info form-control mb-4'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }





class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('content','video')