"""Download adjusted daily closes and retain each completed month's last close."""
from datetime import datetime, timezone
from pathlib import Path
import json

import pandas as pd
import requests

TICKERS = ["SOXX", "VTI", "BND", "SGOV"]
START = "2021-09-01"
END = "2026-10-01"  # Exclusive: omit the unfinished October 2026 month.


def main():
    evidence = Path("Lab15-data")
    evidence.mkdir(exist_ok=True)
    series = []
    sources = []
    for ticker in TICKERS:
        response = requests.get(
            f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}",
            params={"period1": int(pd.Timestamp(START, tz="UTC").timestamp()),
                    "period2": int(pd.Timestamp(END, tz="UTC").timestamp()),
                    "interval": "1d", "events": "div,splits"},
            headers={"User-Agent": "Mozilla/5.0"}, timeout=45)
        response.raise_for_status()
        raw = response.json()
        if raw["chart"]["error"]:
            raise ValueError(raw["chart"]["error"])
        item = raw["chart"]["result"][0]
        if item["meta"]["symbol"] != ticker or item["meta"]["currency"] != "USD":
            raise ValueError("Unexpected symbol or currency")
        dates = pd.to_datetime(item["timestamp"], unit="s", utc=True).tz_convert("America/New_York").tz_localize(None)
        daily = pd.Series(item["indicators"]["adjclose"][0]["adjclose"], index=dates, name=ticker)
        daily = daily.loc[(daily.index >= START) & (daily.index < END)]
        if daily.isna().any() or daily.index.has_duplicates:
            raise ValueError(f"Missing/duplicate daily data for {ticker}")
        monthly = daily.resample("ME").last()
        expected = pd.date_range("2021-09-30", "2026-09-30", freq="ME")
        if not monthly.index.equals(expected) or monthly.isna().any() or (monthly <= 0).any():
            raise ValueError(f"Incomplete five-year monthly history for {ticker}")
        series.append(monthly)
        (evidence / f"{ticker}-yahoo.json").write_text(json.dumps(raw), encoding="utf-8")
        sources.append({"ticker": ticker, "url": response.url,
                        "history_page": f"https://finance.yahoo.com/quote/{ticker}/history/",
                        "downloaded_utc": datetime.now(timezone.utc).isoformat(),
                        "field": "indicators.adjclose[0].adjclose",
                        "method": "last trading-day adjusted close per completed calendar month",
                        "price_rows": len(monthly), "monthly_returns": len(monthly)-1})
    prices = pd.concat(series, axis=1)
    prices.index.name = "Date"
    prices.to_csv("prices.csv", date_format="%Y-%m-%d")
    (evidence / "sources.json").write_text(json.dumps(sources, indent=2), encoding="utf-8")
    print(prices.iloc[[0, -1]].to_string())
    print("Saved 61 monthly prices per fund: 60 returns, October 2021–September 2026.")


if __name__ == "__main__":
    main()
