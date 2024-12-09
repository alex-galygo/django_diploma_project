# mixins.py
from django.db.models import Case, When, Value, IntegerField
from django.utils import timezone


class SortMixin:
    def get_sorted_queryset(self, queryset):
        sort_param = self.request.GET.get('sort')

        if sort_param:
            if sort_param == 'priority':
                queryset = queryset.order_by(
                    Case(
                        When(priority='HIGH', then=Value(1)),
                        When(priority='MEDIUM', then=Value(2)),
                        When(priority='LOW', then=Value(3)),
                        default=Value(4),
                        output_field=IntegerField(),
                    )
                )
                # elif sort_param == 'status':
            #     queryset = queryset.order_by(
            #         Case(
            #             When(status='NEW', then=Value(1)),
            #             When(status='IN_PROGRESS', then=Value(2)),
            #             When(status='DONE', then=Value(3)),
            #             default=Value(4),
            #             output_field=IntegerField(),
            #         )
            #     )
            elif sort_param == 'due_date':
                # Сначала задачи с дедлайном (сортировка по возрастанию)
                queryset = queryset.order_by(
                    Case(
                        When(due_date__isnull=True, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    ),
                    'due_date'
                )
            # elif sort_param == '-due_date':
            #     # Сначала задачи с дедлайном (сортировка по убыванию)
            #     queryset = queryset.order_by(
            #         Case(
            #             When(due_date__isnull=True, then=Value(1)),
            #             default=Value(0),
            #             output_field=IntegerField(),
            #         ),
            #         '-due_date'
            #     )
            elif sort_param in ['created_at', '-created_at']:
                queryset = queryset.order_by(sort_param)

        return queryset

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['sort'] = self.request.GET.get('sort')
    #     return context
