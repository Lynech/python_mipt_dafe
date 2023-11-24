from typing import Iterable, Union
from numbers import Real

from regressors.regressor_abc import RegressorABC


class RegressorLSM(RegressorABC):
    def fit(self, abscissa: Iterable, ordinates: Iterable) -> None:
        self._abscissa = abscissa
        self._ordinates = ordinates
        # ваш код
        pass

    def average(self):
        self._ax = sum(self._abscissa) / len(self._abscissa)
        self._ay = sum(self._ordinates) / len(self._ordinates)
        self._axy = sum(x[0] * x[1] for x in zip(self._abscissa, self._ordinates))
        self._axx = sum(x**2 for x in self._abscissa)
        pass

    def predict(self, abscissa: Union[Real, Iterable]) -> list:
        prediction = []
        self.average()
        k = (self._axy - self._ax * self._ay) / (self._axx - self._ax**2)
        b = self._ay - k * self._ax
        for x in abscissa:
            prediction.append(b + k * x)
        return prediction
        # ваш код
        return [abscissa] if isinstance(abscissa, Real) else abscissa
