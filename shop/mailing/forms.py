from django import forms

from mailing.models import Mailing


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['text']
