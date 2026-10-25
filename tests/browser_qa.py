"""Optional offline end-to-end QA. Requires requirements-browser-tests.txt and Chromium."""
from pathlib import Path
from tempfile import TemporaryDirectory
import csv,json,math
import duckdb
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
PAGES=['overview','marketing','products','funnel','seasonality','customers','ask','explorer','quality','about']
checks=[]
def check(name,condition):
    if not condition:raise AssertionError(name)
    checks.append({'check':name,'status':'pass'})
def navigate(page,name):
    page.evaluate('(name)=>window.FUZZY_APP.navigate(name)',name)
    page.wait_for_timeout(140)
def compare(page,con,where_o='',where_s=''):
    got=page.evaluate('window.FUZZY_APP.totals()')
    o=con.execute('select count(*),sum(revenue_usd),sum(gross_profit_usd),sum(refund_usd),sum(cogs_usd),count(distinct user_id) from fct_orders '+where_o).fetchone()
    for k,v in zip(['orders','revenue','gp','refunds','cogs','buyers'],o):check('SQL reconciliation: '+k,abs(got[k]-float(v or 0))<.0001)
    ss=con.execute('select count(*),sum(converted_session) from fct_sessions '+where_s).fetchone()
    for k,v in zip(['sessions','converted'],ss):check('SQL reconciliation: '+k,got[k]==int(v or 0))
