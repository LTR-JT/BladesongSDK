from pathlib import Path
import json,zipfile
ROOT=Path(__file__).resolve().parents[1];version=json.loads((ROOT/'SDK/version.json').read_text())['version']
with zipfile.ZipFile(ROOT/f'Releases/BladesongDeveloperSDK_{version}.zip')as z:
 assert z.testzip()is None
 assert not any(name.endswith(('.exe','.dll'))for name in z.namelist())
 for name in ['SDK/mod.schema.json','SDK/framework.d.lua','Tools/package_mod.py','Tools/validate_manifest.py','Tools/package_runtime.py']:assert name in z.namelist()
print('PASS: standalone SDK archive with schema/types/tools and no runtime or manager binaries')
