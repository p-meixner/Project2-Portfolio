"""Lab 15 interface; all portfolio calculations live in portfolio.py."""

from hashlib import sha256
from io import BytesIO
from pathlib import Path

import pandas as pd
import streamlit as st

from portfolio import (CORRELATIONS, OBJECTIVE_RETURN, RESERVE_INDICES,
                       SLEEVES, covariance_matrix, equal_weights, expected_return,
                       inverse_volatility_weights, portfolio_volatility, reserve_weight,
                       estimate_from_csv, search_portfolio)

st.set_page_config(page_title="Portfolio Stability Decision", layout="wide")
st.title("Portfolio Stability Decision")
st.caption("Built with OpenAI Codex for coding and analysis; the student must review and own the analysis and decision. Education, not investment advice.")

saved_example = st.sidebar.checkbox("Load Intel-related fund example", value=False)
objective = st.sidebar.number_input("Expected-return objective (%)", value=OBJECTIVE_RETURN * 100,
                                    step=0.1) / 100
minimum = st.sidebar.number_input("Reserve minimum (%)", min_value=0.0, max_value=100.0,
                                  value=5.0 if saved_example else 3.0, step=1.0,
                                  key=f"minimum_{saved_example}") / 100
cost = st.sidebar.number_input("Annual cost assumption (%)", min_value=0.0, max_value=10.0,
                               value=0.0, step=0.1, help="Illustrative uniform annual drag, not a transaction-cost model.") / 100
upload = st.sidebar.file_uploader("Upload prices.csv", type=["csv"])
recent = st.sidebar.checkbox("Use last 36 months", disabled=upload is None and not saved_example)
st.sidebar.caption("CSV: date first, oldest first; 3–6 tickers of monthly adjusted close prices.")

