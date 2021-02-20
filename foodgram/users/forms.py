from django.contrib.auth import get_user_model, forms 


User = get_user_model()

#

class CreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'username', 'email', 'password1')

    

class PassChangeForm(forms.PasswordChangeForm):
    pass

class PassResetForm(forms.PasswordResetForm):
    pass