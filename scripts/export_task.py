#!/usr/bin/env python3
# Created 2026-09-21 22:13:12 +03.
"""Export only one profile-specific model input packet; never exports answer keys."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def export(task_id, profile, destination):
    tasks=[json.loads(s) for s in (ROOT/'public/tasks.jsonl').read_text().splitlines() if s.strip()]
    t=next((t for t in tasks if t['task_id']==task_id),None)
    if t is None or profile not in t['profiles']:
        raise ValueError('unknown task or unsupported task/profile combination')
    out=Path(destination)
    if out.exists() and (not out.is_dir() or any(out.iterdir())):
        raise ValueError('destination must be absent or an empty directory')
    c={**t,**t.get('profile_overrides',{}).get(profile,{})}
    public=(ROOT/'public').resolve()
    sources=[]
    for name in c['attachments']:
        path=(public/name).resolve()
        if not path.is_relative_to(public) or not path.is_file():
            raise ValueError('invalid attachment path')
        sources.append((name,path))
    out.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(ROOT/'public/prompts'/profile/(task_id+'.md'),out/'TASK.md')
    system=(ROOT/'templates/system_prompt.txt').read_text()
    system+='\nSelected profile: '+profile+'. '
    system+=('No model-side tools or execution are allowed. Code may be submitted for external evaluation.' if profile=='text' else 'Local terminal and Python tools are allowed within the recorded run budget. Use only packet files; no internet.')
    (out/'SYSTEM.txt').write_text(system+'\n')
    for name,path in sources:
        dst=out/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,dst)
    files={str(p.relative_to(out)):hashlib.sha256(p.read_bytes()).hexdigest() for p in out.rglob('*') if p.is_file()}
    (out/'packet_manifest.json').write_text(json.dumps(dict(task_id=task_id,profile=profile,budget_class=t['budget_class'],sha256=files),indent=2)+'\n')
    return out

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--task',required=True);p.add_argument('--profile',choices=['text','tools','full'],required=True);p.add_argument('--out',required=True)
    a=p.parse_args()
    try:print(export(a.task,a.profile,a.out))
    except (ValueError,OSError) as e:p.error(str(e))

if __name__=='__main__':main()
