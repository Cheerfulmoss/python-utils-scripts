"""
Alexander Bürow - 13 October 2023

License: GPL3
"""

class TableOut:
    def __init__(self, headers: list[any, ...], rows: list[list[any, ...]],
                 cell_x_padding: int, title: str | None):
        """Creates a TableOut class which formats the given parameters into a
            basic table

        :param headers: The headers of each column in the table.
        :param rows: The rows of the table ( everything below the 'headers' ).
        :param cell_x_padding: The padding for the cells.
        :param title: The title of the table, can be None if no title is wanted.
        """
        self._headers = headers
        self._rows = rows
        self._x_padding = cell_x_padding
        self._title = title

        if any(len(self._headers) != len(row) for row in self._rows):
            raise ValueError("'headers' and 'rows' should have the same "
                             "number of values")

        previous_row = 0
        for row in self._rows:
            if len(row) != previous_row and previous_row != 0:
                raise ValueError("'rows' must be a rectangular matrix")

    def __add__(self, other):
        matrix_a = [len(row) for row in self._rows]
        matrix_b = [len(row) for row in other._rows]
        for index, row_length in enumerate(matrix_a):
            if row_length != matrix_b[index] or len(matrix_a) != len(matrix_b):
                raise ValueError("Row matrices not of same size")

        new_rows = list()
        for index, row in enumerate(self._rows):
            new_rows.append(row + other._rows[index])

        return TableOut(headers=self._headers + other._headers,
                        rows=new_rows,
                        cell_x_padding=self._x_padding,
                        title=f"{self._title} / {other._title}")

    def __len__(self):
        return len(self._rows) * len(self._rows[0])

    def __repr__(self):
        return (f"TableOut({self._headers}, {self._rows}, "
                f"{self._x_padding}, {self._title})")

    def __str__(self):
        return "\n".join(self._make_basic_table())

    @staticmethod
    def _column_width_add_dict(column_widths: dict[int: int, ...],
                               column: int, value: int) -> dict[int: int, ...]:
        if column not in column_widths or column_widths[column] < value:
            column_widths[column] = value
        return column_widths

    @staticmethod
    def _construct_multi_row(row: list[any, ...] | None,
                             column_widths: dict[int: int, ...],
                             border: str, alignment: int | None) -> str:
        match alignment:
            case 0:
                justify = "<"
            case 2:
                justify = ">"
            case _:
                justify = "^"
        if row is not None:
            table_row = border + border.join([
                f"{value: {justify}{column_widths[column]}}"
                if column < len(column_widths) - 1
                else f"{value: {justify}{column_widths[column]}}{border}"
                for column, value in enumerate(row)
            ])
        else:
            table_row = border + border.join([
                "-" * value
                if column < len(column_widths) - 1
                else ('-' * value) + border
                for column, value in
                column_widths.items()
            ])
        return table_row

    def _max_column_widths(self):
        column_widths = dict()
        for row in self._rows:
            for column, value in enumerate(row):
                value_len = len(str(value)) + self._x_padding
                column_widths = self._column_width_add_dict(column_widths,
                                                            column, value_len)
        for column, header in enumerate(self._headers):
            header_len = len(str(header)) + self._x_padding
            column_widths = self._column_width_add_dict(column_widths,
                                                        column, header_len)
        return column_widths

    def _make_basic_table(self):
        column_widths = self._max_column_widths()
        table_frame = self._construct_multi_row(None, column_widths, "+", None)
        table_header = self._construct_multi_row(self._headers, column_widths,
                                                 "|", 0)
        if self._title is not None:
            width = int(len(table_frame) - (self._x_padding // 2))
            top_title_frame = self._construct_multi_row(None, {0: width}, "+",
                                                        None)
            bottom_title_frame = (
                self._construct_multi_row(None, column_widths, "+", None))
            title_header = self._construct_multi_row([self._title], [width],
                                                     "|", 1)
            table = [top_title_frame, title_header, bottom_title_frame,
                     table_header, table_frame]
        else:
            table = [table_frame, table_header, table_frame]
        for row in self._rows:
            value_row = self._construct_multi_row(row, column_widths, "|", 1)
            table.append(value_row)
        table.append(table_frame)
        return table

    def print_basic_table(self):
        print("\n".join(self._make_basic_table()))


if __name__ == "__main__":
    headings = ["Cost", "Simplicity", "Redundancy", "Safety", "Size",
                "Processing Power", "device Storage"]

    base_score = ((2, 3, 3, 1, 2, 3, 3),
                  (1, 2, 2, 2, 1, 2, 2),
                  (3, 1, 1, 3, 3, 1, 1))

    one = TableOut(headings, base_score, 4, "Matrix thing")
    two = TableOut(headings, base_score, 4, "Matrix thing 2")
    one.print_basic_table()
    print(one)
    print(len(one))
    (one + two).print_basic_table()
