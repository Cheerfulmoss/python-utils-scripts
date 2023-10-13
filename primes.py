"""
Alexander Bürow - 13 October 2023

License: GPL3
"""

from __future__ import annotations
from time import perf_counter_ns
import time
import plotly.graph_objs as go


class Primes:
    def __init__(self, index: int):
        self._check_inputs(index)
        self._index = index

        self._prime = (2 if self._index == 1 else self.prime_index(index))

    def __str__(self):
        return f"{self.__repr__()} = {self._prime}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self._index})"

    def __mul__(self, other):
        if type(other) in [float, int, complex]:
            return self.get_prime() * other
        elif type(other) == Primes:
            return self.get_prime() * other.get_prime()
        else:
            raise ValueError(f"Cannot multiply Primes by {type(other)}")

    def __add__(self, other):
        if type(other) in [float, int, complex]:
            return self.get_prime() + other
        elif type(other) == Primes:
            return self.get_prime() + other.get_prime()
        else:
            raise ValueError(f"Cannot add Primes with {type(other)}")

    @staticmethod
    def _check_inputs(inputs) -> None:
        if type(inputs) != int:
            raise ValueError(f"index is not an int, {inputs}, {type(inputs)}")

        if inputs <= 0:
            raise ValueError(f"Cannot index past 1")

    @staticmethod
    def prime_factors(number: int) -> list[int]:
        if type(number) != int:
            raise ValueError(f"number must be an int, "
                             f"{type(number)=}, "
                             f"{number=}")

        factors = []
        if is_prime(number):
            factors.append(number)
            return factors

        for quotient in p_range(number // 2 + 1):
            while number % quotient == 0:
                number /= quotient
                factors.append(quotient)
        return factors

    def prime_index(self, index: int) -> int:
        """Gets a prime by index.

        Precondtions:
            index > 1
        """
        number = 1
        count = 2
        while count <= index:
            number += 2
            if self._is_prime(number):
                count += 1
        return number

    @staticmethod
    def _is_prime(number: int):
        """Checks if a number is prime.

        Precondtitions:
            number is greater than 2
        """
        highest_factor = int(number * 0.5) + 1

        for divisor in range(3, highest_factor, 2):
            if number % divisor == 0:
                return False
        return True

    def get_prime(self):
        return self._prime

    def get_index(self):
        return self._index


class p_range:
    def __init__(self, *args: int) -> None:
        self.start = args[0] if len(args) > 1 else 0
        self.stop = args[0] if len(args) == 1 else args[1]
        self.step = args[2] if len(args) == 3 else 1
        self._MAX_ITERS = 10000

    def __iter__(self):
        current = self.start
        count = 0
        p_current = prime_index(current)
        while True and count < self._MAX_ITERS:
            while not is_prime(p_current):
                p_current += 2
            if p_current < self.stop:
                yield p_current
                if p_current & 1:
                    p_current += 2
                else:
                    p_current += 1
            else:
                break
            count += 1


def is_prime(number: int) -> bool:
    """Checks if a number is prime and returns a bool.
    Parameters:
        number (int): The number you want to check.

    Returns:
        True if prime, false if composite.
    """
    if not (number & 1) and number != 2:
        return False

    highest_factor = int(number * 0.5) + 1

    for divisor in range(3, highest_factor, 2):
        if number % divisor == 0:
            return False
    return True


def prime_index(index: int) -> int:
    """Gets a prime by index.
    """
    if index == 0:
        return 2
    number = 1
    count = 1
    while count <= index:
        number += 2
        if is_prime(number):
            count += 1
    return number


if __name__ == '__main__':

    prime_factors = dict()

    max_process_time = ((int(input(f"Max processing time (seconds): ")) *
                         1 * 10 ** 9))

    with open("output.txt", "w") as oput:
        sum = 0
        count = 0
        p_start = perf_counter_ns()
        process_time = 0
        while process_time < max_process_time:
            start = perf_counter_ns()
            factors = Primes.prime_factors(count + 1)
            end = perf_counter_ns() - start

            for factor in factors:
                if factor in prime_factors:
                    prime_factors[factor] += 1
                else:
                    prime_factors[factor] = 1

            print(
                f"{count + 1} : {', '.join(str(j) for j in factors)} : {end} ns")
            oput.write(
                f"{count + 1} : {', '.join(str(j) for j in factors)} : {end} "
                f"ns\n")

            process_time = perf_counter_ns() - p_start
            sum += end
            count += 1

        oput.write(f"\nTotal: {sum} ns, Avg: {sum/count} ns")

        fig = go.Figure(
            data=go.Scatter(x=list(prime_factors.keys()),
                            y=list(prime_factors.values()),
                            mode="markers")
        )

        fig.update_xaxes(type="log")
        fig.show()



