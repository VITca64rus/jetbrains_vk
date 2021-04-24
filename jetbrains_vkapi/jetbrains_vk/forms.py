from django import forms

GEEKS_CHOICES =(
    ("1", "---"),

    ("2", "Отбираем комментарии по дате поста"),

    ("3", "Отбираем комментарии по дате комментария (Загрузка в БД дольше)"),
)

class DomainForm(forms.Form):
    domain = forms.IntegerField(label='ID пользователя или сообщества')
    what = forms.ChoiceField (choices=GEEKS_CHOICES, label = 'Для чего используем даты?')
    data1 = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
    data2 = forms.DateTimeField(label = 'Анализировать по',
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker2'
        })
    )
