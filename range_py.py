"""
Alexander Bürow - 13 October 2023

License: GPL3
"""

import decimal


class Range:
    """
    Range(stop) -> iterator object
    Range(start, stop[, step]) -> iterator object

    Return an object that produces a sequence of floats from start (inclusive)
    to stop (exclusive) by step. range(i, j) produces i, i+1, i+2, ..., j-1.
    start defaults to 0, and stop is omitted! range(4) produces 0, 1, 2, 3.
    These are exactly the valid indices for a list of 4 elements.
    When step is given, it specifies the increment (or decrement).
    """

    def __init__(self, *args: float | int) -> None:
        """Initialises the Range object and sets the start, stop and step.

        Checks if the args inputted are valid. First if there are between 1 - 3
        args, then if the args are all floats or integers, and then finally
        if they make sense. Such as start not equalling stop or step not
        being 0.

        Parameters:
            args (float | int): Can be a minimum of one arg to a maximum of
                three args. The args can be either floats or integers. If one
                value is given it is taken as the "stop" (non-inclusive)
                with a "start" (inclusive) and "step" of 0 and 1 respectively.
                If two args are they are the "start" and "stop" in that
                order with a "step" of 1; Range(start, stop). If three args
                are given they are taken as "start", "stop" and "step";
                Range(start, stop, step).
        """
        self._validate_inputs(args)

        self.start = decimal.Decimal(args[0] if len(args) > 1 else 0)
        self.stop = decimal.Decimal(args[0] if len(args) == 1 else args[1])
        self.step = decimal.Decimal(args[2] if len(args) == 3 else 1)
        self.round_length = len(str(float(self.step))) - 2

    def __iter__(self):
        """Yields the next element in the sequence given by start+step, where
        start is the previous element in the sequence.
        """
        current = self.start
        while ((self.step > 0 and current < self.stop) or
               (self.step < 0 and current > self.stop)):
            yield round(float(current), self.round_length)
            current += self.step

    def __repr__(self) -> str:
        if self.step == 1.0 and self.start == 0.0:
            args = f"{round(self.stop, self.round_length)}"
        elif self.step == 1.0:
            args = (f"{round(self.start, self.round_length)}, "
                    f"{round(self.stop, self.round_length)}")
        else:
            args = (f"{round(self.start, self.round_length)}, "
                    f"{round(self.stop, self.round_length)}, "
                    f"{round(self.step, self.round_length)}")
        return f"{self.__class__.__name__}({args})"

    @staticmethod
    def _validate_inputs(inputs: tuple) -> None:
        """Checks if inputs are valid for the Range class initialisation.
        Parameters:
            inputs (tuple): The args inputted into the Range class.
        """
        condition = len(inputs)
        if condition not in range(1, 4):
            raise ValueError(f"Invalid amount of arguments (use 1 - 3),"
                             f" {inputs}")

        var_names = (["start", "stop", "step"][:condition]
                     if condition > 1 else ["stop"])

        for index, u_in in enumerate(inputs):
            if not isinstance(u_in, (int, float)):
                var_name = var_names[index]
                raise ValueError(f"{var_name} is not type int or "
                                 f"float, type({var_name})={type(u_in)}, "
                                 f"start={u_in}")
        if ((condition == 1 and inputs[0] == 0) or
                (condition > 1 and inputs[0] == inputs[1])):
            raise ValueError("start cannot equal stop.")
        if condition > 2 and inputs[2] == int():
            raise ValueError("step cannot equal 0.")
        if condition == 3 and (
                (inputs[0] < inputs[1] and inputs[2] < 0) or
                (inputs[0] > inputs[1] and inputs[2] > 0)
        ):
            value = ">0" if inputs[0] < inputs[1] and inputs[2] < 0 else "<0"
            raise ValueError(f"Invalid conditions, step must be {value} given "
                             f"the start ({inputs[0]}) and stop ({inputs[1]}).")

