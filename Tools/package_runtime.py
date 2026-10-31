"""Portable package and manual overlay generation, independent of an installer."""
from pathlib import Path
import json,hashlib,zipfile
from package_mod import package
PREFIX='Bladesong/Binaries/Win64/ue4ss/Mods/'
def build(stage,out,repository,license_path,notices_path):
 out=Path(out);out.mkdir(exist_ok=True,parents=True);meta=json.loads((Path(stage)/'mod.json').read_text());id=meta['id'];version=meta['version'];portable=out/f'{id}_{version}_Package.zip';release=package(stage,portable)
 release['repository']=repository;release['download']={'url':repository+f'/releases/download/v{version}/{portable.name}','sha256':hashlib.sha256(portable.read_bytes()).hexdigest()}
 (out/'mod.json').write_text(json.dumps(release,indent=2)+'\n',encoding='utf-8');manual=out/f'{id}_{version}_Runtime.zip'
 with zipfile.ZipFile(portable)as source,zipfile.ZipFile(manual,'w',zipfile.ZIP_DEFLATED)as z:
  for name in source.namelist():
   if name=='mod.json':continue
   if id=='BladesongModFramework'and name.startswith('shared/'):target=PREFIX+'shared/BladesongFramework/'+name[7:]
   elif name.startswith('assets/logicmods/'):target='Bladesong/Content/Paks/LogicMods/'+name[17:]
   else:target=PREFIX+id+'/'+name
   z.writestr(target,source.read(name))
  for name in ['mod.json','bmf-installed.json']:z.writestr(PREFIX+id+'/'+name,json.dumps(release,indent=2)+'\n')
  z.writestr(PREFIX+id+'/deployment.json',json.dumps({'schema_version':1,'owner':'manual','mod_id':id}))
  z.write(license_path,'LICENSE_'+id+'.txt');z.write(notices_path,'THIRD_PARTY_NOTICES_'+id+'.md')
 for path in [portable,manual]:
  with zipfile.ZipFile(path)as z:assert z.testzip()is None
 checksums(out,[portable,manual]);return release

def checksums(out,archives):
 (Path(out)/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n'for p in archives),encoding='utf-8')
