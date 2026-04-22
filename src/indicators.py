from __future__ import annotations


def extract_closes(klines: list[dict]) -> list[float]:
    return [float(item["close"]) for item in klines]


def extract_highs(klines: list[dict]) -> list[float]:
    return [float(item["high"]) for item in klines]


def extract_lows(klines: list[dict]) -> list[float]:
    return [float(item["low"]) for item in klines]


def extract_volumes(klines: list[dict]) -> list[float]:
    return [float(item["volume"]) for item in klines]


def sma(values: list[float], period: int) -> list[float | None]:
    if period <= 0:
        raise ValueError("period must be greater than 0")

    if not values:
        return []

    result: list[float | None] = [None] * len(values)

    if len(values) < period:
        return result

    for i in range(period - 1, len(values)):
        window = values[i - period + 1 : i + 1]
        result[i] = sum(window) / period

    return result


def stddev(values: list[float], period: int) -> list[float | None]:
    if period <= 0:
        raise ValueError("period must be greater than 0")

    if not values:
        return []

    result: list[float | None] = [None] * len(values)

    if len(values) < period:
        return result

    for i in range(period - 1, len(values)):
        window = values[i - period + 1 : i + 1]
        mean = sum(window) / period
        variance = sum((value - mean) ** 2 for value in window) / period
        result[i] = variance ** 0.5

    return result


def bollinger_bands(
    closes: list[float],
    period: int,
    multiplier: float,
) -> tuple[list[float | None], list[float | None], list[float | None]]:
    middle = sma(closes, period)
    deviation = stddev(closes, period)

    upper: list[float | None] = [None] * len(closes)
    lower: list[float | None] = [None] * len(closes)

    for i in range(len(closes)):
        if middle[i] is None or deviation[i] is None:
            continue
        upper[i] = middle[i] + deviation[i] * multiplier
        lower[i] = middle[i] - deviation[i] * multiplier

    return upper, middle, lower


def rolling_vwap(klines: list[dict], period: int) -> list[float | None]:
    if period <= 0:
        raise ValueError("period must be greater than 0")

    if not klines:
        return []

    result: list[float | None] = [None] * len(klines)

    if len(klines) < period:
        return result

    typical_prices: list[float] = []
    volumes: list[float] = []

    for item in klines:
        high = float(item["high"])
        low = float(item["low"])
        close = float(item["close"])
        volume = float(item["volume"])
        typical_prices.append((high + low + close) / 3.0)
        volumes.append(volume)

    for i in range(period - 1, len(klines)):
        tp_window = typical_prices[i - period + 1 : i + 1]
        volume_window = volumes[i - period + 1 : i + 1]
        denominator = sum(volume_window)

        if denominator <= 0:
            continue

        result[i] = sum(tp * volume for tp, volume in zip(tp_window, volume_window)) / denominator

    return result


def ema(values: list[float], period: int) -> list[float | None]:
    if period <= 0:
        raise ValueError("period must be greater than 0")

    if not values:
        return []

    result: list[float | None] = [None] * len(values)

    if len(values) < period:
        return result

    sma = sum(values[:period]) / period
    result[period - 1] = sma

    multiplier = 2 / (period + 1)
    previous_ema = sma

    for i in range(period, len(values)):
        current_ema = ((values[i] - previous_ema) * multiplier) + previous_ema
        result[i] = current_ema
        previous_ema = current_ema

    return result


def rsi(closes: list[float], period: int = 14) -> list[float | None]:
    if period <= 0:
        raise ValueError("period must be greater than 0")

    if not closes:
        return []

    result: list[float | None] = [None] * len(closes)

    if len(closes) <= period:
        return result

    gains: list[float] = []
    losses: list[float] = []

    for i in range(1, period + 1):
        delta = closes[i] - closes[i - 1]
        gains.append(max(delta, 0.0))
        losses.append(max(-delta, 0.0))

    average_gain = sum(gains) / period
    average_loss = sum(losses) / period

    if average_loss == 0:
        result[period] = 100.0
    else:
        rs = average_gain / average_loss
        result[period] = 100.0 - (100.0 / (1.0 + rs))

    for i in range(period + 1, len(closes)):
        delta = closes[i] - closes[i - 1]
        gain = max(delta, 0.0)
        loss = max(-delta, 0.0)

        average_gain = ((average_gain * (period - 1)) + gain) / period
        average_loss = ((average_loss * (period - 1)) + loss) / period

        if average_loss == 0:
            result[i] = 100.0
        else:
            rs = average_gain / average_loss
            result[i] = 100.0 - (100.0 / (1.0 + rs))

    return result


def atr(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    period: int = 14,
) -> list[float | None]:
    if period <= 0:
        raise ValueError("period must be greater than 0")

    if not highs or not lows or not closes:
        return []

    if not (len(highs) == len(lows) == len(closes)):
        raise ValueError("highs, lows, closes must have the same length")

    length = len(closes)
    result: list[float | None] = [None] * length

    if length <= period:
        return result

    true_ranges: list[float] = [0.0]

    for i in range(1, length):
        high = highs[i]
        low = lows[i]
        previous_close = closes[i - 1]

        tr = max(
            high - low,
            abs(high - previous_close),
            abs(low - previous_close),
        )
        true_ranges.append(tr)

    initial_atr = sum(true_ranges[1 : period + 1]) / period
    result[period] = initial_atr

    previous_atr = initial_atr

    for i in range(period + 1, length):
        current_atr = ((previous_atr * (period - 1)) + true_ranges[i]) / period
        result[i] = current_atr
        previous_atr = current_atr

    return result
