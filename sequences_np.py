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
from plotly.subplots import make_subplots


class MSequence:
    def __init__(self, func: Callable, i_values: np.ndarray,
                 recursive: bool = True) -> None:
        # self._EPSILON = Decimal(1 * 10 ** -10)
        self._EPSILON = Decimal(1 * 10 ** -6)
        self._MAX_ITERATIONS = 1000
        decimal.getcontext().prec = 100

        self._values = i_values
        self._func = func
        self._rec = recursive
        self._calc_time = (0, 0)

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
            self._values = np.append(self._values, [self._func(self._values)])
            self._values = np.append(self._values, [self._func(self._values)])
            count = 2
            while (not (self._values[-2] - self._EPSILON <= self._values[-1]
                        <= self._values[-2] + self._EPSILON) and
                   count + 1 < self._MAX_ITERATIONS):
                self._values = np.append(self._values,
                                         [self._func(self._values)])
                count += 1
            self._values = np.append(self._values, [self._func(self._values)])

        else:
            for _ in range(start, end):
                self._values = np.append(self._values,
                                         [self._func(self._values)])

        self._calc_time = (perf_counter_ns() - start_calc[0],
                           round(time() - start_calc[1], 5))
        return self._values

    def analyse(self):
        if not self._values.size:
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
        if not self._values.size:
            return

        x_axis = np.arange(len(self._values))

        # Create a scatter plot for the sequence using markers
        sequence_fig = go.Figure()
        sequence_fig.add_trace(
            go.Scatter(x=x_axis, y=self._values, mode="markers",
                       name="Sequence"))

        # Create a bar chart for the cluster points
        cluster_points = self.analyse()["cluster points"]
        unique_cluster_points = list(cluster_points.keys())
        cluster_fig = go.Figure()
        cluster_fig.add_trace(go.Bar(x=unique_cluster_points,
                                     y=list(cluster_points.values()),
                                     name="Cluster Points"))

        # Display subplots
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                            vertical_spacing=0.1)

        sequence_x_axis = np.arange(
            len(self._values))  # X-axis for sequence subplot
        cluster_x_axis = unique_cluster_points  # X-axis for cluster points subplot

        sequence_fig.data[0].x = sequence_x_axis
        cluster_fig.data[0].x = cluster_x_axis

        fig.add_trace(sequence_fig.data[0], row=1, col=1)
        fig.add_trace(cluster_fig.data[0], row=2, col=1)

        fig.update_layout(
            title="Generated Sequence and Cluster Points",
            xaxis_title="Term Index",
            hovermode="closest",
            showlegend=False
        )

        fig.update_yaxes(title_text="Value", row=1, col=1)
        fig.update_yaxes(title_text="Cluster Count", row=2, col=1)

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
    func = lambda x: Decimal(2 ** (1 + 3 * (len(x) + 1))) ** Decimal(
        1 / (len(x) + 1))
    # func = lambda x: Decimal(np.e**np.cos(len(x)))
    in_values = np.array([], dtype=Decimal)
    seq = MSequence(func, in_values, True)
    seq.mod_settings(iterations=1000, epsilon=Decimal(1 * 10 ** -5))
    print(seq.run(None))
    print(seq.analyse())
    seq.plot()
