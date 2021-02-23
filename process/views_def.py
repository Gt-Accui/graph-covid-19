from .models import Memo, Image
from .plot import plot_image


def up_memo(process, memo):
    Memo.objects.update_or_create(
        process=process,
        defaults={'memo': memo},
    )


def up_image(process):
    url = plot_image(process)

    Image.objects.update_or_create(
        process=process,
        defaults={'url': url},
    )
