from django import forms

from .models import analise


class Forms:
    pass

class formulario_nova_analise(forms.ModelForm):
    OPCAO_CHOICES = [
        ('null', 'Selecione uma opção'),
        ('SF_Salaries', 'SF Salaries'),
        ('Salary_Dataset_with_Extra_Features', 'Software Industry Salary Dataset - 2022'),
        ('DataScience_salaries_2024', 'Latest Data Science Job Salaries 2020 - 2024'),
    ]

    nome_analise = forms.ChoiceField(choices=OPCAO_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = analise
        fields = ['nome_analise']