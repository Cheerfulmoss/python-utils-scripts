"""
Alexander Bürow - 13 October 2023

License: GPL3
"""


from __future__ import annotations


class DictUtils:
    def __init__(self, dictionary: dict):
        self._dict = dictionary

    def add_key_value_list(self, key_val: list[tuple[any, any], ...],
                      condition: int) -> None:
        """Adds a list key/value pair to the dictionary.

        :param key_val: The key/value pairs to add to the dictionary.
        :param condition: What to do with the key/value. Condition 0 means to
            add it to the dictionary and raise an error if the key already
            exists. 1 means overwrite if already there. 2 means to skip if
            already there. 3 means to append to a list (assumes that - if a
            value already exists - it is a list, otherwise throws an error).
            4 is the same as 3 but if it is not a list it will be converted
            to a list (directly if it's a tuple and added to the 0th value of a
            list if it's a single value). Condition 4 does not convert every
            value in the dictionary to a list, only the ones you change.
        """
        match condition:
            case 0:
                for key, value in key_val:
                    if key in self._dict:
                        raise ValueError(f"key already in dict, {key=}, "
                                         f"{type(key)=}")
                    self._dict[key] = value
            case 1:
                for key, value in key_val:
                    self._dict[key] = value
            case 2:
                for key, value in key_val:
                    if key in self._dict:
                        continue
                    self._dict[key] = value
            case 3:
                for key, value in key_val:
                    if key in self._dict:
                        if type(self._dict[key]) != list:
                            value = self._dict[key]
                            raise ValueError(f"dictionary contains a value "
                                             f"that is not a list, this does "
                                             f"not work for {condition=}, "
                                             f"{value=}")
                        self._dict[key].append(value)
                    else:
                        self._dict[key] = [value]
            case 4:
                for key, value in key_val:
                    if key in self._dict:
                        current_val = self._dict[key]
                        if type(current_val) != list:
                            if (hasattr(current_val, "__len__") and
                                    type(current_val) != str):
                                self._dict[key] = list(current_val)
                            else:
                                self._dict[key] = [current_val, value]
                        else:
                            self._dict[key].append(value)
            case _:
                raise ValueError(f"Not a valid condition, {condition=}, "
                                 f"{type(condition)=}")

    def add_key_value(self, key: any, value: any, condition: int):
        """Adds a key/value pair to the dictionary.

        :param key: The key you want to modify or add to.
        :param value: The value you want to put in.
        :param condition: What to do with the key/value. Condition 0 means to
            add it to the dictionary and raise an error if the key already
            exists. 1 means overwrite if already there. 2 means to skip if
            already there. 3 means to append to a list (assumes that - if a
            value already exists - it is a list, otherwise throws an error).
            4 is the same as 3 but if it is not a list it will be converted
            to a list (directly if it's a tuple and added to the 0th value of a
            list if it's a single value). Condition 4 does not convert every
            value in the dictionary to a list, only the ones you change.
        """
        self.add_key_value_list([(key, value)], condition)


if __name__ == "__main__":
    dict_1 = {"a": 1, "b": 2, "c": 3}
    print(dict_1)
    obj = DictUtils(dict_1)
    obj.add_key_value_list([("d", 4), ("c", 6)], 4)
    obj.add_key_value("a", 8, 1)
    print(dict_1)
