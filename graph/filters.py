from django_filters import filters
from django_filters import FilterSet
from .models import Source


class MyOrderingFilter(filters.OrderingFilter):
    descending_fmt = '%s （降順）'


class SourceFilter(FilterSet):

    name = filters.CharFilter(
        label='名称（部分一致）', lookup_expr='contains')
    source = filters.CharFilter(
        label='出典（部分一致）', lookup_expr='contains')
    updated_at_gte = filters.DateTimeFilter(
        label='更新日（以降）', field_name='updated_at', lookup_expr='gte')
    updated_at_lte = filters.DateTimeFilter(
        label='更新日（以前）', field_name='updated_at', lookup_expr='lte')

    order_by = MyOrderingFilter(
        fields=(
            ('name', 'name'),
            ('updated_at', 'updated_at'),
        ),
        field_labels={
            'name': '名称',
            'updated_at': '更新日',
        },
        label='並び順'
    )

    class Meta:
        model = Source
        fields = (
            'name', 'source',
            'updated_at_gte', 'updated_at_lte',
        )
