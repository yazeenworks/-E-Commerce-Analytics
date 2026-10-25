from pathlib import Path
import json
import duckdb
import pytest
ROOT=Path(__file__).resolve().parents[1]
@pytest.fixture(scope='module')
def con():
    c=duckdb.connect(str(ROOT/'data/warehouse/fuzzy.duckdb'),read_only=True)
    yield c
    c.close()
@pytest.mark.parametrize('table,key',[('fct_orders','order_id'),('fct_order_items','order_item_id'),('fct_sessions','website_session_id'),('dim_products','product_id'),('dim_customers','user_id'),('dim_dates','date_day')])
def test_primary_keys(con,table,key):
    n,u,nulls=con.execute(f'select count(*),count(distinct {key}),count(*) filter(where {key} is null) from {table}').fetchone()
    assert n==u and nulls==0
@pytest.mark.parametrize('fact,source',[('fct_orders','orders'),('fct_order_items','order_items'),('fct_sessions','website_sessions')])
def test_source_counts(con,fact,source):
    assert con.execute(f'select count(*) from {fact}').fetchone()[0]==con.execute(f'select count(*) from raw.{source}').fetchone()[0]
def test_sales_reconcile(con):
    values=[float(con.execute(f'select sum({col}) from {table}').fetchone()[0]) for table,col in [('raw.orders','price_usd'),('raw.order_items','price_usd'),('fct_orders','revenue_usd'),('fct_order_items','revenue_usd'),('fct_sessions','revenue_usd')]]
    assert max(values)-min(values)<.01

def test_refunds_reconcile(con):
    raw=float(con.execute('select sum(refund_amount_usd) from raw.order_item_refunds').fetchone()[0])
    for table in ['fct_order_items','fct_orders','fct_sessions']:
        assert abs(float(con.execute(f'select sum(refund_usd) from {table}').fetchone()[0])-raw)<.01

def test_funnel(con):
    assert con.execute('select count(*) from fct_sessions where reached_thankyou>reached_billing or reached_billing>reached_shipping or reached_shipping>reached_cart or reached_cart>reached_products').fetchone()[0]==0

def test_first_purchase(con):
    assert con.execute('select count(*) from dim_customers d join (select user_id,min(created_at) as f from fct_orders group by 1) o using(user_id) where d.first_order_at<>o.f').fetchone()[0]==0

def test_gross_profit(con):
    assert con.execute('select count(*) from fct_order_items where abs(gross_profit_usd-revenue_usd+cogs_usd)>.01').fetchone()[0]==0

def test_order_header_totals(con):
    assert con.execute('select count(*) from fct_orders f join raw.orders o using(order_id) where abs(f.revenue_usd-o.price_usd)>.01 or abs(f.cogs_usd-o.cogs_usd)>.01 or f.item_count<>o.items_purchased').fetchone()[0]==0

def test_attribution(con):
    assert con.execute("select count(*) from stg_sessions where channel is null or campaign is null or utm_source='NULL'").fetchone()[0]==0

def test_all_sql_runs(con):
    files=list((ROOT/'sql').glob('*.sql'))
    assert len(files)==11
    for f in files:assert con.execute(f.read_text()).fetchall(),f.name

def test_build_evidence(con):
    meta=json.loads((ROOT/'docs/BUILD_METADATA.json').read_text())
    assert len(meta['quality'])==20 and all(r['status']=='pass' for r in meta['quality'])
    for table,count in meta['counts'].items():assert con.execute(f'select count(*) from raw.{table}').fetchone()[0]==count
