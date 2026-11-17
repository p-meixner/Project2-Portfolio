"""Lab 15 interface; all portfolio calculations live in portfolio.py."""

from hashlib import sha256
from io import BytesIO
from pathlib import Path

import pandas as pd
import streamlit as st

from portfolio import (CORRELATIONS, OBJECTIVE_RETURN, RESERVE_INDICES,
                       SLEEVES, estimate_from_csv, search_portfolio)

st.set_page_config(page_title="Portfolio Stability Decision", layout="wide")
st.title("Portfolio Stability Decision")
st.caption("Built with AI help, a learning demonstration, not investment advice.")

saved_example = st.sidebar.checkbox("Load Intel-related fund example", value=False)
objective = st.sidebar.number_input("Expected-return objective (%)", value=OBJECTIVE_RETURN * 100,
                                    step=0.1) / 100
minimum = st.sidebar.number_input("Reserve minimum (%)", min_value=0.0, max_value=100.0,
                                  value=5.0 if saved_example else 3.0, step=1.0,
                                  key=f"minimum_{saved_example}") / 100
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
        edited.append({**sleeve, "return": value / 100})
        if right.checkbox(f'{sleeve["name"]} reserve-eligible', value=i in default_reserves,
                          key=f"reserve_{dataset}_{i}"):
            eligible.append(i)

    baseline = search_portfolio(loaded, loaded_corr, objective, minimum, eligible)
    current = search_portfolio(edited, selected_corr, objective, minimum, eligible)
    st.caption("Both answers use the sidebar objective and the same reserve rule. "
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
except (ValueError, TypeError, OSError, pd.errors.ParserError) as error:
    st.error(f"Check your inputs: {error}")
