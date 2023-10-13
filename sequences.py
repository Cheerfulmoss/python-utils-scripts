"""
Alexander Bürow - 13 October 2023

License: GPL3
"""

import decimal
from typing import Callable
from decimal import Decimal
from time import time, perf_counter_ns
import numpy as np
import plotly.graph_objects as go


class MSequence:
    def __init__(self, func: Callable, i_values: list[Decimal],
                 recursive: bool = True) -> None:
        # self._EPSILON = Decimal(1 * 10 ** -10)
        self._EPSILON = Decimal(1 * 10 ** -7)
        self._MAX_ITERATIONS = 1000
        decimal.getcontext().prec = 100

        self._values = i_values
        self._func = func
        self._rec = recursive
        self._calc_time = (0,0)


    def run(self, *args):
        start_calc = (perf_counter_ns(), time())
        start = 0
        if self._rec and len(args) == 1:
            end = args[0]

        elif not self._rec and len(args) == 2:
            start = args[0]
            end = args[1]

        else:
            raise ValueError(f"No, read your own code butt head")

        if end is None:
            self._func(self._values)
            self._func(self._values)
            count = 2
            while (not (self._values[-2] - self._EPSILON <= self._values[-1]
                        <= self._values[-2] + self._EPSILON) and
                   count < self._MAX_ITERATIONS):
                self._func(self._values)
                count += 1
            self._func(self._values)

        else:
            for _ in range(start, end):
                self._func(self._values)

        self._calc_time = (perf_counter_ns() - start_calc[0],
                           round(time() - start_calc[1], 5))
        return self._values

    def analyse(self):
        if not self._values:
            return

        cluster_points = {}

        for value in self._values:
            for key in cluster_points:
                if key - self._EPSILON <= value <= key + self._EPSILON:
                    cluster_points[key] += 1
                    break
            else:
                cluster_points[value] = 1

        to_remove = list()

        for point, count in cluster_points.items():
            if count == 1:
                to_remove.append(point)

        for key in to_remove:
            cluster_points.pop(key)

        analysis_return = {
            "cluster points": cluster_points,
            "sequence length": len(self._values),
            "construction time ns": self._calc_time[0],
            "construction time s": self._calc_time[1],
        }

        return analysis_return

    def plot(self):
        if not self._values:
            return

        x_axis = [i for i in range(len(self._values))]

        fig = go.Figure(
            data=go.Scatter(x=x_axis, y=self._values, mode="markers")
        )

        fig.show()

    def mod_settings(self, **kwargs):
        old_vals = {
            "epsilon": self._EPSILON,
            "iterations": self._MAX_ITERATIONS,
            "precision": decimal.getcontext().prec,
        }

        if "precision" in kwargs:
            decimal.getcontext().prec = kwargs.get("precision")
        if "iterations" in kwargs:
            self._MAX_ITERATIONS = kwargs.get("iterations")
        if "epsilon" in kwargs:
            self._EPSILON = kwargs.get("epsilon")

        new_vals = {
            "epsilon": self._EPSILON,
            "iterations": self._MAX_ITERATIONS,
            "precision": decimal.getcontext().prec,
        }

        print(f"{old_vals} -> {new_vals}")


if __name__ == "__main__":
    func = lambda x: x.append(
        Decimal(2**(1+3*(len(x)+1)))**Decimal(1/(len(x)+1)))
    in_values = []
    seq = MSequence(func, in_values, True)
    seq.mod_settings(iterations=100)
    print(seq.run(None))
    print(seq.analyse())
    seq.plot()
