from django.contrib import admin
from .models import Process, Memo, Image


@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):
    pass


@admin.register(Memo)
class MemoAdmin(admin.ModelAdmin):
    pass


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass
