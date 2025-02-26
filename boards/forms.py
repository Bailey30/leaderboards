from django import forms


class ScoreForm(forms.Form):
    username = forms.CharField(label="Enter name", max_length=3)
    score = forms.IntegerField(label="Score")
