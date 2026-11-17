"""Lab 14: Meridian portfolio baselines; standard library only.

Course-authored training inputs, not market estimates. Rates are decimals.
Run: python portfolio.py
"""

from math import isclose, isfinite, sqrt
from itertools import combinations


# Editable inputs, in the same order as the correlation rows and columns.
SLEEVES = [
    {"name": "Treasury bills", "return": 0.035, "volatility": 0.005},
    {"name": "Treasury 10-year note", "return": 0.043, "volatility": 0.07},
    {"name": "Investment-grade bond fund", "return": 0.05, "volatility": 0.06},
    {"name": "Global equity index fund", "return": 0.08, "volatility": 0.16},
]
CORRELATIONS = [
    [1.00, 0.10, 0.05, 0.00],
    [0.10, 1.00, 0.80, -0.10],
    [0.05, 0.80, 1.00, 0.25],
    [0.00, -0.10, 0.25, 1.00],
]
OBJECTIVE_RETURN = 0.065  # CPI estimate 2.5% + 4%; not a guarantee.
RESERVE_INDICES = (0, 1)  # Bills and 10-year government note.
BENCHMARK_WEIGHTS = [0.0, 0.0, 0.4, 0.6]


def validate_inputs(sleeves, correlations):
    """Reject malformed inputs before calculating any portfolio."""
    n = len(sleeves)
    if not n or len(correlations) != n or any(len(row) != n for row in correlations):
        raise ValueError("Correlation table must be square and match the sleeves.")
    for sleeve in sleeves:
        if not isfinite(sleeve["return"]):
            raise ValueError("Expected returns must be finite.")
        if not isfinite(sleeve["volatility"]) or sleeve["volatility"] <= 0:
            raise ValueError("Volatilities must be finite and positive.")
    for i in range(n):
        for j in range(n):
            value = correlations[i][j]
            if not isfinite(value) or not -1 <= value <= 1:
                raise ValueError(f"Correlation [{i}][{j}] must be between -1 and 1.")
            if not isclose(value, correlations[j][i], rel_tol=0, abs_tol=1e-12):
                raise ValueError(f"Correlation table is not symmetric at [{i}][{j}].")
        if not isclose(correlations[i][i], 1.0, rel_tol=0, abs_tol=1e-12):
            raise ValueError("Every diagonal correlation must equal 1.")


def covariance_matrix(sleeves, correlations):
    validate_inputs(sleeves, correlations)
    return [
        [correlations[i][j] * sleeves[i]["volatility"] * sleeves[j]["volatility"]
         for j in range(len(sleeves))]
        for i in range(len(sleeves))
    ]


def validate_weights(weights, size):
    if len(weights) != size or any(not isfinite(w) or w < 0 for w in weights):
        raise ValueError("Weights must match the sleeves and be finite and nonnegative.")
    if not isclose(sum(weights), 1.0, rel_tol=0, abs_tol=1e-10):
        raise ValueError("Weights must sum to 100%.")


def equal_weights(sleeves):
    return [1.0 / len(sleeves)] * len(sleeves)


def inverse_volatility_weights(sleeves):
    inverse = [1.0 / sleeve["volatility"] for sleeve in sleeves]
    return [value / sum(inverse) for value in inverse]


def expected_return(weights, sleeves):
    validate_weights(weights, len(sleeves))
    return sum(w * sleeve["return"] for w, sleeve in zip(weights, sleeves))


def portfolio_volatility(weights, covariance):
    validate_weights(weights, len(covariance))
    # Both (i, j) and (j, i) appear: this includes both cross terms.
    variance = sum(
        weights[i] * weights[j] * covariance[i][j]
        for i in range(len(weights))
        for j in range(len(weights))
    )
    if variance < -1e-12:
        raise ValueError("Negative portfolio variance; check the correlation inputs.")
    return sqrt(max(0.0, variance))


def reserve_weight(weights, eligible_indices=RESERVE_INDICES):
    return sum(weights[i] for i in eligible_indices)


def meets_objective(portfolio_return, objective=OBJECTIVE_RETURN):
    return portfolio_return >= objective


