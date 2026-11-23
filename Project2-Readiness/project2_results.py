"""Reproduce the saved classroom results. Run: python project2_results.py"""
import json
from pathlib import Path

from portfolio import (covariance_matrix, equal_weights, expected_return,
                       inverse_volatility_weights, portfolio_volatility,
                       reserve_weight, estimate_from_csv, search_portfolio)

ROOT = Path(__file__).resolve().parent


def pack(weights, sleeves, correlations, objective, minimum):
    if weights is None:
        return {"verdict": "FAIL: no feasible allocation"}
    ret = expected_return(weights, sleeves)
    reserve = reserve_weight(weights, (3,))
    failures = []
    if ret < objective - 1e-12:
        failures.append("return objective")
    if reserve < minimum - 1e-12:
        failures.append("reserve minimum")
    return {"weights": dict(zip((s["name"] for s in sleeves), weights)),
            "expected_return_net": ret,
            "volatility": portfolio_volatility(weights, covariance_matrix(sleeves, correlations)),
            "reserve": reserve, "modeled_checks": "FAIL: " + ", ".join(failures) if failures else "PASS"}


def main():
    data = ROOT / "prices.csv"
    sleeves, corr = estimate_from_csv(data)
    recent, recent_corr = estimate_from_csv(data, last_36=True)
    baseline = search_portfolio(sleeves, corr, .065, .05, (3,))
    stress_estimates = [dict(s) for s in sleeves]
    stress_estimates[3]["return"] -= .01
    net = [{**s, "return": s["return"] - .01} for s in sleeves]
    scenarios = {
        "equal_weight": pack(equal_weights(sleeves), sleeves, corr, .065, .05),
        "inverse_volatility": pack(inverse_volatility_weights(sleeves), sleeves, corr, .065, .05),
        "meridian_benchmark_proxy_60_vti_40_bnd": pack([0, .6, .4, 0], sleeves, corr, .065, .05),
        "constrained": pack(baseline["weights"] if baseline else None, sleeves, corr, .065, .05),
    }
    for name, s, c, minimum in [("last_36_returns", recent, recent_corr, .05),
                                ("sgov_return_minus_1pp", stress_estimates, corr, .05),
                                ("annual_cost_1pct", net, corr, .05),
                                ("reserve_minimum_95pct", sleeves, corr, .95)]:
        result = search_portfolio(s, c, .065, minimum, (3,))
        scenarios[name] = pack(result["weights"] if result else None, s, c, .065, minimum)
    out = {"data_through": "2026-09-30", "downloaded_utc": "2026-10-22",
           "objective_annual": .065, "reserve_minimum": .05, "scenarios": scenarios}
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
