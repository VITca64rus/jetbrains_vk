from django import forms

class DomainForm(forms.Form):
    domain = forms.DateField(label='ID пользователя или сообщества')