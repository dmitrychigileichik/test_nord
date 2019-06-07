from django.shortcuts import render
from django.contrib.auth.views import LoginView
from main_page import forms
from django.views.generic import FormView



class MyselfLoginView(LoginView):
    template_name = "login.html"
    form_class =  forms.MyAuthenticationForm


class RegisterFormView(FormView):
    form_class = forms.SignUpForm
    success_url = "/login/"
    template_name = "register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)