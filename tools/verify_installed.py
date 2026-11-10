"""Run against the installed wheel, outside the source checkout."""
import sys,json,tempfile,subprocess,pathlib
cs=json.load(open(sys.argv[1],encoding='utf-8'))
from stablelab import __version__
assert __version__=='0.1.0'
count=0
with tempfile.TemporaryDirectory() as t:
 for i,c in enumerate(cs):
  inp=pathlib.Path(t)/'input.json';out=pathlib.Path(t)/'evidence.json';inp.write_text(json.dumps(c['program']))
  for cmd in [[sys.executable,'-m','stablelab'],['stablelab']]:
   report=json.loads(subprocess.check_output(cmd+['analyze',str(inp)]));out.write_text(json.dumps(report));checked=json.loads(subprocess.check_output(cmd+['verify',str(out)]));assert checked['valid'];count+=1
   report['stable_masks'].append(999);out.write_text(json.dumps(report));bad=subprocess.run(cmd+['verify',str(out)],capture_output=True);assert bad.returncode==2
print('installed',__version__,'controls',len(cs),'entry-point pairs',count,'and forged reports rejected')
