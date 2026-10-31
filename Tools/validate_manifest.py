"""Validate the published mod.json schema subset using only Python's standard library.

This validator deliberately rejects unknown schema keywords rather than silently
claiming support for the entire JSON Schema specification.
"""
from pathlib import Path
import argparse,json,re
from urllib.parse import urlparse
KEYS={'$schema','$id','title','description','type','required','properties','additionalProperties','items','enum','const','pattern','format','minLength','maxLength','minItems','maxItems','minimum','maximum'}
def check(value,schema,path='$'):
 unknown=set(schema)-KEYS
 if unknown:raise ValueError('Unsupported schema keywords: '+str(unknown))
 kind=schema.get('type');types={'object':dict,'array':list,'string':str,'integer':int,'boolean':bool,'number':(int,float)}
 if kind and (not isinstance(value,types[kind])or(kind in ('integer','number')and isinstance(value,bool))):raise ValueError(path+': expected '+kind)
 if 'const'in schema and value!=schema['const']:raise ValueError(path+': unexpected constant')
 if 'enum'in schema and value not in schema['enum']:raise ValueError(path+': invalid enum')
 if isinstance(value,dict):
  for key in schema.get('required',[]):
   if key not in value:raise ValueError(path+': missing '+key)
  props=schema.get('properties',{})
  for key,item in value.items():
   if key in props:check(item,props[key],path+'.'+key)
   elif schema.get('additionalProperties')is False:raise ValueError(path+': unknown '+key)
   elif isinstance(schema.get('additionalProperties'),dict):check(item,schema['additionalProperties'],path+'.'+key)
 if isinstance(value,list):
  if not schema.get('minItems',0)<=len(value)<=schema.get('maxItems',10**9):raise ValueError(path+': array bounds')
  for i,item in enumerate(value):check(item,schema.get('items',{}),path+'['+str(i)+']')
 if isinstance(value,str):
  if not schema.get('minLength',0)<=len(value)<=schema.get('maxLength',10**9):raise ValueError(path+': text bounds')
  if 'pattern'in schema and not re.search(schema['pattern'],value):raise ValueError(path+': invalid pattern')
  if schema.get('format')=='uri'and not urlparse(value).scheme:raise ValueError(path+': URI required')
 if isinstance(value,(int,float))and not isinstance(value,bool):
  if not schema.get('minimum',-float('inf'))<=value<=schema.get('maximum',float('inf')):raise ValueError(path+': numeric bounds')
def validate_manifest(value,schema=None):
 schema=schema or json.loads((Path(__file__).resolve().parents[1]/'SDK/mod.schema.json').read_text(encoding='utf-8'))
 check(value,schema)
 for field in ['dependencies','optional_dependencies']:
  for id,version in value.get(field,{}).items():
   if not re.fullmatch('[A-Za-z0-9_-]{1,64}',id)or not version.strip():raise ValueError('Invalid dependency identifier/range')
 if 'files'in value:
  from package_mod import validate
  validate(value)
 return value
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('manifest',nargs='+');args=parser.parse_args()
 for path in args.manifest:validate_manifest(json.loads(Path(path).read_text(encoding='utf-8')));print('Valid:',path)
