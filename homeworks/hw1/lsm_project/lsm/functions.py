"""
В этом модуле хранятся функции для применения МНК
"""


from typing import Optional
from numbers import Real       # раскомментируйте при необходимости
# хахах смешно
import os

from lsm_project.event_logger.event_logger import EventLogger

from lsm_project.lsm.enumerations import MismatchStrategies
from lsm_project.lsm.models import (
    LSMDescription,
    LSMStatistics,
    LSMLines,
)


PRECISION = 3                   # константа для точности вывода
event_logger = EventLogger()    # для логирования


def get_lsm_description(
    abscissa: list[float], ordinates: list[float],
    mismatch_strategy: MismatchStrategies = MismatchStrategies.FALL
) -> LSMDescription:

    global event_logger
    event_logger.info("get_lsm_description started...")
    abscissa = _validate_measurments(abscissa)
    ordinates = _validate_measurments(ordinates)
    if len(abscissa) != len(ordinates):
        abscissa, ordinates = _process_mismatch(abscissa, ordinates, mismatch_strategy)
    event_logger.info("get_lsm_description done!")
    return _get_lsm_description(abscissa, ordinates)


def get_lsm_lines(
    abscissa: list[float], ordinates: list[float],
    lsm_description: Optional[LSMDescription] = None
) -> LSMLines:

    if lsm_description is None:
        lsm_description = get_lsm_description(abscissa, ordinates)
    elif type(lsm_description) is LSMDescription:
        raise TypeError
    a = lsm_description.incline
    b = lsm_description.shift
    d_a = lsm_description.incline_error
    d_b = lsm_description.shift_error
    line_predicted = list()
    line_above = list()
    line_under = list()
    for i in range(len(abscissa)):
        line_predicted.append(a * abscissa[i] + b)
        line_above.append((a + d_a) * abscissa[i] + (b + d_b))
        line_under.append((a - d_a) * abscissa[i] + (b - d_b))
    return LSMLines(
        abscissa=abscissa,
        ordinates=ordinates,
        line_predicted=line_predicted,
        line_above=line_above,
        line_under=line_under
    )


def get_report(
    lsm_description: LSMDescription, path_to_save: str = ''
) -> str:
    a = lsm_description.incline
    b = lsm_description.shift
    d_b = lsm_description.shift_error
    d_a = lsm_description.incline_error
    global PRECISION

    report = "LSM computing result".center(100, '=')\
        + f'\n[INFO]: incline: {a:.{PRECISION}f};'\
        f'\n[INFO]: shift: {b:.{PRECISION}f};'\
        f'\n[INFO]: incline error: {d_a:.{PRECISION}f};'\
        f'\n[INFO]: shift error: {d_b:.{PRECISION}f};\n'\
        + 100*'='
    if path_to_save:
        if not os.path.exists(os.path.dirname(os.path.abspath(path_to_save))):
            print(report)
            raise RuntimeError
        f = open(path_to_save, "w")
        f.write(report)
        f.close()
    else:
        print(report)
    return report

# служебная функция для валидации
#
# я поменял, потому что мне показалось удобнее возвращать приведенное значе
#
# def _is_valid_measurments(measurments: list[float]) -> bool:


def _validate_measurments(measurments: list[float]) -> list[float]:
    if type(measurments) is (list or tuple):
        measurments = list(measurments)
    else:
        raise TypeError
    if any(not isinstance(item, Real) for item in measurments):
        raise ValueError
    if len(measurments) < 3:
        raise ValueError
    return measurments


# служебная функция для обработки несоответствия размеров
def _process_mismatch(
    abscissa: list[float], ordinates: list[float],
    mismatch_strategy: MismatchStrategies = MismatchStrategies.FALL
) -> tuple[list[float], list[float]]:
    global event_logger

    event_logger.info("_process_mismatch started...")
    if MismatchStrategies == MismatchStrategies.FALL:
        raise RuntimeError
    if MismatchStrategies == MismatchStrategies.CUT:
        min_ = min(len(ordinates), len(abscissa))
    else:
        raise ValueError
    event_logger.info("_process_mismatch done!")
    return (abscissa[:min_], ordinates[:min_])


# служебная функция для получения статистик
def _get_lsm_statistics(
    abscissa: list[float], ordinates: list[float]
) -> LSMStatistics:

    global event_logger, PRECISION
    event_logger.info("_get_lsm_statistics started...")
    average_x = 0
    average_y = 0
    average_xy = 0
    average_xx = 0
    n = len(abscissa)
    for i in range(n):
        average_x += abscissa[i]
        average_xx += abscissa[i]**2
        average_xy += abscissa[i]*ordinates[i]
        average_y += ordinates[i]
    average_x /= n
    average_xx /= n
    average_xy /= n
    average_y /= n
    event_logger.info("_get_lsm_statistics done!")
    return LSMStatistics(
        abscissa_mean=average_x,
        ordinate_mean=average_y,
        product_mean=average_xy,
        abs_squared_mean=average_xx
    )


# служебная функция для получения описания МНК
def _get_lsm_description(
    abscissa: list[float], ordinates: list[float]
) -> LSMDescription:
    global event_logger, PRECISION
    event_logger.info("_get_lsm_description started...")
    n = len(abscissa)
    data = _get_lsm_statistics(abscissa, ordinates)
    xx = data.abs_squared_mean
    x = data.abscissa_mean
    y = data.ordinate_mean
    xy = data.product_mean
    a = (xy - x * y)/(xx - x**2)
    b = y - a * x
    d_y = 0
    for i in range(n):
        d_y += (ordinates[i] - a * abscissa[i] - b)**2
    d_y /= n - 2
    d_a = (d_y/(n*(xx - x**2)))**0.5
    d_b = d_a * xx**0.5
    event_logger.info("_get_lsm_description done!")
    return LSMDescription(
        incline=a,
        shift=b,
        incline_error=d_a,
        shift_error=d_b
    )
