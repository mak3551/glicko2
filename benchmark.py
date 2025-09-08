from collections.abc import Callable
from datetime import date
from timeit import repeat
from typing import Any

from glicko2 import Glicko2, Glicko2Np, game_rate_calculate
from tests.test_game.test_game import _get_sample_data

BENCHMARK_NUMBER = 1000
REPEAT_NUMBER = 10


def get_sample() -> list[tuple[str | date, str, str, float]]:
    sample_data = _get_sample_data()
    return sample_data


def get_lambda_benchmark_glicko2() -> Callable[[], Any]:
    sample_data = get_sample()
    return lambda: game_rate_calculate(sample_data, per_days=60, rating_system=Glicko2())


def get_lambda_benchmark_glicko2np() -> Callable[[], Any]:
    sample_data = get_sample()
    return lambda: game_rate_calculate(sample_data, per_days=60, rating_system=Glicko2Np())


def benchmark() -> None:
    print(
        "Glicko2Np: ",
        min(repeat(get_lambda_benchmark_glicko2np(), number=BENCHMARK_NUMBER, repeat=REPEAT_NUMBER)),
    )
    print(
        "Glicko2: ",
        min(repeat(get_lambda_benchmark_glicko2(), number=BENCHMARK_NUMBER, repeat=REPEAT_NUMBER)),
    )


if __name__ == "__main__":
    benchmark()
