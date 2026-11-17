"""Run meaningful Lab 15 engine and interface regression checks."""
from copy import deepcopy
from io import BytesIO
from pathlib import Path
import subprocess
import sys

import numpy as np
import pandas as pd
from streamlit.testing.v1 import AppTest

from portfolio import SLEEVES, CORRELATIONS, estimate_from_csv, search_portfolio

before = Path("Lab15-baseline-before.txt").read_text(encoding="utf-8-sig")
after = subprocess.check_output([sys.executable, "portfolio.py"], text=True)
assert before == after
print("PASS: Lab 14 printed output unchanged.")

base = search_portfolio(SLEEVES, CORRELATIONS)
stress_inputs = deepcopy(SLEEVES)
stress_inputs[3]["return"] = .07
stress = search_portfolio(stress_inputs, CORRELATIONS)
correlations = deepcopy(CORRELATIONS)
correlations[2][3] = correlations[3][2] = .5
changed = search_portfolio(SLEEVES, correlations)
for label, result, weights, ret, vol in [
    ("As loaded", base, [0, .2, .25, .55], "6.51%", "9.44%"),
    ("Equity 7%", stress, [0, .1, .1, .8], "6.53%", "12.94%"),
    ("Correlation 0.50", changed, [0, .4, 0, .6], "6.52%", "9.73%"),
]:
    assert result["weights"] == weights
    assert f'{result["return"]:.2%}' == ret
    assert f'{result["volatility"]:.2%}' == vol
    print(f"PASS: {label}: {weights}, {ret}, {vol}")
assert abs(max(abs(a-b) for a,b in zip(base["weights"], stress["weights"])) - .25) < 1e-12
assert search_portfolio(SLEEVES, CORRELATIONS, objective=.10) is None
assert search_portfolio(SLEEVES, CORRELATIONS, eligible_indices=()) is None

# Synthetic prices are test fixtures only, never student market evidence.
rng = np.random.default_rng(15)
returns = rng.normal(.005, .03, (60, 3))
prices = pd.DataFrame(np.vstack([np.ones(3)*100, 100*np.cumprod(1+returns, axis=0)]),
                      columns=["TEST_A", "TEST_B", "TEST_C"])
prices.insert(0, "Date", pd.date_range("2021-09-30", periods=61, freq="ME"))
data = prices.to_csv(index=False).encode()
for recent in (False, True):
    sleeves, corr = estimate_from_csv(BytesIO(data), recent)
    sample = returns[-36:] if recent else returns
    np.testing.assert_allclose([s["return"] for s in sleeves], sample.mean(axis=0)*12)
    np.testing.assert_allclose([s["volatility"] for s in sleeves], sample.std(axis=0, ddof=1)*np.sqrt(12))
    np.testing.assert_allclose(corr, np.corrcoef(sample.T), atol=1e-12)
print("PASS: CSV estimates use all returns or exactly the last 36 returns.")
bad = prices.drop(index=5).to_csv(index=False).encode()
try:
    estimate_from_csv(BytesIO(bad))
    raise AssertionError("Missing month accepted")
except ValueError:
    pass

app = AppTest.from_file("app.py").run(timeout=30)
assert not app.exception
assert [m.value for m in app.metric] == ["6.51%", "9.44%", "20.00%"]*2 + ["0.00"]
equity = next(w for w in app.number_input if w.label == "Global equity index fund expected return (%)")
equity.set_value(7.0).run()
assert not app.exception
assert [m.value for m in app.metric][-4:] == ["6.53%", "12.94%", "10.00%", "25.00"]
print("PASS: actual app controls reproduce the 7% stress and 25-point change.")

# Temporarily edit the actual engine file, run a fresh app process, always restore it.
engine = Path("portfolio.py")
original = engine.read_bytes()
try:
    engine.write_bytes(original.replace(b"[0.05, 0.80, 1.00, 0.25]", b"[0.05, 0.80, 1.00, 0.50]")
                      .replace(b"[0.00, -0.10, 0.25, 1.00]", b"[0.00, -0.10, 0.50, 1.00]"))
    subprocess.run([sys.executable, "-c",
        "from streamlit.testing.v1 import AppTest; "
        "a=AppTest.from_file('app.py').run(timeout=30); "
        "assert not a.exception; "
        "assert [m.value for m in a.metric][:3]==['6.52%','9.73%','40.00%']"], check=True)
finally:
    engine.write_bytes(original)
print("PASS: actual engine correlation edit changes app answer; file restored to 0.25.")
