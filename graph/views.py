from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from django.contrib import messages
import pandas as pd
import io

from .models import Source, CSVColumn, CSVData, PlotMode
from .forms import SourceForm, CSVColumnFormset, PlotModeFormset
from .plot import plot
from .filters import SourceFilter


def csv_str(source):
    with source.csv.open() as csv:  # csvを列ごとに取り出し、文字列として結合
        csv_str = ''
        for line in csv: csv_str += line.decode(encoding='UTF8')
        csv.close()

    CSVData.objects.update_or_create(
        source=source,
        defaults={'csv_str': csv_str},
    )


def csv_col_def(source):  # CSVの列ラベルをテーブル'CSVColumn'に保存
    csv_str = CSVData.objects.get(source=source).csv_str
    df = pd.read_csv(io.StringIO(csv_str))  # , encoding='UTF8',)
    columns = list(df.columns)

    for column in columns:  # 数値はY軸、その他はX軸をデフォルトとする
        col_num = columns.index(column)
        axis = 'Y'
        try: df.iloc[[0], [col_num]].values[0] / 1  # 日付はエラーと判定される
        except Exception: axis = 'X'

        CSVColumn.objects.update_or_create(
            source=source, csv_col_num=col_num, csv_col_label=column,
            defaults={'df_col_label': column, 'axis': axis},
            )


class SourceCreateView(CreateView):  # 登録画面
    model = Source
    form_class = SourceForm

    def get_success_url(self):
        return reverse('update', kwargs={'pk': self.object.id})  # 更新画面に遷移

    def form_valid(self, form):
        self.object = form.save()
        csv_str(self.object)
        csv_col_def(self.object)
        PlotMode(source=self.object, mode='lines').save()  # 折れ線をデフォルトに
        messages.info(self.request, f'{self.object.name}を保存しました。')
        return redirect(self.get_success_url())


class SourceUpdateView(UpdateView):  # 更新画面
    model = Source
    form_class = SourceForm

    def get_success_url(self):
        return reverse('update', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(SourceUpdateView, self).get_context_data(**kwargs)
        source = get_object_or_404(Source, pk=self.kwargs.get('pk'))
        context.update({
            'plot': plot(source),
            'source': source,
            'csvcolumns': CSVColumnFormset(
                self.request.POST or None, instance=source,
                prefix='csvcolumns',),
            'plotmode': PlotModeFormset(
                self.request.POST or None, instance=source,
                prefix='plotmode',),
        })
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset_col = context['csvcolumns']
        form_plot = context['plotmode']

        try:
            if formset_col.is_valid():
                formset_col.save()
                messages.info(
                    self.request, f'{self.object.name}の軸の設定を保存しました。')
                return redirect(self.get_success_url())
        except Exception as e_formset_c: print('e_formset_col', e_formset_c)

        try:
            if form_plot.is_valid():
                form_plot.save()
                messages.info(
                    self.request, f'{self.object.name}のグラフ種別を保存しました。')
                return redirect(self.get_success_url())
        except Exception as e_form_plot: print('e_form_plot', e_form_plot)

        if form.is_valid():
            self.object = form.save()  # commit=False)  # ← 必要性
            source = Source.objects.get(pk=self.object.id)
            try:
                print(source.csv.size)
                csv_str(self.object)
                csv_col_def(self.object)
            except Exception as e_csv_exist: print(e_csv_exist)
            messages.info(
                self.request, f'{self.object.name}を保存しました。')
            return redirect(self.get_success_url())
        else:
            print('Not Valid!')
            for ele in form: print(ele)
            return self.render_to_response(context)


class SourceFilterView(FilterView):
    model = Source
    filterset_class = SourceFilter
    queryset = Source.objects.all().order_by('-updated_at')  # 更新順をデフォに

    strict = False  # クエリ未指定時の全件検索オプション（django-filter2.0以降）
    paginate_by = 5  # 1ページあたりの表示件数

    def get(self, request, **kwargs):
        if request.GET:
            request.session['query'] = request.GET
        else:
            request.GET = request.GET.copy()
            if 'query' in request.session.keys():
                for key in request.session['query'].keys():
                    request.GET[key] = request.session['query'][key]

        try:
            return super().get(request, **kwargs)
        except Exception as e_session:
            print(e_session)
            request.GET['page'] = ''
            return super().get(request, **kwargs)


class SourceDeleteView(DeleteView):
    model = Source
    success_url = reverse_lazy('index')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.info(self.request, f'{self.object.name}を削除しました。')
        return redirect(self.get_success_url())
