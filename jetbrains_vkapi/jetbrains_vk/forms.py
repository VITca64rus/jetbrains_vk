from django import forms

GEEKS_CHOICES =(
    ("1", "---"),

    ("2", "Отбираем комментарии по дате поста"),

    ("3", "Отбираем комментарии по дате комментария (Загрузка в БД дольше)"),
)

class DomainForm(forms.Form):
    domain = forms.IntegerField(label='ID пользователя или сообщества')
    what = forms.ChoiceField (choices=GEEKS_CHOICES, label = 'Для чего используем даты?')
    data1 = forms.DateField ( input_formats='%d/%m/%Y', label='Анализ с')
    data2 = forms.DateField (input_formats='%d/%m/%Y', label='Анализ по')