def main():
    con=duckdb.connect(str(ROOT/'data/warehouse/fuzzy.duckdb'),read_only=True)
    errors=[];network=[]
    with sync_playwright() as p,TemporaryDirectory() as temp:
        browser=p.chromium.launch(headless=True)
        ctx=browser.new_context(viewport={'width':1440,'height':1000},accept_downloads=True,color_scheme='light')
        ctx.route('https://**/*',lambda r:(network.append(r.request.url),r.abort())[-1])
        page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto((ROOT/'dashboard/fuzzy-factory.html').as_uri());page.wait_for_function('window.FUZZY_READY===true')
        page.wait_for_selector('#sales-trend .main-svg')
        compare(page,con)
        check('Full order count',page.evaluate('window.FUZZY_APP.totals().orders')==32313)
        for width,height in [(1440,1000),(375,812)]:
            page.set_viewport_size({'width':width,'height':height})
            for name in PAGES:
                navigate(page,name)
                check(f'{width}px {name}: no error view',page.get_by_text('We could not render this view').count()==0)
                check(f'{width}px {name}: one heading',page.locator('h1').count()==1)
                check(f'{width}px {name}: no document overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
                check(f'{width}px {name}: body has content',len(page.locator('#view').inner_text())>50)
            navigate(page,'overview')
            page.screenshot(path=str(ROOT/f'docs/screenshots/executive-{width}.png'),full_page=True)
        page.set_viewport_size({'width':1440,'height':1000})
        page.locator('#theme').click();check('Dark mode toggle',page.locator('html').get_attribute('data-theme')=='dark')
        for name in PAGES:
            navigate(page,name)
            check('Dark '+name+' no render error',page.get_by_text('We could not render this view').count()==0)
        navigate(page,'products');page.screenshot(path=str(ROOT/'docs/screenshots/products-dark.png'),full_page=True)
        page.locator('#theme').click()
        navigate(page,'customers')
        cohort=page.evaluate('(()=>{const c=window.FUZZY_APP.cohortData();return {cohorts:c.cohorts,ages:c.ages,z:c.z,sizes:Array.from(c.sizes,([k,v])=>[k,v.size])};})()')
        check('Cohort month-zero equals one',all(abs(row[0]-1)<1e-12 for row in cohort['z']))
        check('Future cohort cells are blank',cohort['z'][-1][1] is None)
        check('Observed cohort zeros are zero',any(v==0 for row in cohort['z'] for v in row))
        check('Cohort denominator matches buyers',sum(v for k,v in cohort['sizes'])==31696)
        row=con.execute("select count(distinct o.user_id) from fct_orders o join dim_customers d using(user_id) where date_trunc('month',d.first_order_at)=date '2012-03-01' and date_trunc('month',o.created_at)=date '2012-04-01'").fetchone()[0]
        check('Cohort age-one SQL reconciliation',abs(cohort['z'][0][1]-row/cohort['sizes'][0][1])<1e-12)
        page.screenshot(path=str(ROOT/'docs/screenshots/customers.png'),full_page=True)
        navigate(page,'funnel');check('Notebook page-popularity analysis included',page.get_by_role('heading',name='Page popularity',exact=True).count()==1)
        page.screenshot(path=str(ROOT/'docs/screenshots/funnel.png'),full_page=True)
        navigate(page,'overview')
        page.locator('#from').fill('2014-01-01');page.locator('#to').fill('2014-12-31');page.locator('#source').select_option('gsearch');page.locator('#device').select_option('mobile');page.locator('#filters button').click()
        compare(page,con,"where order_date between date '2014-01-01' and date '2014-12-31' and channel='gsearch' and device_type='mobile'","where session_date between date '2014-01-01' and date '2014-12-31' and channel='gsearch' and device_type='mobile'")
        page.reload();page.wait_for_function('window.FUZZY_READY===true')
        check('URL retains date/source/device filters',page.evaluate("window.FUZZY_APP.state.from==='2014-01-01'&&window.FUZZY_APP.state.source==='gsearch'&&window.FUZZY_APP.state.device==='mobile'"))
        for name in PAGES:
            navigate(page,name);check('Filtered '+name+' works',page.get_by_text('We could not render this view').count()==0)
        navigate(page,'ask')
        expected=['summary','sources','products','refunds','devices','repeat','trend']
        for index,kind in enumerate(expected):
            btn=page.locator('[data-question]').nth(index);q=btn.get_attribute('data-question')
            check('Question template: '+kind,page.evaluate('(q)=>window.FUZZY_APP.routeQuestion(q)',q)==kind)
            btn.click();check('Question answer and SQL '+kind,page.locator('#answer details').count()==1)
            sql=page.locator('#answer code').text_content();check('Assistant SQL executes '+kind,len(con.execute(sql).fetchall())>0)
        page.locator('#question').fill('What is ROAS and net profit?');page.locator('#question-form button').click()
        check('Unsupported metrics rejected',page.get_by_role('heading',name='Outside the supported scope').count()==1)
        page.locator('[data-question]').nth(0).click();page.screenshot(path=str(ROOT/'docs/screenshots/ask-your-data.png'),full_page=True)
        navigate(page,'explorer')
        n=page.evaluate('window.FUZZY_APP.state.exports.length')
        with page.expect_download() as dl:page.locator('#export').click()
        destination=Path(temp)/'orders.csv';dl.value.save_as(destination)
        with destination.open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
        check('Explorer CSV exports all matching rows',len(rows)==n and n>20)
        first=page.locator('#view tbody tr').first.locator('td').first.inner_text();page.locator('#next').click()
        check('Explorer pagination changes rows',page.locator('#view tbody tr').first.locator('td').first.inner_text()!=first)
        page.locator('[data-sort=order_id]').click()
        ids=[int(v) for v in page.locator('#view tbody tr td:first-child').all_inner_texts()]
        check('Explorer ascending sort',ids==sorted(ids))
        page.locator('#order-search').fill('not-a-real-order-xyz')
        check('Search empty state',page.get_by_role('heading',name='No orders match that search').count()==1)
        page.locator('#order-search').fill('2014-06')
        check('Search narrows and exports selection',page.evaluate('window.FUZZY_APP.state.exports.length')>0 and page.evaluate("window.FUZZY_APP.state.exports.every(r=>r.order_date.startsWith('2014-06'))"))
        page.locator('#from').fill('2014-12-31');page.locator('#to').fill('2014-01-01');page.locator('#filters button').click()
        check('Invalid date order is rejected',page.locator('#filter-error').is_visible())
        page.locator('#reset').click();navigate(page,'overview')
        page.locator('#from').fill('2012-03-19');page.locator('#to').fill('2012-03-19');page.locator('#source').select_option('socialbook');page.locator('#filters button').click()
        check('No-data filter state',page.get_by_role('heading',name='No records match those filters').count()==1)
        page.locator('#empty-reset').click();compare(page,con)
        page.set_viewport_size({'width':375,'height':667});page.locator('#menu').click()
        check('Mobile menu opens',page.locator('#menu').get_attribute('aria-expanded')=='true')
        last=page.locator('nav [data-page=about]');last.scroll_into_view_if_needed();last.click()
        check('All mobile navigation reachable',page.locator('#title').inner_text()=='Metric definitions')
        check('Mobile menu closes on navigation',page.locator('#menu').get_attribute('aria-expanded')=='false')
        page.locator('#menu').click();page.keyboard.press('Escape');check('Escape dismisses menu',page.locator('#menu').get_attribute('aria-expanded')=='false')
        page.set_viewport_size({'width':1440,'height':1000});navigate(page,'overview')
        page.emulate_media(media='print');check('Print layout retains heading',page.locator('h1').is_visible());page.emulate_media(media='screen')
        check('No uncaught JavaScript errors',not errors)
        browser.close()
    con.close()
    report={'browser':'Chromium (headless, Linux)','modes':['local file://, light','local file://, dark'],'viewports':['1440x1000','375x812','375x667 menu'],'external_https_blocked':True,'checks_passed':len(checks),'uncaught_errors':errors,'checks':checks}
    (ROOT/'docs/BROWSER_QA_RESULTS.json').write_text(json.dumps(report,indent=2))
    print(f'{len(checks)} browser checks passed with external HTTPS blocked.')
if __name__=='__main__':
    (ROOT/'docs/screenshots').mkdir(parents=True,exist_ok=True)
    main()
