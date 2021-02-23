from .models import Process, Memo, Image
from .plot import plot_image


def up_memo(process, memo):
    Memo.objects.update_or_create(
        process=process,
        defaults={'memo': memo},
    )


def updated(pk, updated_at):
    Process.objects.update_or_create(
        pk=pk,
        defaults={'updated_at': updated_at},)


def up_image(process):
    url = plot_image(process)

    Image.objects.update_or_create(
        process=process,
        defaults={'url': url},
    )
