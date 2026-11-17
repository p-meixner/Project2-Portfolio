# Lab 16 - Provenance Gate

Built with AI assistance using the fictional classroom card-spend table.

## Question

On the day you would have traded, what did this data actually say, and how
much of what you see now came later?

## Run

```powershell
python asof.py
```

[Python file](asof.py) uses only the standard library. Edit `TABLE` and
`DECISION_DATE` at the top. The saved decision date is `2026-03-31`.
[Executed verification](Lab16-validation.txt) includes both dates.

## Known-answer verification

| Rule, applied in order | Count removed | Row numbers |
|---|---:|---|
| Quarantine missing ticker | 1 | 11 |
| Remove exact duplicate (excluding row ID) | 1 | 7 |
| Remove publication after March 31 | 3 | 3, 8, 10 |
| Keep latest eligible revision per ticker/month | 1 | 2 |

The remaining panel contains rows **1, 4, 5, 6, 9, 12**.

Signal = `(latest month index / previous month index - 1) * 100`.

| Ticker | As-of signal | Naive signal |
|---|---|---|
| AAA | +1.98% (February) | +5.83% (March) |
| BBB | -1.02% (February) | -5.15% (March) |
| CCC | +0.91% (February) | +1.82% (February, revised) |

All values match. With April 15 as the decision date, the as-of panel and
signals equal the naive panel and signals. This check changed the imported
module's date in memory; the source file remains set to March 31.

## Interpretation and code study

The month measured is event time; publication time tells us when the number
became available. A revision is a later publication for the same measured month.
Look-ahead bias occurs when a historical decision uses information that became
available only afterward.

`latest_publications` groups rows by `(ticker, month)` and replaces a stored
row only when it encounters a later publication. For the as-of panel, it receives
only rows that already passed the decision-date filter. Thus AAA's March 25
revision replaces its March 10 release, but CCC's April 5 revision cannot replace
its March 10 release on March 31. The naive panel skips the date filter.

AAA's knowable change is from 101 to 103. Its naive change is from 103 to 109,
using March data published April 10. The larger naive signal was unavailable
on March 31 and also measures a different month-to-month interval.

## Rule 4, line by line

```python
latest = {}
for row in rows:
    key = (row[1], row[2])
    if key not in latest or row[3] > latest[key][3]:
        latest[key] = row
    elif row[3] == latest[key][3] and row[4] != latest[key][4]:
        raise ValueError(f"Conflicting values on the same publication date: {key}")
return sorted(latest.values(), key=lambda row: row[0])
```

1. `latest = {}` creates an empty dictionary to hold the selected rows.
2. `for row in rows` examines each eligible row.
3. `key = (row[1], row[2])` groups by ticker and month measured. Grouping by
   ticker alone would discard earlier months needed to calculate the signal.
4. The `if` keeps a row when its group is new or its publication is later than
   the stored publication. Fixed-width `YYYY-MM-DD` strings sort chronologically.
5. `latest[key] = row` stores the new row or replaces the older vintage.
6. The `elif` checks for conflicting index values with the same publication date
   for the same ticker and month.
7. `raise ValueError` stops instead of arbitrarily choosing between those values.
8. `return sorted(...)` returns the selected rows in original row-number order.

Rule 3 has already removed future publications before this function receives
the as-of rows. The same function also builds the naive panel, using cleaned
rows without the publication cutoff.

Practice question: why keep row 4 instead of row 2 when its index is lower?
Answer: the rule selects the latest available publication, not the highest
index. March 25 is later than March 10 and is still before March 31.

## Reflection answers

**Which rule removed the row that mattered most?** For AAA's misleading naive
signal, rule 3 removes row 3: the March index of 109 was published April 10,
after the March 31 decision. It cannot support a March 31 decision. Rule 4
also matters because keeping AAA's older February value of 104 would produce
+2.97% instead of the correct +1.98%.

**What would a backtest built on the naive column claim?** It would act as
though March 31 decisions could use AAA's +5.83%, BBB's -5.15%, and CCC's
revised +1.82%. Those numbers depend on April publications. A strategy could
therefore appear to anticipate later information, making its historical
performance misleading. The table alone cannot show the size or direction of
the resulting trading returns.

**Why does AAA's +5.83% look better than what was knowable?** It uses the
increase from February's 103 to March's 109. March's value was unavailable
until April 10. On March 31, the latest available comparison was January's
101 to February's revised 103, only +1.98%. The two signals also cover different
month-to-month intervals.

## Student checkout

### Partner exchange (student-reported completion)

I explained that rule 4 uses a dictionary keyed by ticker and measured month.
A row is stored when the key is new, or replaces the stored row when its
publication date is later. My partner asked why AAA keeps row 4 instead of
row 2. I explained that the March 25 publication revises the March 10 value,
so the February index is 103. When asked whether an April revision could
sneak in, I explained that rule 3 removes future publications first.

We swapped roles and tested April 15. The as-of and naive signals matched:
AAA +5.83%, BBB -5.15%, and CCC +1.82%. We discussed why using those April
publications on March 31 would introduce look-ahead bias, and agreed to
restore the decision date to March 31. The saved Python file uses March 31.

### Remaining checkout

- Complete Brightspace Lab 16 and submit GitHub links to these files after upload.
- Bring your Lab 15 Project 2 universe and chat; prepare the ALFRED series table.

The partner discussion and shared date-change test above are reported by the
student. Running a separate copy of the partner's file was not explicitly
reported. Brightspace submission, GitHub upload, and ALFRED prework are not
recorded as completed.
