# Lab 20 — Project 2 readiness record

Working draft. The cold-run note records details supplied by the student. The prediction and drafted responses below were written with AI assistance at the student's request; they are not evidence that AI was closed.

## Partner cold run

- Partner and date: Not supplied.
- Command: `python -m streamlit run app.py`.
- First failure: Streamlit was not installed, so the command failed.
- Elapsed time: 8 minutes.
- Result location: After dependencies were installed, the app opened in a browser. The reviewer selected **Load Intel-related fund example** and found the allocation and decision numbers there.
- Fix: Clarified the dependency installation step in the README; the student reported uploading it to GitHub.
- Follow-up check: AI acting as the requested partner role “Sam Stewart” ran the installation command in the existing environment on November 17, 2026; dependencies were already installed and the command succeeded. A Streamlit automated app test then selected the fund example without exceptions and displayed 6.81% expected return, 3.84% volatility, and 90% reserve. This was a local automated check, not a clean-machine browser rerun.

## Locked changed-input record

The published lab calls for a human prediction with AI closed. The student reports receiving instructor permission for AI assistance; the following is an AI-written prediction, so it does not establish compliance with the original AI-closed requirement. Commit and push it before running the change. Preserve before and after outputs and explain the result afterward.

**Prediction, before the changed-input run:** For the saved Intel-related fund example, raise the expected-return objective from **6.50% to 7.00% per year**. Keep the data, expected-return estimates, the 5% SGOV reserve minimum, and all other settings unchanged. I expect the chosen allocation to shift away from SGOV toward higher-expected-return assets, with expected return and estimated volatility increasing and reserve weight decreasing. I expect a feasible allocation to remain, but the higher target and any increased risk may make the case for a pilot weaker. The exact allocation is uncertain because the search uses a 5-percentage-point grid.

Prediction commit and push: Pending.

Existing baseline for the saved Intel-related fund example (October 2021–September 2026 monthly returns): SOXX / VTI / BND / SGOV weights **10% / 0% / 0% / 90%**, expected return **6.81%**, estimated volatility **3.84%**, and reserve **90%**. The return objective is 6.50% and the SGOV reserve minimum is 5%. See [Lab 15](Lab15.md) for the data and limitations. This existing baseline is not a new changed-input run.

Before and after outputs and explanation for the new change: Pending.

## Code explanation and reflection

- **AI-drafted answer to Sam's code question:** In `search_portfolio` in [portfolio.py](portfolio.py), each 5% grid allocation is constructed to be long-only and sum to 100%. The function calculates expected return and the weight in eligible reserves. If expected return falls below the objective or reserves fall below the minimum, it skips that allocation. It calculates volatility only for the remaining allocations and keeps the one with the lowest volatility. These are the two modeled mandate checks, not proof that all mandate provisions are met. A prior walkthrough is in [Lab 15](Lab15.md). A live student explanation and partner exchange have not been recorded.
- **Reflection draft for student review — what the cold run revealed:** The reviewer encountered a missing Streamlit installation before reaching the app. That made the installation prerequisite a more prominent README step.
- **Reflection draft for student review — what I will not touch before the deadline:** Avoid adding assets, features, or new research scope; focus on completing the required evidence, resolving documented failures, and keeping results and limitations consistent.

## Decision line

**Draft for student review:** Pilot the 10% SOXX / 90% SGOV classroom allocation, subject to independently justified forward estimates and the proposed five-percentage-point stability tolerance; reconsider adoption if those estimates fail the 6.50% return objective or the allocation exceeds that tolerance in the stated tests. This is the AI-assisted draft from [Lab 15](Lab15.md), not a final student decision. In that lab's separate SGOV stress, the allocation shifted by 10 percentage points, exceeding the proposed tolerance.

## Readiness gaps

- Confirm the intended mandate and scope in the student-owned repository.
- Create the decision memo, validation and AI-use record, submission manifest, research-evolution materials, and video/transcript links required by the assignment. Do not recreate a missing pre-AI Edition A.
- Confirm that the tool's implemented checks cover the intended mandate, or explicitly disclose missing checks. Review date, cost, data provenance, and point-in-time limitations.
- Commit and push the prediction before running the changed input; record the actual results and obtain any necessary instructor ruling on the AI-assisted prediction.
