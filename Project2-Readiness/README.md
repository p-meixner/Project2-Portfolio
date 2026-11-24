# Project 2: Portfolio Stability Decision

OpenAI Codex was used to develop and check code and draft analysis; the student must review and own the analysis and decision. This is education, not investment advice.

**Working recommendation for review: reject adoption of the current historical-estimate process.** A classroom-only pilot is conditional on credible forward estimates, a client-approved risk policy, and stress stability; it is not authorization to trade. The saved example uses a proposed classroom mandate, not Intel's corporate policy or the complete Meridian mandate. See the [decision memo](docs/decision-memo.md).

## Start the app

Install Python 3.10 or later, open a terminal in this folder, and install dependencies:

```sh
python -m pip install -r requirements-lab15.txt
```

Then run:

```sh
python -m streamlit run app.py
```

Select **Load Intel-related fund example**. The app shows the constrained result, equal-weight and inverse-volatility baselines with modeled rule verdicts, and point-in-time context. Change return estimates, the lookback window, annual cost drag, return objective, or reserve minimum to stress the process. If no mix passes the modeled constraints, the app reports no feasible allocation. Use `Ctrl+C` in the terminal to stop it. No API key is needed.

To reproduce the saved results without a browser, run `python project2_results.py`; the checked-in [output](project2-output.json) is visible without running code. The table below rounds those results.

## Visible results and scope

The saved adjusted-price sample uses 61 month-end observations from September 2021 to September 2026 (60 returns), downloaded October 22, 2026. Historical arithmetic means are estimates, not forward forecasts. The proposed classroom objective is 6.50% annual expected return after assumed costs; the grid is long-only and fully invested with at least 5% in SGOV. The base cost assumption is 0%, an unverified simplification. Annualized volatility is the risk measure; no defensible risk ceiling has been established. Weights below are SOXX / VTI / BND / SGOV.

| Case | Weights (%) | Expected return | Volatility | SGOV reserve | Modeled verdict |
|---|---|---:|---:|---:|---|
| Equal weight | 25 / 25 / 25 / 25 | 12.76% | 13.69% | 25.00% | Pass |
| Inverse volatility | 1.18 / 2.79 / 6.89 / 89.14 | 4.06% | 1.32% | 89.14% | Fail: return objective |
| 60/40 VTI/BND proxy | 0 / 60 / 40 / 0 | 7.71% | 11.38% | 0.00% | Fail: reserve minimum |
| Constrained minimum volatility | 10 / 0 / 0 / 90 | 6.81% | 3.84% | 90.00% | Pass |

These verdicts cover only fully invested, long-only, expected-return and reserve checks; they are **not** full mandate certification. The 60/40 proxy uses US equity and broad US bonds, so it does not exactly reproduce Meridian's global-equity/US-investment-grade benchmark. The [mandate reconciliation](docs/mandate-reconciliation.md) maps each Lab 13 constraint to the implemented checks and gaps. The 2026-09-30 ALFRED vintage supplies a separate DGS10 context signal, last observed 2026-09-29 at 5.26% per year; it is not an optimizer input. ETF price revisions, intraday availability, costs, underlying holdings, issuer concentration, and loss limits remain material limitations. See [validation and AI use](docs/validation-and-ai-use.md), [Lab 15](Lab15.md), and [Lab 17](Lab17.md).

The proposed 5-percentage-point stability tolerance is a classroom assumption, not a client-approved limit. The saved SGOV return stress moved an allocation weight by 10 points, exceeding it. The process stops for adoption when modeled constraints fail, no feasible allocation exists, inputs cannot be justified, or this proposed stability condition fails. A historical stress cannot establish future performance.

## Files and unfinished work

- [App](app.py), [portfolio engine](portfolio.py), [result generator](project2_results.py), [data](prices.csv), and [source download record](Lab15-data/sources.json).
- [Decision memo](docs/decision-memo.md), [validation and AI-use record](docs/validation-and-ai-use.md), [manifest](manifest.csv), and [Lab 20 record](Lab20.md).
- Three videos have been recorded and their links added to the manifest. Corrected transcripts, video timestamps and playback checks remain outstanding; confirm captions are available for all three. Student review and decision ownership are also required. The [AI-enhanced changed-input record](docs/validation-and-ai-use.md) is disclosed; it is not a human-authored AI-off record as specified in the published brief. The student reports instructor permission for AI assistance.
