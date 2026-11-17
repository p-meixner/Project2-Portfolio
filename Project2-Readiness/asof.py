"""Lab 16: publication dates determine what was knowable."""

# Editable inputs: row number, ticker, month measured, publication date, index.
DECISION_DATE = "2026-03-31"
TABLE = [
    (1, "AAA", "2026-01", "2026-02-10", 101.0),
    (2, "AAA", "2026-02", "2026-03-10", 104.0),
    (3, "AAA", "2026-03", "2026-04-10", 109.0),
    (4, "AAA", "2026-02", "2026-03-25", 103.0),
    (5, "BBB", "2026-01", "2026-02-10", 98.0),
    (6, "BBB", "2026-02", "2026-03-10", 97.0),
    (7, "BBB", "2026-02", "2026-03-10", 97.0),
    (8, "BBB", "2026-03", "2026-04-10", 92.0),
    (9, "CCC", "2026-01", "2026-02-10", 110.0),
    (10, "CCC", "2026-02", "2026-04-05", 112.0),
    (11, "", "2026-02", "2026-03-10", 99.0),
    (12, "CCC", "2026-02", "2026-03-10", 111.0),
]

from datetime import date


def report(label, removed):
    numbers = ", ".join(str(row[0]) for row in removed) or "none"
    print(f"{label}: removed {len(removed)}; rows: {numbers}")


def latest_publications(rows):
    """Rule 4: retain one latest publication for each ticker and month."""
    latest = {}
    for row in rows:
        key = (row[1], row[2])  # Ticker and month measured.
        if key not in latest or row[3] > latest[key][3]:
            latest[key] = row
        elif row[3] == latest[key][3] and row[4] != latest[key][4]:
            raise ValueError(f"Conflicting values on the same publication date: {key}")
    return sorted(latest.values(), key=lambda row: row[0])


def signals(panel):
    results = {}
    for ticker in sorted({row[1] for row in panel}):
        history = sorted((row for row in panel if row[1] == ticker),
                         key=lambda row: row[2])
        current = history[-1]
        month = date.fromisoformat(current[2] + "-01")
        label = f"{month:%B %Y}"
        if len(history) < 2:
            results[ticker] = f"N/A ({label}; no previous month)"
            continue
        previous = history[-2]
        prior_month = date.fromisoformat(previous[2] + "-01")
        if month.year * 12 + month.month - (prior_month.year * 12 + prior_month.month) != 1:
            results[ticker] = f"N/A ({label}; previous calendar month missing)"
        elif previous[4] == 0:
            results[ticker] = f"N/A ({label}; previous index is zero)"
        else:
            change = (current[4] / previous[4] - 1) * 100
            results[ticker] = f"{change:+.2f}% ({label})"
    return results


def main():
    cutoff = date.fromisoformat(DECISION_DATE)
    print(f"Decision date: {cutoff}\nStarting rows: {len(TABLE)}")

    # Rule 1: quarantine missing tickers.
    report("1. Quarantined: no ticker", [r for r in TABLE if not r[1] or not r[1].strip()])
    identified = [r for r in TABLE if r[1] and r[1].strip()]

    # Rule 2: row number is provenance, not part of the data being compared.
    seen = set()
    clean, duplicates = [], []
    for row in identified:
        if row[1:] in seen:
            duplicates.append(row)
        else:
            seen.add(row[1:])
            clean.append(row)
    report("2. Exact duplicate", duplicates)

    # Rule 3: publication on the decision date is included.
    future = [r for r in clean if date.fromisoformat(r[3]) > cutoff]
    eligible = [r for r in clean if date.fromisoformat(r[3]) <= cutoff]
    report("3. Published after decision date", future)

    # Rule 4 runs only on eligible publications, so later revisions cannot leak in.
    panel = latest_publications(eligible)
    report("4. Older vintage replaced by revision", [r for r in eligible if r not in panel])

    print(f"\nAs-of panel ({len(panel)} rows)")
    print("Row  Ticker  Month    Published     Index")
    for number, ticker, month, published, value in panel:
        print(f"{number:>3}  {ticker:<6}  {month}  {published}  {value:>6.1f}")

    # Naive comparison still cleans missing tickers and duplicates, but skips rule 3.
    naive_panel = latest_publications(clean)
    asof_signals, naive_signals = signals(panel), signals(naive_panel)
    print("\nTicker  As-of signal                       Naive signal")
    for ticker in sorted(naive_signals):
        print(f"{ticker:<6}  {asof_signals.get(ticker, 'N/A (no knowable rows)'):<33} {naive_signals[ticker]}")
    return panel, naive_panel


if __name__ == "__main__":
    main()
