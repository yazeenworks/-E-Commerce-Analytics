# Troubleshooting

## I only want to open it

Extract the whole ZIP. Open `dashboard/fuzzy-factory.html` in Chrome, Edge or Firefox. It must stay next to the included `assets/` folder. No Python or Power BI installation is necessary. If the Windows launcher is blocked by corporate policy, opening the HTML directly is sufficient.

## The Mac launcher is blocked

Downloaded shell scripts may not retain executable permissions. Open the HTML directly, or run `python3 run.py` if Python is installed. Do not bypass your device's security policies.

## Fonts look different offline

Fontshare is optional. Chart code and data are bundled locally; system font fallback does not affect analytics. The dashboard was tested with external HTTPS requests blocked.

## Optional rebuild dependency conflict

Use Python 3.11 or 3.12 in a fresh virtual environment and install the pinned `requirements.txt`. Avoid installing into an unrelated project environment. Viewing the prebuilt app does not require this setup.

## Database locked or incompatible

Close other applications holding `data/warehouse/fuzzy.duckdb`. Use the pinned rebuild dependencies. The raw CSVs allow a rebuild; the dashboard does not query the database while viewing. Do not run concurrent builds against the same database.

## I changed source data but charts did not change

The dashboard is a published snapshot. Run `python run.py --rebuild --test`, then reload. The command runs dbt checks before exporting. A failed build leaves the prior dashboard data available; it does not claim the new data passed.

## The pages show different totals for the same date range

Order pages use order dates; acquisition/funnel pages use session dates. Refunds are allocated to original sales. Check event grain, filters and the metric contract before comparing metrics.

## Where is Power BI / Tableau?

The finished report is a web application, not a .pbix/.twbx. The optional `powerbi/` assets are labeled starter files; no native authoring tool is needed to see the completed dashboards.

## How do exports work?

The top export button downloads each page's analytic table. The explorer exports all matching orders. The question page exports monthly reference values, not prose. Individual Plotly charts have a hover toolbar for PNG export. Print / PDF uses your browser's print dialog.

## Is the question assistant AI?

It is a fixed, auditable question-template router, not an LLM. Questions outside its scope are rejected. It does not execute user-provided arbitrary SQL.
