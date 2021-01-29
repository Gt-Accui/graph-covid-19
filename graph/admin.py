from django.contrib import admin
from .models import Source, CSVColumn, CSVData, PlotMode


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    pass


@admin.register(CSVColumn)
class CSVColumnAdmin(admin.ModelAdmin):
    pass


@admin.register(CSVData)
class CSVDataAdmin(admin.ModelAdmin):
    pass


@admin.register(PlotMode)
class PlotModeAdmin(admin.ModelAdmin):
    pass
