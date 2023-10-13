"""
Alexander Bürow - 13 October 2023

License: GPL3
"""

from __future__ import annotations


class ListUtils:
    def __init__(self, *lists: list) -> None:
        self._lists = list(lists)

    def __repr__(self):
        return (f"ListUtils"
                f"({', '.join([str(sub_list) for sub_list in self._lists])})")

    def __str__(self):
        list_lens = [len(sub_list) for sub_list in self._lists]
        boiler = "List of length"
        return (f"<"
                f"{', '.join([f'{boiler} {length}' for length in list_lens])}"
                f">")

    def zip_columns(self) -> list:
        """Returns a list of the values grouped by index.

        Precondition
            All lists given to ListUtils must be the same length.
        """
        return list(zip(*self._lists))

    def unzip_columns(self) -> tuple:
        """Reverses the process of zip_columns

        Precondition:
            All lists given to ListUtils must be the same length.
            List_count must be the same number of values in each tuple.
            The number of values in each tuple must all be the same
        """
        unzipped_lists = [list(zip(*zipped)) for zipped in self._lists]
        for index_u, unzipped in enumerate(unzipped_lists):
            for index, sub_list in enumerate(unzipped):
                unzipped[index] = list(sub_list)
            unzipped_lists[index_u] = tuple(unzipped)
        return tuple(unzipped_lists)

    def flatten_list(self) -> tuple:
        """Returns a list of flattened lists.
        """
        flattened_lists = list()
        for sub_list in self._lists:
            flat_sub_lists = [value for tup in sub_list for value in tup]
            flattened_lists.append(flat_sub_lists)
        return tuple(flattened_lists)

    def delete_all_instances(self, value: any,
                             index: list[int, int] | None = None) -> None:
        """Removes all instances of value from one or more lists. THIS
        MODIFIES THE INPUTTED LISTS.
        """
        if index is None:
            for sub_list in self._lists:
                for index, list_value in enumerate(sub_list):
                    if list_value == value:
                        del sub_list[index]

        elif (type(index) == list and 1 <= len(index) <= 2 and
              any(type(val) == int for val in index)) and index[0] <= index[1]:
            sel_lists = self._lists[index[0]:index[1]]
            for sub_list in sel_lists:
                for index, list_value in enumerate(sub_list):
                    if list_value == value:
                        del sub_list[index]

        else:
            raise ValueError(f"Index is not valid, should be list[int, "
                             f"int] or none, {index=}, {type(index)=}")

    def display_lists(self) -> None:
        """Prints the lists given to the instance of ListUtils.

        Precondition:
            All lists given have values within them that have a __str__
            implementation.
        """
        print(f"<{', '.join([str(value) for value in self._lists])}>")

    def get_lists(self,
                  index: list[int, int] | int | None) -> tuple[list,
                    ...] | list:
        if index is None:
            return tuple(self._lists)
        elif (type(index) == list and len(index) == 2 and
              0 <= index[0] < index[1] <= len(self._lists) + 1):
            if abs(index[0] - index[1]) == 1:
                return self._lists[index[0]:index[1]][0]
            return tuple(self._lists[index[0]:index[1]])
        elif type(index) == int and 0 <= index <= len(self._lists) + 1:
            return self._lists[index]
        else:
            raise ValueError(f"index is not valid, must be type list or int. "
                             f"If index is a list it must have a range of "
                             f"[0, len(*lists) + 1], {index=}, {type(index)=}")


if __name__ == '__main__':
    # print(ListUtils([(1, 6), (2, 7), (3, 8), (4, 9), (5, 0)],
    #                 [(11, 16), (12, 17), (13, 18), (14, 19), (15, 10)]
    #                 ).unzip_columns())
    bleh = ListUtils(list(range(15)), list(range(10)))
    print(bleh.__repr__())
    print(bleh)
    bleh.delete_all_instances(10)
    print(bleh)
    bleh.display_lists()
    print(bleh.get_lists(None))
    print(bleh.get_lists([0, 1]))
    print(bleh.get_lists([0, 2]))
    print(bleh.get_lists(0))
