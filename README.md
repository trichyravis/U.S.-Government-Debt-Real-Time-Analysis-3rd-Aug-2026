# U.S. Government Debt — Real-Time Analysis & Learning Studio

A Mountain Path Academy Streamlit project for analysing official U.S. federal debt data, debt composition, long-run growth, interest cost and the Treasury financing environment.

## Features

- Official daily Debt to the Penny data from U.S. Treasury Fiscal Data.
- Debt held by the public versus intragovernmental holdings.
- Daily and fiscal-year debt growth analysis.
- Reported interest expense and refinancing-cost interpretation.
- Official Treasury par yield curve as financing context.
- Dedicated educational tab covering debt, deficits, holders, maturity structure and sustainability.
- Knowledge check and professionally formatted Excel workbook download.
- Reproducible classroom fallback when a live provider is unavailable.

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Fiscal Data series are published on their official release schedules; “real-time” means the latest available official observation. Treasury par yields are indicative bid-side curve estimates. Educational material only—not policy or investment advice.
