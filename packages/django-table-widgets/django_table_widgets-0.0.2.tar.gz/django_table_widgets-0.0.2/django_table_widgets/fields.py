# Django
from django.contrib.postgres.forms import SplitArrayField

# Local application / specific library imports
from .widgets import TableRowSumWidget, TableRowWidget, TableWidget


class TableRowField(SplitArrayField):
    def __init__(
        self, base_field, size, *, widget=None, remove_trailing_nulls=False, **kwargs
    ):
        self.base_field = base_field
        self.size = size
        self.remove_trailing_nulls = remove_trailing_nulls

        widgetClass = TableRowWidget if not widget else widget
        widget = widgetClass(widget=base_field.widget, size=size)
        kwargs.setdefault("widget", widget)

        # Bypass the SplitArrayField constructor
        super(SplitArrayField, self).__init__(**kwargs)


class TableField(SplitArrayField):
    def __init__(
        self,
        cell_field,
        rows_headers: list[str],
        columns_headers: list[str],
        *,
        widget=None,
        remove_trailing_nulls=False,
        show_row_sum=False,
        show_column_sum=False,
        show_table_sum=False,
        **kwargs,
    ):
        """
        A field to display a two dimensional table of inputs with a sum of rows and columns.

        :param cell_field: Field to display in the table cells (forms.IntegerField, forms.FloatField, etc.)
        :param rows_headers: List of headers for the rows
        :param columns_headers: List of headers for the columns
        :param widget: Widget to use for the table
        :param remove_trailing_nulls: Whether to remove trailing nulls from the table
        :param show_row_sum: Whether to show the row sum
        :param show_column_sum: Whether to show the column sum
        :param show_table_sum: Whether to show the table sum
        """
        self.size = len(rows_headers)
        self.remove_trailing_nulls = remove_trailing_nulls

        RowWidgetClass = TableRowSumWidget if show_row_sum else TableRowWidget
        self.base_field = TableRowField(
            cell_field, widget=RowWidgetClass, size=len(columns_headers), **kwargs
        )

        TableWidgetClass = TableWidget if not widget else widget
        widget = TableWidgetClass(
            widget=self.base_field.widget,
            rows_headers=rows_headers,
            columns_headers=columns_headers,
            show_row_sum=show_row_sum,
            show_column_sum=show_column_sum,
            show_table_sum=show_table_sum,
        )
        kwargs.setdefault("widget", widget)

        # Bypass the SplitArrayField constructor
        super(SplitArrayField, self).__init__(**kwargs)
