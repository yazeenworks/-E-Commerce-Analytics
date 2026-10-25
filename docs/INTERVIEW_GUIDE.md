# Project presentation guide

## Honest short explanation

“I customized and validated an AI-assisted commerce analytics system. Six official Maven educational source tables enter DuckDB, dbt normalizes missing attribution and decimal money, and grain-safe marts drive the interactive browser dashboards. I can reconcile item/order/session sales, demonstrate data tests and explain why refunds, cohorts and partial months need careful interpretation.”

Review and run it before using that description. Do not say you independently wrote unfamiliar code, built a native Power BI artifact, integrated a real LLM or operated a production data platform.

## Demonstration sequence

1. Open Executive overview and explain sales, gross profit, AOV and conversion.
2. Filter a date range/source/device and demonstrate the same selected data in Marketing and Order explorer.
3. Open Products & refunds and explain why raw refund joins can multiply revenue.
4. Show the ordered website funnel; explain why landing-page differences are not automatically causal.
5. Show quarterly seasonality and explain partial boundary months.
6. Show repeat purchase and cohort retention; distinguish future blank cells from observed 0%.
7. Open Data quality and show actual dbt test results.
8. Open Ask your data, inspect SQL, then ask for ROAS and explain the rejection.

## Technical questions to prepare

- What is the grain of each mart?
- Why aggregate refunds and pageviews before joining?
- Why are repeat sessions not repeat purchases?
- Why is gross profit not net profit?
- Why is a high-conversion source not necessarily the highest ROI?
- How does a session date differ from an order date?
- Why do recent cohorts have incomplete return/refund follow-up?
- Why should future retention be null instead of 0?
- Which tests catch duplicate rows or revenue multiplication?
- What would production require beyond this local project? Authentication, scheduling, privacy, monitoring, incremental models and controlled publication.

No job or deadline outcome is guaranteed. Add your own written interpretation, local demo and screenshots after understanding the package.
