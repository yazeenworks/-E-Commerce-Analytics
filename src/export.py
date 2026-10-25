from pathlib import Path
import json,shutil
from datetime import date
import duckdb
from plotly.offline import get_plotlyjs
ROOT=Path(__file__).resolve().parents[1]
def main():
    con=duckdb.connect(str(ROOT/'data/warehouse/fuzzy.duckdb'),read_only=True)
    out=ROOT/'data/exports';out.mkdir(parents=True,exist_ok=True)
    tables=['fct_orders','fct_order_items','fct_sessions','dim_products','dim_customers','dim_dates']
    for t in tables:
        path=str(out/f'{t}.csv').replace("'","''")
        con.execute(f"copy {t} to '{path}' (header,delimiter ',')")
    def records(sql):
        cur=con.execute(sql)
        cols=[x[0] for x in cur.description]
        data=[[v.isoformat() if hasattr(v,'isoformat') else float(v) if type(v).__name__=='Decimal' else v for v in row] for row in cur.fetchall()]
        return {'columns':cols,'rows':data}
    orders=records('select order_id,order_date,user_id,channel,campaign,device_type,item_count,revenue_usd,cogs_usd,gross_profit_usd,refund_usd,customer_order_number from fct_orders order by order_id')
    items=records('select order_item_id,order_id,product_id,order_date,user_id,channel,device_type,revenue_usd,cogs_usd,gross_profit_usd,refund_usd,refunded_item from fct_order_items order by order_item_id')
    sessions=records('''select session_date,channel,campaign,device_type,landing_page,count(*) as sessions,
        sum(orders) as orders,sum(converted_session) as converted,sum(revenue_usd) as revenue,sum(gross_profit_usd) as gp,
        sum(bounced) as bounced,sum(reached_products) as products,sum(reached_cart) as cart,
        sum(reached_shipping) as shipping,sum(reached_billing) as billing,sum(reached_thankyou) as thankyou
        from fct_sessions group by 1,2,3,4,5 order by 1''')
    page_popularity=records('''select s.session_date,s.channel,s.device_type,p.pageview_url,
        count(*) as pageviews,count(distinct s.website_session_id) as sessions
        from stg_pageviews p join fct_sessions s using(website_session_id)
        group by 1,2,3,4 order by 1''')
    products=records('select product_id,product_name,created_at::date as launch_date from dim_products order by 1')
    first=records('select user_id,first_order_at::date as first_date from dim_customers')
    run=json.loads((ROOT/'dbt_project/target/run_results.json').read_text())
    quality=[{'name':r['unique_id'].split('.')[-1].replace('_',' '),'status':r['status'],'seconds':r['execution_time']} for r in run['results'] if r['unique_id'].startswith('test.')]
    dates=con.execute('select min(session_date),max(session_date) from fct_sessions').fetchone()
    counts={t:con.execute(f'select count(*) from raw.{t}').fetchone()[0] for t in ['orders','order_items','order_item_refunds','products','website_sessions','website_pageviews']}
    data={'orders':orders,'items':items,'sessions':sessions,'products':products,'first':first,'pagePopularity':page_popularity,
        'meta':{'min_date':str(dates[0]),'max_date':str(dates[1]),'counts':counts,'quality':quality,'build_date':date.today().isoformat(),
        'source':'https://mavenanalytics.io/data-playground/toy-store-e-commerce-database'}}
    (ROOT/'dashboard/assets/data.js').write_text('window.FUZZY_DATA='+json.dumps(data,separators=(',',':'))+';')
    (ROOT/'dashboard/assets/plotly.min.js').write_text(get_plotlyjs())
    (ROOT/'docs/BUILD_METADATA.json').write_text(json.dumps(data['meta'],indent=2))
    shutil.copy(ROOT/'dbt_project/target/run_results.json',ROOT/'docs/DBT_RUN_RESULTS.json')
    con.close()
    print('Exported',len(orders['rows']),'orders,',len(items['rows']),'items,',len(sessions['rows']),'session groups.')
if __name__=='__main__':main()
