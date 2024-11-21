from django import forms
from django.contrib.auth.models import User
from .models import Gamer, Game


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]


class GamerProfileForm(forms.ModelForm):
    delete_profile_picture = forms.BooleanField(
        required=False, label="Delete Profile Picture", initial=False
    )

    class Meta:
        model = Gamer
        fields = ["profile_picture"]

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("delete_profile_picture"):
            cleaned_data["profile_picture"] = None
        return cleaned_data


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = [
            "title",
            "category",
            "num_players",
            "avg_playing_time",
            "min_age",
            "description",
            "image",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "num_players": forms.TextInput(attrs={"class": "form-control"}),
            "avg_playing_time": forms.TextInput(attrs={"class": "form-control"}),
            "min_age": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
