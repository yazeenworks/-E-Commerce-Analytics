"""Launch the already-built offline dashboard; rebuilding is optional."""
from pathlib import Path
import argparse,os,subprocess,sys,webbrowser
ROOT=Path(__file__).resolve().parent
def main():
    parser=argparse.ArgumentParser(description='Fuzzy Factory Commerce Intelligence')
    parser.add_argument('--rebuild',action='store_true',help='Reload CSVs, run dbt models/tests, publish exports')
    parser.add_argument('--test',action='store_true',help='Run Python regression tests')
    parser.add_argument('--no-open',action='store_true',help='Do not launch browser')
    args=parser.parse_args()
    if args.rebuild:
        import importlib.util
        missing=[m for m in ['duckdb','pandas','dbt','plotly'] if importlib.util.find_spec(m) is None]
        if missing:
            print('Optional rebuild needs dependencies: python -m pip install -r requirements.txt')
            return 1
        env=os.environ.copy();env['FUZZY_DB_PATH']=str(ROOT/'data/warehouse/fuzzy.duckdb')
        subprocess.run([sys.executable,str(ROOT/'src/ingest.py')],cwd=ROOT,check=True)
        subprocess.run([sys.executable,'-c','from dbt.cli.main import cli; cli()','build','--profiles-dir','.'],cwd=ROOT/'dbt_project',env=env,check=True)
        subprocess.run([sys.executable,str(ROOT/'src/export.py')],cwd=ROOT,check=True)
    if args.test:
        subprocess.run([sys.executable,'-m','pytest','tests/test_warehouse.py','-q'],cwd=ROOT,check=True)
    file=ROOT/'dashboard/fuzzy-factory.html'
    if args.no_open: print('Dashboard ready:',file)
    else:
        print('Opening the prebuilt dashboard. No installed packages are needed for normal viewing.')
        if not webbrowser.open(file.as_uri()):print('Open this file in a browser:',file)
    return 0
if __name__=='__main__':
    try:sys.exit(main())
    except subprocess.CalledProcessError as e:
        print('Build/test failed. Review the error above. Existing dashboard files remain available.')
        sys.exit(e.returncode)
