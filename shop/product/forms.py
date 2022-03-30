from django import forms

from product.models import Feedback, Likes, RATE_CHOICES


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['text']


class RateForm(forms.ModelForm):
    score = forms.ChoiceField(choices=RATE_CHOICES, widget=forms.Select(),
                              required=True)

    class Meta:
        model = Likes
        fields = ['score']

