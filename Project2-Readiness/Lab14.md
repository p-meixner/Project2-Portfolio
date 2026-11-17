# Lab 14 - Portfolio baselines

AI-assisted technical work; student learning and partner tasks remain pending.
Inputs are course-authored training values, not market estimates.

Run `python portfolio.py` (or `.venv\Scripts\python.exe portfolio.py` here).
Rates in the engine are decimals; displayed weights and results are percentages.

## Baseline results
| Portfolio | Bills / 10-year / IG / equity (%) | Return (%) | Volatility (%) | Reserve (%) | Meets 6.5% |
|---|---|---|---|---|---|
| Benchmark | 0.0 / 0.0 / 40.0 / 60.0 | 6.80 | 10.46 | 0.0 | yes |
| Equal weight | 25.0 / 25.0 / 25.0 / 25.0 | 5.20 | 5.21 | 50.0 | no |
| Inverse volatility | 84.3 / 6.0 / 7.0 / 2.6 | 3.77 | 1.05 | 90.3 | no |

All calculations use unrounded weights. CPI 2.5% is a labelled estimate.
Meeting expected return alone does not establish mandate compliance.

## Technical validation
Executed output and assertions are saved in [Lab14-validation.txt](Lab14-validation.txt).
Known-answer returns, volatilities, and reserve weights matched.
Changing both IG-equity correlations from 0.25 to 0.50 produced benchmark
volatility of 11.00%. Correlation 1.3 was rejected; an asymmetric table was
also rejected. Checks used copies; saved base correlations remain 0.25.
This is AI-assisted verification, not a claimed partner swap.

## Mandate integration
Candidate E in [mandate.py](mandate.py) is 40% IG bonds / 60% global equity.
It has 0.0% reserve-eligible assets versus the computed 3.0% minimum.
Run `python mandate.py` to see its verdict alongside A-D.

## Diversification
Diversification combines exposures whose returns do not move perfectly together.
Portfolio risk depends on both each holding's volatility and the correlations
between holdings. For positive weights, correlation below +1 reduces variance
relative to the same holdings moving perfectly together. This does not guarantee
that a portfolio is less volatile than its least volatile holding.

The benchmark's 10.46% volatility is below equity's 16%, but above IG bonds' 6%.
It is below the 12% weighted-average volatility that would apply with correlation
of +1. This distinction matters when explaining the diversification benefit.

## Benchmark calculation by hand
Use decimal weights and volatilities: bonds 0.40 and 0.06; equity 0.60 and 0.16;
correlation 0.25.

```text
Expected return = 0.40(0.05) + 0.60(0.08)
                = 0.068 = 6.80%

Variance = (0.40^2)(0.06^2) + (0.60^2)(0.16^2)
           + 2(0.40)(0.60)(0.06)(0.16)(0.25)
         = 0.000576 + 0.009216 + 0.001152
         = 0.010944
Volatility = sqrt(0.010944) = approximately 10.46%

At correlation 0.50:
Variance = 0.000576 + 0.009216 + 0.002304 = 0.012096
Volatility = sqrt(0.012096) = approximately 11.00%

Omitting covariance:
sqrt(0.000576 + 0.009216) = approximately 9.90% (wrong for this case).
```

## Code walkthrough preparation
In `covariance_matrix`, each cell is correlation times the two asset volatilities.
Diagonal cells are individual variances because each asset's self-correlation is 1.

In `portfolio_volatility`:
1. `validate_weights` checks the number of weights, nonnegative finite values,
   and a total of 1.
2. `variance = sum(...)` accumulates contributions from every ordered asset pair.
3. `weights[i] * weights[j] * covariance[i][j]` weights that pair's covariance.
4. The outer loop selects asset i; the inner loop selects every asset j.
   Including both bond/equity and equity/bond supplies the factor of 2 in the
   hand calculation. The diagonal terms supply the individual weighted variances.
5. A materially negative variance raises an error.
6. `sqrt(max(0.0, variance))` converts variance to volatility, guarding against
   a tiny negative floating-point residual.

The engine checks the required range and symmetry conditions and unit diagonal.
It does not implement a general positive-semidefinite matrix test; passing these
input checks alone does not certify every possible edited correlation matrix.

## Reflection draft for review
Inverse volatility assigns more weight to lower-volatility holdings because each
raw weight is 1 divided by volatility. Bills have only 0.5% volatility, so their
raw weight is 200, compared with 14.2857 for the note, 16.6667 for IG bonds, and
6.25 for equity. Dividing by the total yields about 84.3% bills. This method does
not target the return objective or use correlations when choosing weights;
correlations are used afterward to calculate portfolio risk.

The benchmark is the clearest starting point for the CIO discussion because S4
names it as the comparison portfolio. Its 6.80% expected return exceeds the 6.50%
training objective, but its 0% reserve allocation violates S3. This demonstrates
why a performance reference is not automatically a permissible client allocation.
Equal weight and inverse volatility meet the reserve minimum but fall short of
the expected-return objective. None meets both conditions under these inputs.
Volatility is not a guaranteed calendar-year loss bound; S9 remains unresolved.

## Completed code quiz
Question: In `sum(w * sleeve["return"] for w, sleeve in zip(weights, sleeves))`,
what does `zip(weights, sleeves)` do, and why must the lists use the same order?

Student answer:
> I think zip(weights, sleeves) pairs each weight with its corresponding sleeve.
> They need to be in the same order so each sleeve gets the correct weight.
> If they are out of order, the calculations could be wrong.

Feedback: Correct. `zip` pairs entries by position, not by holding name.
The expression multiplies each weight by the paired expected return and sums
those contributions to calculate portfolio expected return.

## Reported discussion and break test with Sam Stewart
Sam asked:
> Why does your calculation include both the bond-equity pair and the
> equity-bond pair? Isn't that counting it twice?

Student's reported answer:
> Both terms belong in the portfolio variance formula. With two assets, the
> covariance contribution is 2 x bond weight x equity weight x covariance.
> The nested loops include each direction once, which supplies that factor of two.

The student confirmed that Sam's program stopped with an error when the
IG-equity correlation was changed to 1.3. The exact error text was not supplied.
Restoring 0.25 and confirming the baseline results has not yet been reported.

## Remaining student activity
- Restore the partner file's IG-equity entries to 0.25 and confirm the baseline results.
- Finish any remaining reciprocal code explanation and swap steps.
- Review the reflection draft and adopt or revise the CIO-first choice.

## Checkout
Publish portfolio.py, mandate.py, and these completed notes to your own GitHub
repository, and submit the file links. Publication has not been performed.