def search_portfolio(sleeves, correlations, objective=OBJECTIVE_RETURN,
                     reserve_minimum=0.03, eligible_indices=RESERVE_INDICES):
    """Find the lowest-volatility feasible long-only mix on a 5% grid."""
    covariance = covariance_matrix(sleeves, correlations)
    n = len(sleeves)
    if not 1 <= n <= 6:
        raise ValueError("Search supports one to six assets.")
    eligible_indices = tuple(set(eligible_indices))
    if any(i < 0 or i >= n for i in eligible_indices):
        raise ValueError("Reserve indices must refer to existing assets.")
    if not isfinite(objective) or not isfinite(reserve_minimum) or not 0 <= reserve_minimum <= 1:
        raise ValueError("Use a finite objective and a reserve minimum between 0 and 1.")
    best = None
    # Place n-1 dividers among 20 units: each unit represents 5%.
    # Gaps between dividers enumerate every allocation exactly once.
    for dividers in combinations(range(20 + n - 1), n - 1):
        edges = (-1,) + dividers + (20 + n - 1,)
        weights = [(edges[i + 1] - edges[i] - 1) / 20 for i in range(n)]
        result_return = expected_return(weights, sleeves)
        reserve = reserve_weight(weights, eligible_indices)
        if result_return < objective - 1e-12 or reserve < reserve_minimum - 1e-12:
            continue
        volatility = portfolio_volatility(weights, covariance)
        if best is None or volatility < best["volatility"]:
            best = {"weights": weights, "return": result_return,
                    "volatility": volatility, "reserve": reserve}
    return best


def estimate_from_csv(source, last_36=False):
    """Estimate annual inputs from complete monthly adjusted prices.

    Last 36 means 36 monthly returns, requiring 37 price observations.
    Arithmetic historical means are estimates, not forecasts.
    """
    import pandas as pd

    prices = pd.read_csv(source)
    if not 4 <= len(prices.columns) <= 7:
        raise ValueError("CSV needs a date column followed by three to six tickers.")
    dates = pd.to_datetime(prices.iloc[:, 0], errors="raise")
    if dates.isna().any() or not dates.is_monotonic_increasing:
        raise ValueError("Dates must be present and ordered oldest first.")
    months = dates.dt.to_period("M").astype("int64")
    if len(months) < 3 or not months.diff().iloc[1:].eq(1).all():
        raise ValueError("Provide consecutive monthly rows, without duplicates or gaps.")
    values = prices.iloc[:, 1:].apply(pd.to_numeric, errors="raise")
    if not all(isfinite(x) and x > 0 for x in values.to_numpy().flat):
        raise ValueError("Every adjusted price must be finite, positive, and present.")
    returns = values.pct_change(fill_method=None).iloc[1:]
    if last_36:
        if len(returns) < 36:
            raise ValueError("Last 36 months requires at least 37 monthly price rows.")
        returns = returns.tail(36)
    means = returns.mean() * 12
    volatilities = returns.std(ddof=1) * sqrt(12)
    sleeves = [{"name": name, "return": float(means[name]),
                "volatility": float(volatilities[name])} for name in values.columns]
    correlations = returns.corr().values.tolist()
    validate_inputs(sleeves, correlations)
    return sleeves, correlations


def main():
    covariance = covariance_matrix(SLEEVES, CORRELATIONS)
    portfolios = {
        "Benchmark": BENCHMARK_WEIGHTS,
        "Equal weight": equal_weights(SLEEVES),
        "Inverse volatility": inverse_volatility_weights(SLEEVES),
    }
    print("Meridian - course-authored training inputs, not market estimates")
    print(f"Objective: {OBJECTIVE_RETURN:.2%} (CPI estimate 2.5% + 4%)")
    print("Weight order: " + " / ".join(s["name"] for s in SLEEVES))
    for name, weights in portfolios.items():
        result = expected_return(weights, SLEEVES)
        print(f"\n{name}")
        print("Weights (%): " + " / ".join(f"{w * 100:.1f}" for w in weights))
        print(f"Expected return: {result:.2%}")
        print(f"Volatility: {portfolio_volatility(weights, covariance):.2%}")
        print(f"Reserve-eligible weight: {reserve_weight(weights):.1%}")
        print("Meets objective: " + ("yes" if meets_objective(result) else "no"))
    print("\nMeeting the expected-return objective is not full mandate compliance.")
    print("Displayed weights are rounded; calculations use unrounded weights.")


if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        raise SystemExit(f"Refusing to run: {error}") from error
