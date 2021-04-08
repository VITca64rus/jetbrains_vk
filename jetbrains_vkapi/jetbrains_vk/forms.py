from django import forms

class DomainForm(forms.Form):
    domain = forms.DateField(label='Короткий адрес пользователя или сообщества')
    date_2 = forms.DateField (label='Конечная дата')