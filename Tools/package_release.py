from pathlib import Path
import json,zipfile,hashlib
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'Releases';OUT.mkdir(exist_ok=True);version=json.loads((ROOT/'SDK/version.json').read_text())['version'];archive=OUT/f'BladesongDeveloperSDK_{version}.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED)as z:
 for folder in ['SDK','Documentation','Examples','Tools']:
  for path in (ROOT/folder).rglob('*'):
   if path.is_file()and not any(part in ['__pycache__','Data']for part in path.parts)and path.suffix not in ['.exe','.dll','.pyc']:z.write(path,path.relative_to(ROOT).as_posix())
 z.write(ROOT/'LICENSE','LICENSE');z.write(ROOT/'UPSTREAM.md','UPSTREAM.md')
with zipfile.ZipFile(archive)as z:assert z.testzip()is None
(OUT/'SHA256SUMS.txt').write_text(hashlib.sha256(archive.read_bytes()).hexdigest()+'  '+archive.name+'\n');print('Prepared standalone SDK archive:',archive)
