from django.contrib.auth import get_user_model, forms


User = get_user_model()


class CreationForm(forms.UserCreationForm):
    password2 = None

    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1')


class AuthForm(forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta():
        model = User
        fields = ('username', 'password')


class PassChangeForm(forms.PasswordChangeForm):

    class Meta(forms.PasswordChangeForm):
        model = User
        fields = ('username', 'password')


class PassResetForm(forms.PasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if not user:
            raise forms.ValidationError(
                'Пользователь с таким e-mail не найден')

        return email
