from Django import forms
from .models  import review
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment','rating']