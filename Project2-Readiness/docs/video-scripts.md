# Project 2 video scripts — drafts to review and personalize

These are recording scripts, not transcripts or proof of recordings. Review every statement and use only claims you understand and can support. If you record different words, correct each transcript to match your actual recording. Each recording needs the actual AI disclosure, your ownership statement if true, and the education disclaimer. Video 3 starts with the app running live. Keep Video 1 within 3 minutes and Videos 2 and 3 within 5 minutes each.

## Video 1 — how the system and thinking changed (maximum 3:00)

**Show:** Your repository README and, if available, your own earlier notes. Then show the Lab 20 record and its prediction commit.

**Say:** “I used OpenAI Codex to help write and check the code and draft the analysis. I have reviewed the analysis and the decision and take responsibility for them. This project is for education, not investment advice.” [Say the ownership sentence only after you have actually reviewed the work.]

“My project asks whether an investment committee should use a portfolio selection process that searches for a low-volatility allocation subject to an expected-return goal and a reserve requirement. The original Lab 13 Meridian case has a seven-year horizon, a CPI-plus-four-percent objective, and several liquidity and concentration constraints. I later explored a classroom fund universe of SOXX, VTI, BND and SGOV. That example is not Intel's corporate mandate and doesn't implement every Meridian rule.”

“The important change in the current draft is the decision: the model can produce an allocation that passes its simplified checks, but that does not establish that it is ready for a real committee to adopt. In the SGOV return stress, one portfolio weight moved by ten percentage points. That exceeded the proposed five-point stability tolerance and supports rejecting live adoption for now.”

**Show:** The Lab 20 prediction commit and before/after table.

“One AI-assisted output I checked was the prediction that raising the return objective from six and a half to seven percent would shift the solution. The prediction was committed before the run. The resulting allocation changed from ten percent SOXX and ninety percent SGOV to ten percent SOXX, five percent VTI, and eighty-five percent SGOV. Estimated return and volatility both increased. The prediction and test were AI-assisted; they are not a human-authored AI-off record. My reported instructor permission is documented, but the grading interpretation is the instructor's.”

“The conclusion is conditional on the data and assumptions, and the remaining checks are documented in the repository.”

## Video 2 — technical walkthrough (maximum 5:00)

**Show:** The repository README, then the terminal in the project folder.

**Say:** “I used OpenAI Codex to help build and validate the code and draft the analysis. I have reviewed the analysis and decision and take responsibility for them. This is for education, not investment advice.” [Use the ownership sentence only after actual review.]

“A reviewer installs the requirements and runs `python -m streamlit run app.py`, then selects the Intel-related fund example. The app loads the saved monthly prices. The prices have sixty-one monthly observations, yielding sixty monthly returns. The data were downloaded in October 2026, and the latest month in the saved sample is September 2026.”

**Show:** `portfolio.py`, `estimate_from_csv`, and `search_portfolio`.

“The estimate function calculates monthly percentage changes, annualizes the arithmetic mean by multiplying by twelve, and annualizes sample standard deviation by the square root of twelve. The search function enumerates fully invested, nonnegative allocations in five-percentage-point increments. It calculates expected return and eligible reserve weight, skips combinations that fail either modeled threshold, and chooses the remaining combination with the lowest estimated volatility.”

**Show:** The app baseline table and the saved output.

“The table compares equal weight, inverse volatility, a sixty-forty VTI and BND benchmark proxy, and the constrained solution. A pass only covers the simplified modeled rules; it does not certify the complete Lab 13 mandate. The benchmark proxy uses US equity rather than global equity and fails the example's SGOV reserve requirement.”

**Show:** Set the annual cost assumption to 1% and point to the constrained row. Then set the reserve minimum to 95% while leaving cost at 1%, and show the no-feasible-allocation verdict.

“With a one-percent annual cost drag, the model selects ten percent SOXX, ten percent VTI and eighty percent SGOV. Raising the SGOV minimum to ninety-five percent under this cost assumption leaves no feasible mix on the grid. This is an illustrative uniform annual drag, not a full transaction-cost model. The historical adjusted prices may have been revised after earlier dates; they do not establish a point-in-time backtest. The separate dated Treasury yield is context and does not determine the weights.”

“The validation record explains the earlier tests, AI assistance, and limitations. The model should not be treated as a guarantee of future returns or full mandate compliance.”

## Video 3 — investment committee presentation (maximum 5:00)

**Start with the app already open and the saved fund example selected.**

**Say:** “I used OpenAI Codex to help build and check this application and draft the analysis. I have reviewed the analysis and the decision and take responsibility for them. This is for education, not investment advice.” [Use the ownership sentence only after actual review.]

“My recommendation to the committee is to reject live adoption of this historical-estimate process for now. Consider a classroom pilot only after the return assumptions, full mandate, risk limits and stability rules are justified and approved.”

**Show:** The base constrained result and baseline table.

“The proposed classroom objective is an expected annual return of at least six and a half percent, after assumed costs, with at least five percent in SGOV. At the base assumptions and zero modeled cost, the minimum-volatility solution is ten percent SOXX and ninety percent SGOV. It has an estimated return of six point eight one percent and volatility of three point eight four percent. These are estimates from historical data, not guaranteed outcomes.”

“Equal weight passes the simplified modeled checks but has estimated volatility of thirteen point six nine percent. Inverse volatility has lower estimated volatility but fails the return objective. The sixty-forty benchmark proxy fails the reserve minimum and is not an exact global-equity benchmark.”

**Show:** The memo's stress table or the app control for the SGOV return estimate.

“The stress that matters most to my decision reduces SGOV's expected return by one percentage point. The selected mix becomes ten percent SOXX, ten percent VTI and eighty percent SGOV. The largest weight shift is ten percentage points, above the proposed five-point stability tolerance. Across the base, short-window and SGOV stress scenarios, SOXX ranges from five to ten percent and SGOV from eighty to ninety-five percent. That is an observed scenario range, not a recommended allocation range.”

“The process stops for live adoption if the modeled constraints fail, there is no feasible solution, assumptions cannot be justified, or the agreed stability condition is breached. The team should monitor return assumptions, costs, liquidity, realized risk and allocation drift. A committee should reconsider the rejection only after the mandate and risk measures are approved, forward assumptions are independently supported, implementation costs are tested and the agreed stresses pass.”

“My ask is to decline live adoption now, assign an owner to the unresolved mandate and data issues, and review a classroom pilot separately.”
