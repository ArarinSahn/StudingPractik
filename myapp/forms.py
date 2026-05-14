from cProfile import label

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from myapp.models import Application


class RegisterForm(UserCreationForm):
    fio = forms.CharField(label='ФИО', max_length=100)
    phone = forms.CharField()

    # phone = PhoneNumberField(label='Телефон', max_length=20,
    #     widget=PhoneNumberPrefixWidget(attrs={'class': 'form-control'})
    # )
    email = forms.EmailField(label='Электронная почта')
    class Meta:
        model = User
        fields = ["username", "password1", "password2", "fio", "phone", "email"]
        # widgets = {
        #     'phone': PhoneNumberPrefixWidget(),
        # }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control"})
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})
        self.fields["fio"].widget.attrs.update({"class": "form-control"})
        self.fields["phone"].widget.attrs.update({"class": "form-control", "value":"+7"})
        self.fields["email"].widget.attrs.update({"class": "form-control"})

class ApplicationCreateForm(ModelForm):
    class Meta:
        model = Application
        #fields = ["quantity_sit", "id_pay", "password2", "fio", "phone", "email"]
        exclude = ['id_aplic','id_ststus','review','date_create','id_user']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["quantity_sit"].widget.attrs.update({"class": "form-control"})
        self.fields["id_pay"].widget.attrs.update({"class": "form-control"})
        self.fields["id_con_event"].widget.attrs.update({"class": "form-control"})


