# Release validation

Validated on October 24, 2026 in a Linux environment with Python 3.12 and headless Chromium. Windows/macOS launcher behavior was not executed on native operating systems; opening the bundled HTML directly is the cross-platform fallback.

## Executed checks

- **dbt:** 12 models (6 staging views, 6 mart tables) and 20 data tests completed successfully; 32/32 build nodes succeeded, no warnings/errors. Machine-readable results: `DBT_RUN_RESULTS.json` and `BUILD_METADATA.json`.
- **Python regression suite:** 18 tests passed. Covers primary keys, counts, source-to-mart sales/refunds, order/header amounts, attribution, ordered funnel, first purchase and all 11 business SQL files.
- **Browser QA:** 168 checks passed. All ten pages rendered at 1440px and 375px, both themes rendered, SQL independently reconciled totals, date/source/device filters persisted in URL, explorer sorting/pagination/search/CSV worked, question templates produced executable SQL, unsupported metrics were rejected, cohorts distinguished future nulls from observed zero. No uncaught JavaScript errors. External HTTPS requests blocked throughout. Machine-readable results: `BROWSER_QA_RESULTS.json`.
- **Notebook:** all 16 Python cells executed without error; displayed outputs are saved in the notebook.
- **Source integrity:** SHA-256 verified for all seven original CSV files against `SOURCE_MANIFEST.json`.
- **Launcher:** `python -S run.py --no-open` succeeded, demonstrating the standard viewing launcher does not import installed packages.
- **JavaScript:** Node syntax validation and ESLint 9.39.1 completed without code errors.
- **Screenshots:** actual browser captures in `screenshots/`, including desktop, mobile, dark mode, funnel, cohorts and question assistant.

## What was not validated

No native Power BI/Desktop/Tableau report was authored or executed; starter assets are explicitly labeled optional. No live cloud hosting, authentication, scheduled ingestion, real LLM, load testing, native Windows/macOS execution, Safari/Firefox cross-browser testing or full WCAG audit is claimed. This is a complete local analytics project, not a production-operated service.
