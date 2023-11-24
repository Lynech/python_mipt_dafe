from typing import Iterable, Union
from numbers import Real

from regressors.regressor_abc import RegressorABC


class NonparametricRegressor(RegressorABC):
    def __init__(self, k_neighbour) -> None:
        if k_neighbour <= 0:
            raise ValueError("Invalid k_neighbour value")
        self.__k_neighbour = k_neighbour

    def fit(self, abscissa: Iterable, ordinates: Iterable) -> None:
        self._abscissa = abscissa
        self._ordinates = ordinates
        return
        # ваш код
        pass

    def predict(self, abscissa: Union[Real, Iterable]) -> list:
        prediction = []
        for x in abscissa:
            prediction.append(self._compute_prediction(self._compute_weights(x)))
        return prediction
        # ваш код
        return abscissa

    @staticmethod
    def __kernel(x):
        return 3 / 4 * (1 - x**2) if abs(x) <= 1 else 0

    def _compute_weights(self, x):
        distance = [abs(x - xi) for xi in self._abscissa]
        window_size = sorted(distance)[self.__k_neighbour - 1]
        distance_norm = [dist / window_size for dist in distance]

        return list(map(self.__kernel, distance_norm))

    def _compute_prediction(self, weights) -> list:
        values1 = sum(wi * yi for wi, yi in zip(weights, self._ordinates))
        return values1 / sum(weights)
