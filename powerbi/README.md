# Optional Power BI starter — not a finished .pbix

The completed ready-to-open dashboards are in `dashboard/fuzzy-factory.html`. This folder is optional and does not require any work to view that completed application.

To create an additional Power BI report later:

1. Import the six CSVs from `data/exports/` using Power BI Desktop Text/CSV.
2. Set IDs to whole number, order/session dates to Date, timestamps to Date/Time and monetary values to fixed decimal where appropriate.
3. Use single-direction one-to-many relationships: dim_dates[date_day] → fct_orders[order_date], fct_order_items[order_date], fct_sessions[session_date]; dim_products[product_id] → fct_order_items[product_id]; dim_customers[user_id] → fct_orders[user_id], fct_order_items[user_id].
4. Do not introduce active fact-to-fact relationships or ambiguous filter paths. For common source/device slicers, create separate channel/device dimensions related to each fact. A customer dimension includes buyers only; do not relate it to session users as though it contained every visitor.
5. Mark dim_dates as the Date table, import the theme, and add DAX measures individually.
6. `load_table.pq` is an optional M query for a single table: change the local path and duplicate per mart. It is not a PBIX generator.

The browser cohort page is already implemented; an equivalent filter-aware Power BI cohort report would need additional DAX/modeling. All definitions and limitations in `docs/METRICS.md` still apply. Power BI Desktop and native PBIX authoring were not executed here.