try:
    if upload is None and not saved_example:
        loaded, loaded_corr = SLEEVES, CORRELATIONS
        selected, selected_corr = loaded, loaded_corr
        dataset = "meridian"
        default_reserves = RESERVE_INDICES
        st.write("Meridian · course-authored training estimates")
    else:
        if upload is not None:
            data = upload.getvalue()
        else:
            data = Path(__file__).with_name("prices.csv").read_bytes()
            st.info("Intel-related fund example: SOXX / VTI / BND / SGOV. "
                    "Proposed classroom mandate: 6.5% expected return, at least 5% SGOV. "
                    "This is not Intel's corporate investment policy. See Lab15.md for sources.")
        dataset = sha256(data).hexdigest()
        loaded, loaded_corr = estimate_from_csv(BytesIO(data))
        selected, selected_corr = estimate_from_csv(BytesIO(data), last_36=recent)
        default_reserves = tuple(i for i, s in enumerate(loaded) if s["name"] == "SGOV") if upload is None else ()
        st.write("Historical arithmetic return estimates, not forecasts: monthly mean × 12.")
        st.caption("Volatility: sample monthly standard deviation × √12. Correlations use the same months. "
                   "Last 36 uses 36 returns (37 prices). Select eligible reserves or set the minimum to 0.")

    edited = []
    eligible = []
    st.subheader("Estimates and reserve eligibility")
    for i, sleeve in enumerate(selected):
        left, right = st.columns([3, 2])
        value = left.number_input(f'{sleeve["name"]} expected return (%)',
                                  value=sleeve["return"] * 100, step=0.1, format="%.2f",
                                  key=f"return_{dataset}_{recent}_{i}")
        edited.append({**sleeve, "return": value / 100 - cost})
        if right.checkbox(f'{sleeve["name"]} reserve-eligible', value=i in default_reserves,
                          key=f"reserve_{dataset}_{i}"):
            eligible.append(i)

    loaded_net = [{**s, "return": s["return"] - cost} for s in loaded]
    baseline = search_portfolio(loaded_net, loaded_corr, objective, minimum, eligible)
    current = search_portfolio(edited, selected_corr, objective, minimum, eligible)
    st.caption("Both answers use the sidebar objective, cost assumption, and the same reserve rule. "
               "As loaded always uses original returns and all CSV months. Search uses 5-point steps.")
    for column, heading, result in zip(st.columns(2),
                                      ["As loaded · all months", "Current inputs"],
                                      [baseline, current]):
        with column:
            st.subheader(heading)
            if result is None:
                st.warning("no mix meets the objective")
            else:
                st.dataframe(pd.DataFrame({"Asset": [s["name"] for s in loaded],
                                           "Weight (%)": [f"{w * 100:.2f}" for w in result["weights"]]}),
                             hide_index=True)
                st.metric("Expected return", f'{result["return"]:.2%}')
                st.metric("Volatility", f'{result["volatility"]:.2%}')
                st.metric("Reserve-eligible weight", f'{result["reserve"]:.2%}')
    if baseline is not None and current is not None:
        change = max(abs(a - b) for a, b in zip(baseline["weights"], current["weights"])) * 100
        st.metric("Largest weight change (percentage points)", f"{change:.2f}")
    else:
        st.info("Largest weight change unavailable: both inputs must have a feasible mix.")

    st.subheader("Baselines and modeled mandate checks")
    st.caption("Pass means these modeled checks only: fully invested, long-only, expected return after the assumed cost at least the objective, and eligible reserves at least the minimum. It is not full mandate compliance.")
    cov = covariance_matrix(edited, selected_corr)
    rows = []
    candidates = [("Equal weight", equal_weights(edited)),
                  ("Inverse volatility", inverse_volatility_weights(edited))]
    if dataset != "meridian" and [s["name"] for s in edited] == ["SOXX", "VTI", "BND", "SGOV"]:
        candidates.append(("60/40 VTI/BND proxy", [0.0, 0.6, 0.4, 0.0]))
    candidates.append(("Constrained minimum volatility", current["weights"] if current else None))
    for name, weights in candidates:
        if weights is None:
            rows.append({"Portfolio": name, "Weights": "—", "Return net (%)": "—", "Volatility (%)": "—", "Reserve (%)": "—", "Verdict": "FAIL: no feasible allocation"})
            continue
        ret = expected_return(weights, edited)
        vol = portfolio_volatility(weights, cov)
        reserve = reserve_weight(weights, eligible)
        failures = []
        if ret < objective - 1e-12:
            failures.append("return objective")
        if reserve < minimum - 1e-12:
            failures.append("reserve minimum")
        rows.append({"Portfolio": name,
                     "Weights": ", ".join(f'{s["name"]} {w:.1%}' for s, w in zip(edited, weights)),
                     "Return net (%)": f"{ret * 100:.2f}", "Volatility (%)": f"{vol * 100:.2f}",
                     "Reserve (%)": f"{reserve * 100:.2f}",
                     "Verdict": "FAIL: " + ", ".join(failures) if failures else "PASS: modeled checks"})
    st.dataframe(pd.DataFrame(rows), hide_index=True)
    st.caption("When shown, the 60/40 VTI/BND mix is a US-fund proxy for Meridian's 60% global equity / 40% US investment-grade bonds benchmark; it is not an exact global benchmark. It has no eligible SGOV reserve under this example's reserve rule.")
    st.caption("Volatility is annualized estimated standard deviation, not a loss guarantee. No maximum volatility was supplied for this classroom example. Issuer exposure, underlying ETF holdings, turnover, trading execution, taxes, liquidity under stress, and future calendar-year loss are not certified.")
    st.subheader("Point-in-time context: 10-year Treasury yield")
    st.write("As of September 30, 2026, the latest DGS10 observation in the saved ALFRED vintage was September 29: **5.26% per year**. This is a contextual rate signal; it does not change portfolio weights or prove predictive value.")
    st.caption("Source: Federal Reserve H.15 via FRED/ALFRED; vintage checked October 29, 2026. Vintage dates do not establish intraday availability. See Lab17.md and Lab17-validation.json for the data card and audit.")
    st.subheader("Stop condition")
    st.write("Do not adopt a mix that fails the modeled return or reserve rules, has no feasible solution, or relies on unjustified return estimates. The prior SGOV estimate stress moved weights by 10 percentage points, exceeding the proposed 5-point stability tolerance; do not treat the current historical optimization as ready for adoption.")
except (ValueError, TypeError, OSError, pd.errors.ParserError) as error:
    st.error(f"Check your inputs: {error}")
