from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm, AuthenticationForm,
    PasswordChangeForm, PasswordResetForm)
from django import forms


User = get_user_model()


class CreationForm(UserCreationForm):
    password2 = None

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1')


class AuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta():
        model = User
        fields = ('username', 'password')


class PassChangeForm(PasswordChangeForm):

    class Meta(PasswordChangeForm):
        model = User
        fields = ('username', 'password')


class PassResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email__iexact=email).exists()
        if not user:
            raise forms.ValidationError(
                'Пользователь с таким e-mail не найден')

        return email
