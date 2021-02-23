from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from django.contrib import messages

from .models import Process
from .forms import ProcessForm, MemoFormset
from .plot import plot
from .filters import ProcessFilter
from .views_def import up_memo, up_image


class ProcessCreateView(CreateView):  # 登録画面
    model = Process
    form_class = ProcessForm

    def get_success_url(self):
        return reverse('process_update', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        self.object = form.save()
        memo = ""
        up_memo(self.object, memo)
        up_image(self.object)
        messages.info(self.request, f'{self.object.name}を保存しました。')
        return redirect(self.get_success_url())


class ProcessUpdateView(UpdateView):  # 更新画面
    model = Process
    form_class = ProcessForm

    def get_success_url(self):
        return reverse('process_update', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(ProcessUpdateView, self).get_context_data(**kwargs)
        process = get_object_or_404(Process, pk=self.kwargs.get('pk'))
        context.update({
            'plot': plot(process),
            'process': process,
            'memo': MemoFormset(
                self.request.POST or None, instance=process,
                prefix='memo',),
        })
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset_memo = context['memo']

        try:
            if formset_memo.is_valid():
                formset_memo.save()
                messages.info(
                    self.request, f'{self.object.name}のメモを保存しました。')
                return redirect(self.get_success_url())
        except Exception: pass

        if form.is_valid():
            self.object = form.save()
            up_image(self.object)
            messages.info(
                self.request, f'{self.object.name}を保存しました。')
            return redirect(self.get_success_url())
        else:
            print('Not Valid!')
            for ele in form:
                print(ele)
            return self.render_to_response(context)


class ProcessFilterView(FilterView):
    model = Process
    filterset_class = ProcessFilter
    queryset = Process.objects.prefetch_related(
        'image').order_by('-updated_at')

    strict = False  # クエリ未指定時の全件検索オプション（django-filter2.0以降）
    paginate_by = 4  # 1ページあたりの表示件数

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
        except Exception:
            request.GET['page'] = ''
            return super().get(request, **kwargs)


class ProcessDeleteView(DeleteView):
    model = Process
    success_url = reverse_lazy('process')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.info(self.request, f'{self.object.name}を削除しました。')
        return redirect(self.get_success_url())
