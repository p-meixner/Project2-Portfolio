# Lab 13 Meridian mandate and Project 2 implementation

The Lab 13 case is a fictional $100 million portfolio with a seven-year horizon, annual rebalancing, a CPI + 4% annual objective over rolling five years, $0.75 million quarterly payouts, and twelve months of eligible reserves. The resulting original reserve minimum is 3%. It uses a 60% global equity / 40% US investment-grade bond benchmark. See [Lab 13](../Lab13.md) for the full mandate and its unresolved wording.

The saved SOXX/VTI/BND/SGOV example was developed later as a proposed classroom extension; it is not the original Meridian mandate, Intel's corporate investment policy, or an approved client mandate. Its 6.50% expected nominal annual return objective is numerically consistent with a 2.50% inflation assumption plus 4%, but expected annual return is not the same test as achieving CPI + 4% net over rolling five years. The example assumes at least 5% in SGOV, stricter than the original 3% reserve amount, and uses this extra requirement as a proposed classroom constraint, not an established Meridian instruction.

| Lab 13 item | Current implementation and limitation |
|---|---|
| Long-only, fully invested; no leverage, shorts or derivatives | The grid produces nonnegative fund weights totaling 100%. It does not inspect the funds' underlying derivatives or financing. |
| Twelve months of distributions, minimum $3 million / 3% | The example sets a 5% SGOV minimum. It does not establish that SGOV qualifies under a client-approved cash/government security definition or perform cash-flow scheduling. |
| Seven-year horizon; annual rebalancing | Historical monthly returns estimate static inputs; no seven-year projection or annual rebalancing policy is implemented. |
| CPI + 4% net over rolling five years | A 6.50% annual expected-return threshold uses a 2.50% inflation assumption; there is no rolling five-year real-return validation or full cost model. |
| 60% global equity / 40% US IG bond benchmark | The app shows a 60% VTI / 40% BND proxy. VTI is US equity, not global equity; BND is a broad US bond fund, not an exact US investment-grade benchmark. The proxy has 0% SGOV and fails the example's 5% reserve rule. |
| At most 8% per nonexempt issuer, with exemptions | Fund look-through issuer exposures and applicable exemptions are not evaluated. The example cannot certify this rule. |
| At least 90% redeemable within five business days | The model does not document or test redemption, market liquidity or stress liquidity for the ETF holdings. |
| Annual turnover at most 25% absent committee approval | Trading history, turnover, exceptions and rebalancing trades are not modeled. |
| No calendar-year loss over 10%, unspecified measurement and breach rule | Annualized volatility is shown; it cannot guarantee or verify a calendar-year loss cap. The CIO must specify an actionable risk measure, threshold and breach response. |

The app's PASS/FAIL labels cover only its stated simplified modeled checks. They are not verdicts on the full Meridian mandate. The committee recommendation is to reject live adoption until these gaps and forward assumptions are resolved. Preserve the distinction if a different mandate is approved later.
