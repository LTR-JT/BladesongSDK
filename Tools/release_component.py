from pathlib import Path
import argparse,json
ROOT=Path(__file__).resolve().parents[1];p=argparse.ArgumentParser();p.add_argument('tag');a=p.parse_args()
version=json.loads((ROOT/'SDK/version.json').read_text())['version'];names=[f'BladesongDeveloperSDK_{version}.zip']
assert a.tag=='v'+version,'Tag must match this repository component version'
for name in names:
 path=ROOT/'Releases'/name;assert path.is_file();print(path)
