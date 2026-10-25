from pathlib import Path
import duckdb
ROOT=Path(__file__).resolve().parents[1]
def main():
    (ROOT/'data/warehouse').mkdir(parents=True,exist_ok=True)
    with duckdb.connect(str(ROOT/'data/warehouse/fuzzy.duckdb')) as con:
        con.execute('create schema if not exists raw')
        for name in ['orders','order_items','order_item_refunds','products','website_sessions','website_pageviews']:
            source=str(ROOT/'data/raw'/f'{name}.csv').replace("'","''")
            con.execute(f"create or replace table raw.{name} as select * from read_csv_auto('{source}',nullstr='NULL')")
            print(name,con.execute(f'select count(*) from raw.{name}').fetchone()[0])
if __name__=='__main__':main()
