from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from main_page.models import User


class MyAuthenticationForm(AuthenticationForm):

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )



class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Это поле обязательно')
    first_name = forms.CharField(max_length=254, help_text='Это поле обязательно')
    last_name = forms.CharField(max_length=254, help_text='Это поле обязательно')
    phone_number = forms.CharField(max_length=254, help_text='Это поле обязательно')

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'address', 'city', 'password1', 'password2', )
