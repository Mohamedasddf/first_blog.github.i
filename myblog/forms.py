from django import forms
from .models import Comment
from .models import SiteRating
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']


class SiteRatingForm(forms.ModelForm):
    class Meta:
        model = SiteRating
        fields = ['rating', 'comment']

    rating = forms.ChoiceField(choices=[(i, str(i)) for i in range(1, 6)])  # خيارات النجوم من 1 إلى 5
