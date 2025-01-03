from __future__ import annotations

import sys
from typing import Literal, Optional, cast

import numpy as np
from numpy.polynomial import Polynomial
from numpy.typing import NDArray


def fit(x: list[float], y: list[float], degrees: int) -> Polynomial:
    return cast(Polynomial, Polynomial.fit(x, y, degrees))  # pyright: ignore [reportUnknownMemberType]


def get_domain(poly: Polynomial) -> Optional[list[np.float64]]:
    return cast(Optional[list[np.float64]], poly.domain)


def evaluate(poly: Polynomial, x: float | np.float64) -> np.float64:
    return cast(np.float64, poly(x))


def array2string(arr: NDArray[np.float64]) -> str:
    return np.array2string(
        arr, separator=",", floatmode="unique", threshold=sys.maxsize
    ).strip("[]")


def to_strings(poly: Polynomial) -> dict[Literal["coefficients", "domain"], str]:
    coef = cast(NDArray[np.float64], poly.coef)
    domain = cast(Optional[NDArray[np.float64]], poly.domain)
    if domain is None:
        raise ValueError("Polynomial domain is None")
    coef_str = array2string(coef)
    domain_str = array2string(domain)
    return {"coefficients": coef_str, "domain": domain_str}
