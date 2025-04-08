# Django
from django.contrib.postgres.forms import SplitArrayWidget


class TableWidget(SplitArrayWidget):
    template_name = "django_table_widgets/widgets/table.html"

    def __init__(
        self,
        widget,
        rows_headers,
        columns_headers,
        show_row_sum=False,
        show_column_sum=False,
        show_table_sum=False,
        **kwargs,
    ):
        self.rows_headers = rows_headers
        self.columns_headers = columns_headers
        self.show_row_sum = show_row_sum
        self.show_column_sum = show_column_sum
        self.show_table_sum = show_table_sum
        size = len(rows_headers)
        super().__init__(widget, size, **kwargs)

    def get_context(self, name, value, attrs=None):
        context = super().get_context(name, value, attrs)
        context["columns_headers"] = self.columns_headers
        context["rows_count"] = len(self.rows_headers)
        context["columns_count"] = len(self.columns_headers)
        context["show_row_sum"] = self.show_row_sum
        context["show_column_sum"] = self.show_column_sum
        context["show_table_sum"] = self.show_table_sum
        value = value or []
        for i in range(max(len(value), self.size)):
            context["widget"]["subwidgets"][i].setdefault(
                "header", self.rows_headers[i]
            )
            context["widget"]["subwidgets"][i].setdefault("row_index", i)
        return context

    class Media:
        js = ("django_table_widgets/js/TableFieldSum.js",)


class TableRowWidget(SplitArrayWidget):
    template_name = "django_table_widgets/widgets/row.html"

    def get_context(self, name, value, attrs=None):
        context = super().get_context(name, value, attrs)
        context["row_index"] = attrs.get("id").split("_")[-1]
        return context


class TableRowSumWidget(TableRowWidget):
    template_name = "django_table_widgets/widgets/row_sum.html"
