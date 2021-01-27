from django import forms
from .models import Source, CSVColumn, PlotMode


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ('name', 'source', 'url', 'csv')
        widgets = {
            'name': forms.TextInput(
                attrs={'placeholder': '記入例：PCR陽性者数（日別）'}),
            'source': forms.TextInput(
                attrs={'placeholder': '記入例：厚生労働省（日本）'}),
            'url': forms.URLInput(
                attrs={'placeholder': '情報源のURL'}),
            'csv': forms.FileInput(
                attrs={'class': 'custom-file-input'}),
        }

    def clean_csv(self):
        csv = self.cleaned_data['csv']
        if csv.name.endswith('.csv'):
            return csv
        else:
            raise forms.ValidationError('拡張子はcsvのみ対応')


class CSVColumnForm(forms.ModelForm):
    class Meta:
        model = CSVColumn
        fields = ('csv_col_num', 'csv_col_label', 'df_col_label', 'axis')
        widgets = {
            'csv_col_num': forms.NumberInput(
                attrs={'readonly': True}),  # 読取のみ
            'csv_col_label': forms.TextInput(
                attrs={'readonly': True}),  # 読取のみ
            'df_col_label': forms.TextInput(
                attrs={'placeholder': 'グラフでの表示名'}),
            'axis': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['csv_col_label'].label = False


CSVColumnFormset = forms.inlineformset_factory(
    Source, CSVColumn, CSVColumnForm, extra=0, can_delete=False, )


class PlotModeForm(forms.ModelForm):
    class Meta:
        model = PlotMode
        fields = ('mode',)
        widgets = {
            'mode': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mode'].label = False


PlotModeFormset = forms.inlineformset_factory(
    Source, PlotMode, PlotModeForm, extra=0, can_delete=False, )
