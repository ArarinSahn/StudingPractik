from cProfile import label


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.utils import timezone
from myapp.models import Application,DateConductEvent


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


class LocalizedDateConductEventChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        local_date = timezone.localtime(obj.date_con)
        formatted_date = local_date.strftime("%d.%m.%Y %H:%M")
        if hasattr(obj, 'remaining_places'):
            places_info = f"мест: {obj.remaining_places}"
        else:
            places_info = f"мест: {obj.max_member}"
        return f"{obj.id_event.name} — {formatted_date}, {places_info}"


class ApplicationCreateForm(ModelForm):
    id_con_event = LocalizedDateConductEventChoiceField(
        queryset=DateConductEvent.objects.all(),
        widget=forms.RadioSelect(),
        label="Доступные сеансы"
    )




    class Meta:
        model = Application
        fields = ['id_con_event', 'quantity_sit', 'id_pay']
        exclude = ['id_user', 'id_ststus']
        widgets = {
            'id_con_event': forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        id_event = kwargs.pop('id_event', None)
        super().__init__(*args, **kwargs)

        if id_event:
            self.fields['id_con_event'].queryset = DateConductEvent.objects.filter(id_event_id=id_event)
        else:
            self.fields['id_con_event'].queryset = DateConductEvent.objects.all()
        self.fields['id_con_event'].label = "Доступные сеансы"

    def clean(self):
        cleaned_data = super().clean()
        id_con_event = cleaned_data.get('id_con_event')
        quantity_sit = cleaned_data.get('quantity_sit')

        if quantity_sit is None and self.data.get('quantity_sit'):
            try:
                quantity_sit = int(self.data.get('quantity_sit'))
                cleaned_data['quantity_sit'] = quantity_sit
            except ValueError:
                pass

        if quantity_sit is not None and quantity_sit < 1:
            self.add_error('quantity_sit', "Количество участников должно быть больше 0.")
            return cleaned_data

        if id_con_event and quantity_sit:
            available_places = id_con_event.remaining_places

            if available_places <= 0:
                self.add_error('id_con_event', "На этот сеанс больше нет свободных мест!")
                self.add_error('quantity_sit', "Запись невозможна, места закончились.")

            elif quantity_sit > available_places:
                self.add_error('quantity_sit', f"Недостаточно мест! Можно забронировать максимум: {available_places}")

        return cleaned_data

    def clean_quantity_sit(self):
        quantity = self.cleaned_data.get('quantity_sit')






