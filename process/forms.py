from django import forms
from .models import Process

import sys
sys.path.append('../')
from graph.models import CSVColumn


class ProcessForm(forms.ModelForm):
    class Meta:
        model = Process
        data1_col = forms.ModelChoiceField(  # ← Not widget
            queryset=CSVColumn.objects,)  # filterは'__init__'で上書き処理 ↓↓
        data2_col = forms.ModelChoiceField(
            queryset=CSVColumn.objects,)
        fields = (
            'name',
            'data1_col', 'data2_col',
            'calc',
            'weekday', 'sma_num',
        )
        widgets = {
            'name': forms.TextInput(
                attrs={'placeholder': '記入例：PCR陽性者数（７日平均）'}),
            'calc': forms.Select(),
            'weekday': forms.CheckboxInput(),
            'sma_num': forms.NumberInput(),
        }

    def __init__(self, *args, **kwargs):
        super(ProcessForm, self).__init__(*args, **kwargs)
        self.fields['data1_col'].queryset = CSVColumn.objects.filter(axis='Y')
        self.fields['data2_col'].queryset = CSVColumn.objects.filter(axis='Y')
