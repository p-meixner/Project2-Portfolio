# Project 2: Portfolio Stability Decision — working draft

Built with AI assistance for education, not investment advice.

This is a preliminary local assembly of Labs 13–17, not a completed Project 2 submission. The investor mandate and final decision still require student confirmation. See [Lab 20 record](Lab20.md) for unresolved work.

## Run

Install Python 3 and, from this folder, run `python -m pip install -r requirements-lab15.txt` once. Then run:

```sh
python -m streamlit run app.py
```

In the sidebar select **Load Intel-related fund example**. The app displays the proposed classroom mandate, weights, expected return, volatility, and reserve-eligible weight. Move a return control or select **Use last 36 months** to compare results. The search checks the expected-return objective and reserve minimum, not every mandate provision. The app defaults to the separate Meridian training example until the checkbox is selected.

## Visible prior results

For the proposed Intel-related classroom example, the saved October 2021–September 2026 sample and 6.50% expected-return objective with 5% minimum SGOV reserve produced 10% SOXX / 0% VTI / 0% BND / 90% SGOV, 6.81% expected return, 3.84% estimated volatility, and 90% reserves. These are historical estimates, not forecasts. See [Lab 15](Lab15.md) for the assumptions, alternative window, stress results, sources, and limitations. The proposed mandate and draft call in that file are AI-assisted and need student review.

## Status

The partner cold run, human-authored locked prediction, final decision memo, validation package, manifest, and video links remain unresolved. The point-in-time exercise in [Lab 17](Lab17.md) is a separate audit and does not establish that the fund price data are point-in-time clean. This folder has not yet been published to GitHub.
