from pathlib import Path
import argparse,json,subprocess,sys,tempfile
from validate_manifest import validate_manifest
from package_mod import package
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--lua',required=True);p.add_argument('--framework');a=p.parse_args();lua=str(Path(a.lua).resolve())
args=[sys.executable,str(ROOT/'Tools/generate_api.py')]+(['--framework',a.framework]if a.framework else[]);subprocess.run(args,check=True)
current={x['name']:x for x in json.loads((ROOT/'SDK/api-contract.json').read_text())}
for entry in json.loads((ROOT/'SDK/contracts/v1.0.0.json').read_text()):assert current[entry['name']]['parameters']==entry['parameters']and current[entry['name']]['returns']==entry['returns']
for path in list((ROOT/'SDK/templates').rglob('mod.json'))+list((ROOT/'Examples').rglob('mod.json')):
 meta=validate_manifest(json.loads(path.read_text(encoding='utf-8')));assert 'BladesongModManager'not in meta.get('dependencies',{})
with tempfile.TemporaryDirectory(dir=ROOT/'Tests')as tmp:
 tmp=Path(tmp);syntax=tmp/'syntax.lua';syntax.write_text('\n'.join('assert(loadfile('+json.dumps(str(f).replace('\\','/'))+'))'for f in list((ROOT/'SDK/templates').rglob('*.lua'))+list((ROOT/'Examples').rglob('*.lua'))));subprocess.run([lua,str(syntax)],check=True)
 for path in (ROOT/'SDK/templates').glob('*/mod.json'):package(path.parent,tmp/(path.parent.name+'.zip'))
subprocess.run([sys.executable,str(ROOT/'Tools/build_docs.py')],check=True)
print('PASS: SDK schemas, frozen API, Lua templates and standalone packaging; no manager installed or imported')

standalone={'schema_version':1,'id':'StandaloneExample','name':'Standalone example','version':'1.0.0','standalone':True,'files':[]}
validate_manifest(standalone)
standalone.pop('standalone')
try:validate_manifest(standalone)
except ValueError:pass
else:raise AssertionError('SDK mod without API range accepted')
print('PASS: standalone UE4SS manifests need no framework API; ordinary SDK manifests still require it')
