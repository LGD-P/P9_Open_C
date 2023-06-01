from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model, password_validation


class SignupForm(UserCreationForm):
    username = UsernameField(label=False, widget=forms.TextInput(
        attrs={"autofocus": True, "placeholder": "Nom d'utilisateur"}))
    password1 = forms.CharField(label=False,
                                strip=False,
                                widget=forms.PasswordInput(
                                    attrs={"autocomplete": "new-password", "placeholder": "Mot de passe"}),
                                help_text=password_validation.password_validators_help_text_html(),
                                )
    password2 = forms.CharField(label=False,
                                widget=forms.PasswordInput(
                                    attrs={"autocomplete": "new-password",
                                           "placeholder": "Confirmation du mot de passe"}),
                                strip=False,
                                help_text=(
                                    "Entrer le même mot de passe que précédement."),
                                )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ["username"]
