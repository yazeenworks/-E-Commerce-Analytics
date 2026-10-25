# Fuzzy Factory · Commerce Intelligence

**A complete ready-to-open analytics project with ten interactive workspace pages.**

The attached notebook supplied the project context: traffic sources, conversion, website paths, quarterly performance, product seasonality and sales growth. This package implements those topics as a fresh reproducible project; it does not copy the notebook screenshots or assume a MySQL server exists. Additional customer, refund, quality and transaction views make the analysis easier to audit.

## Start in one step

Extract the entire ZIP. On Windows double-click **START_WINDOWS.bat**. On any OS open **dashboard/fuzzy-factory.html** in a current browser. If Python is available, `python run.py` opens the same file.

**No package installation, database server, login or API key is required for viewing.** The source-derived dashboard data and Plotly runtime are bundled locally. Optional font loading uses Fontshare and falls back offline. Do not open the HTML from inside an unextracted ZIP or move it without its `assets/` folder.

## Completed workspace

| Page | Included interactions and analysis |
|---|---|
| Executive overview | Gross sales, gross profit, AOV, conversion, trends, financial bridge |
| Marketing performance | Source/campaign scorecards, device conversion and bounce rates |
| Products & refunds | Item-level contribution, margin, refund rates, product trends |
| Website conversion | Event-ordered funnel, stage conversion, landing-page scorecards and page popularity |
| Seasonality & growth | Quarterly operating scorecard, annual totals, monthly demand |
| Customer intelligence | Repeat purchases, frequency segments, observed buyer value, cohorts |
| Ask your data | Seven supported question templates and equivalent SQL |
| Order explorer | All orders, search, sortable columns, pagination, filtered CSV exports |
| Data quality & lineage | Real dbt results, model grains, source counts and lineage |
| Metric definitions | Exact formulas, source provenance and analytical limits |

Date, source and device filters recalculate data-driven pages. The URL hash preserves filter/page state on reload. Quality and methodology are full-build reference pages; global filters do not change source counts or rerun tests. Export CSV downloads the current page's analytical table; on Order explorer it exports all matching orders, not just the visible page. On Ask your data it exports the selected monthly sales reference table, not the assistant's prose. Browser Print / PDF and individual Plotly PNG exports are available. No API requests or database connection are used while viewing.

## Actual data

Official source: [Maven Analytics Toy Store E-Commerce Database](https://mavenanalytics.io/data-playground/toy-store-e-commerce-database). The provider labels it Public Domain. This is a fictional educational business, not a real retailer's confidential data. The included source files are unchanged; provenance and SHA-256 hashes are in `docs/SOURCE_MANIFEST.json`.

The six original tables contain **472,871 sessions, 1,188,124 pageviews, 32,313 orders, 40,025 sold items, 1,731 refund events and 4 products**. Observed sessions run March 19, 2012 through March 19, 2015. Both boundary months are partial. No synthetic rows or forecasts were added. A seventh CSV is the provider's data dictionary, not another fact table.

## Architecture

```text
Original source CSVs (six tables + dictionary)
  → src/ingest.py → DuckDB raw schema
  → six dbt staging views (null normalization, decimal money)
  → item-grain refunds aggregated BEFORE joining
  → six dbt analytical marts
  → twenty dbt data tests
  → src/export.py → clean CSVs + dashboard/assets/data.js
  → local browser dashboard (no server)
```

| Mart | Grain |
|---|---|
| fct_order_items | One row per sold item, with refunds pre-aggregated per item |
| fct_orders | One row per order, revenue and COGS reconciled to header |
| fct_sessions | One row per website session; pageviews and orders pre-aggregated |
| dim_customers | One row per observed buyer, full-history first purchase |
| dim_products | One row per catalog product |
| dim_dates | One row per observed source-calendar day |

## Optional rebuild

Viewing does not require Python. For a technical rebuild, Python 3.11 or 3.12 in a fresh virtual environment is recommended.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python run.py --rebuild --test
```

The command reloads included source CSVs, executes dbt models and tests, exports dashboard/CSV files only after dbt succeeds, runs Python tests and opens the browser. For a headless build use `python run.py --rebuild --test --no-open`. Direct dbt access: from `dbt_project/`, run `dbt build --profiles-dir .`. No personal credentials are stored.

Optional browser QA: install `requirements-browser-tests.txt`, run `python -m playwright install chromium`, then `python tests/browser_qa.py`. It checks all pages at desktop/mobile widths, independent SQL reconciliation, filtering, exports, theme switching, navigation and question routing with external HTTPS requests blocked.

For the optional walkthrough notebook, use a Jupyter environment with the packages in `requirements-notebook.txt`. All notebook outputs are already executed and saved.

## Included files

```text
START_HERE.txt, START_WINDOWS.bat, START_MAC.command, start_linux.sh
run.py, requirements.txt, requirements-browser-tests.txt
 dashboard/         completed offline web application
 data/raw/          original source CSVs and dictionary
 data/exports/      six clean Power BI-ready CSV marts
 data/warehouse/    prebuilt DuckDB database
 dbt_project/       staging SQL, six marts, twenty tests and profiles
 src/               ingest and export scripts
 sql/               eleven reusable business queries
 tests/             Python and optional browser tests
 notebooks/         original executable technical walkthrough
 docs/              metrics, provenance, QA, screenshots, handover
 powerbi/           optional DAX, Power Query, theme and relationship guide
```

## Verified release

The package passed 20 dbt data tests, 18 Python tests, 168 offline Chromium browser checks and execution of all 16 notebook code cells. See `docs/VALIDATION.md` for exact coverage and untested environments.

## Scope boundaries

- The finished dashboards are a web app. **No Power BI .pbix or Tableau .twbx is claimed.** Optional Power BI starter files are not a completed native report.
- The question box is deterministic and offline, **not an LLM or unrestricted text-to-SQL engine**. Similar questions are routed to fixed analyses. Unsupported metrics are rejected.
- No ad spend means no CAC or ROAS. No operating expense means no net profit. No targets, geolocation, shipping timing or forecast is invented.
- Gross profit = gross sales − product COGS. Refunds are allocated back to original sale date using the full observed refund history; not refund-date cash flow. Recent sale cohorts are right-censored for refunds.
- Repeat purchase rate is selected buyers with two or more selected orders divided by selected buyers. First purchase is determined over full source history. Cohort future cells are blank; final source month is partial.
- Funnel/landing-page results are descriptive. No valid randomized assignment or causal A/B effect is assumed merely because landing-page names differ.

## Publish or present

The browser app can be published on a static host by uploading `dashboard/` and configuring `fuzzy-factory.html` as the entry point. No hosting account was created or external deployment performed. Only the browser folder is needed for hosting. The whole source ZIP includes large CSVs and a database; do not upload all of it to a regular Git repository. `.gitignore` excludes large raw/generated artifacts. Preserve source attribution.

This is an AI-assisted implementation. If presenting it as a portfolio, review and run it yourself and explain the grains, joins, tests and limitations. Do not claim independent authorship or an LLM integration. A useful honest description: “Customized and validated an AI-assisted commerce analytics project using SQL, DuckDB, dbt and interactive web dashboards.” No hiring outcome is promised.
