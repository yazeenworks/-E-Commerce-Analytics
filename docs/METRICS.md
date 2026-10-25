# Metric contracts

## Core definitions

| Metric | Definition | Scope/limitation |
|---|---|---|
| Gross sales | Sum sold-item prices | Before refunds |
| Product COGS | Sum recorded sold-item COGS | Not all business costs |
| Gross profit | Gross sales − product COGS | Not operating or net profit |
| Gross margin | Gross profit / gross sales | 0 when denominator is 0 in UI |
| Refund amount | All observed refund events on selected sold items | Allocated to original order date |
| Net sales | Gross sales − refunds | Not net profit |
| After-refund contribution | Gross sales − COGS − refunds | No COGS recovery assumed; no overhead |
| AOV | Gross sales / orders | Gross, not after refunds |
| Session conversion | Sessions with >=1 order / sessions | Session-date basis |
| Sales per session | Attributed gross sales / sessions | Not ROAS |
| Bounce rate | One-pageview sessions / sessions | Not GA4 engagement |
| Refunded-item rate | Items with >=1 refund / sold items | Not refund events divided by orders |
| Repeat purchase rate | Selected buyers with >=2 selected orders / selected buyers | Window-dependent, not lifetime probability |
| Returning order | Customer order number >1 over full history | Distinct from selected-window repeat buyer |
| Observed buyer value | Selected gross sales / selected buyers | Not predicted LTV |

## Grain and time

Staging monetary columns are decimal(18,2). Refund events are summed per item before joining, preventing revenue duplication. Order amounts are aggregated before joining to session-level page metrics. Browser exports use JSON numbers; display rounds to currency precision.

Sales/product/customer pages filter on original order date, inclusive endpoints. Acquisition and funnel pages filter session creation date. Refunds follow the original sale rather than refund event date, so these metrics are not period cash flows. Recent orders have less refund follow-up. The source starts March 19, 2012 and ends March 19, 2015, so boundary months and quarters are incomplete. No annualized or partial-period growth forecast is claimed.

## Attribution

Literal NULL and empty string attribution tags are normalized. Existing source tags are retained. Missing source plus missing referrer becomes Direct; missing source with a referrer becomes Organic / referral. This combined group does not claim to classify search versus all referrals. Missing campaign becomes Unattributed. Source/device filters apply to individual order/session events, not lifetime acquisition properties.

## Funnel and landing pages

Pageview IDs determine event order. First occurrences of /products, /cart, /shipping, /billing or /billing-2, and /thank-you-for-your-order must increase strictly. Every stage requires the previous stages. This is a first-occurrence ordered-path implementation; repeated-page journeys could require more advanced sequence matching. Landing-page comparisons are descriptive, not proof of randomized causal lift or statistical significance.

## Customer cohorts

First purchase is calculated using full order history. The heatmap denominator is selected buyers whose first purchase falls in the selected dates. Later selected purchase events count as active, one per buyer/cohort-age cell. Source/device filters apply to selected order events; denominators are not fixed original acquisition-channel cohorts. Month 0 includes an observed selected purchase in the acquisition calendar month, not necessarily only the first transaction. An observed future repeat count of zero is 0%; an unobserved calendar month is blank. The final observed month may be partial. The heatmap shows at most the first 19 cohort ages (month 0 through 18), with buyer exports retaining the complete selected population.

## Missing facts

No advertising spend, CAC, ROAS, net profit, operating expenses, taxes, delivery timing, geography, inventory, randomized experiment assignments, targets or forecasts are supplied. Never imply these can be calculated from the provided tables alone.

Page popularity counts all pageviews and distinct sessions per page, joined to session-date attributes. A session can visit many different pages; do not sum page-level unique-session counts as a global distinct population.
