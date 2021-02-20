from django import forms
from .models import Process, Memo

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
            'data1_col',
            'data1_process', 'data1_periods',
            'data2_col',
            'data2_process', 'data2_periods',
            'calc',
            'weekday', 'sma_num',
        )
        widgets = {
            'name': forms.TextInput(
                attrs={'placeholder': '記入例：PCR陽性者数（７日平均）'}),
            'data1_process': forms.Select(),
            'data1_periods': forms.NumberInput(),
            'data2_process': forms.Select(),
            'data2_periods': forms.NumberInput(),
            'calc': forms.Select(),
            'weekday': forms.CheckboxInput(),
            'sma_num': forms.NumberInput(),
        }

    def __init__(self, *args, **kwargs):
        super(ProcessForm, self).__init__(*args, **kwargs)
        self.fields['data1_col'].queryset = CSVColumn.objects.filter(axis='Y')
        self.fields['data2_col'].queryset = CSVColumn.objects.filter(axis='Y')
        self.fields['data1_process'].label = "処理"
        self.fields['data1_periods'].label = "間隔"
        self.fields['data2_process'].label = "処理"
        self.fields['data2_periods'].label = "間隔"


class MemoForm(forms.ModelForm):
    class Meta:
        model = Memo
        fields = ('memo',)
        widgets = {
            'memo': forms.Textarea(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['memo'].label = False


MemoFormset = forms.inlineformset_factory(
    Process, Memo, MemoForm, extra=0, can_delete=False, )
