#!/usr/bin/env python3
# Created 2026-09-21 22:13:12 +03; coordinator-reviewed implementation.
"""Aggregate externally verified scores; does not grade LLM answers."""
import argparse, csv, json, math, sys
from collections import defaultdict
REQUIRED = ['model_id','profile','repeat','task_id','status','passed','partial_score','confidence','wall_seconds','input_tokens','output_tokens','cost_usd','grader_id','notes']
PROFILES = {'text','tools','full'}
STATUSES = {'completed','timeout','model_error','infra_error','pending'}
TELEMETRY = ('wall_seconds','input_tokens','output_tokens','cost_usd')

def number(value, name, low=0, high=None, integer=False, optional=False):
    if value is None or str(value).strip() == '':
        if optional: return None
        raise ValueError(f'{name} is required')
    try: x=float(value)
    except (ValueError,TypeError): raise ValueError(f'{name} is not numeric') from None
    if not math.isfinite(x) or x<low or (high is not None and x>high):
        raise ValueError(f'{name} is outside its finite allowed range')
    if integer and not x.is_integer(): raise ValueError(f'{name} must be an integer')
    return int(x) if integer else x

def evaluate(tasks, rows, repeats):
    if not isinstance(repeats,int) or isinstance(repeats,bool) or repeats<1:
        raise ValueError('repeats must be a positive integer')
    taskmap={}
    for t in tasks:
        tid,mid,profiles=t.get('task_id'),t.get('module_id'),t.get('profiles')
        if not isinstance(tid,str) or not tid or not isinstance(mid,str) or not mid or tid in taskmap:
            raise ValueError('invalid or duplicate task/module id')
        if not isinstance(profiles,list) or not profiles or len(set(profiles))!=len(profiles) or not set(profiles)<=PROFILES:
            raise ValueError(f'{tid}: invalid task profiles')
        taskmap[tid]=t
    if not taskmap or not rows: raise ValueError('tasks and result rows must be nonempty')
    for p in PROFILES:
        families=[t.get('family_id',t['task_id']) for t in tasks if p in t['profiles']]
        if len(families)!=len(set(families)):
            raise ValueError('v0.1 requires one task per family/profile; do not double-count variants')
    groups=defaultdict(list)
    for i,row in enumerate(rows,1):
        try:
            if any(c not in row for c in REQUIRED): raise ValueError('missing required columns')
            r=dict(row)
            for name in ('model_id','profile','task_id','status'): r[name]=str(r[name] or '').strip()
            if not r['model_id']: raise ValueError('empty model_id')
            if r['profile'] not in PROFILES or r['status'] not in STATUSES: raise ValueError('unknown profile or status')
            if r['task_id'] not in taskmap: raise ValueError('unknown task_id')
            if r['profile'] not in taskmap[r['task_id']]['profiles']: raise ValueError('task not allowed for profile')
            r['repeat']=number(r['repeat'],'repeat',1,repeats,integer=True)
            required=r['status']=='completed'
            r['passed']=number(r['passed'],'passed',0,1,integer=True,optional=not required)
            r['partial_score']=number(r['partial_score'],'partial_score',0,1,optional=not required)
            if r['status'] in {'timeout','model_error'}:
                if r['passed'] not in (None,0) or r['partial_score'] not in (None,0):
                    raise ValueError('timeout/model_error cannot have nonzero scores')
                r['passed']=0; r['partial_score']=0.
            elif r['status'] in {'infra_error','pending'}:
                if r['passed'] is not None or r['partial_score'] is not None:
                    raise ValueError('pending/infra_error scores must be blank')
            r['confidence']=number(r['confidence'],'confidence',0,1,optional=True)
            for name in TELEMETRY:
                r[name]=number(r[name],name,integer=name in ('input_tokens','output_tokens'),optional=True)
            groups[r['model_id'],r['profile']].append(r)
        except ValueError as e: raise ValueError(f'row {i}: {e}') from None
    output=[]
    for (model,profile),rs in groups.items():
        allowed={tid:t for tid,t in taskmap.items() if profile in t['profiles']}
        expected={(tid,rep) for tid in allowed for rep in range(1,repeats+1)}
        observed={(r['task_id'],r['repeat']) for r in rs}
        if len(observed)!=len(rs): raise ValueError(f'duplicate task/repeat: {model}/{profile}')
        errors=[]
        if expected!=observed: errors.append(f'incomplete grid: {len(expected-observed)} missing trials')
        if any(r['status'] in {'pending','infra_error'} for r in rs): errors.append('pending or infra_error blocks aggregate scores')
        g=dict(model_id=model,profile=profile,status='incomplete' if errors else 'complete',errors=errors,expected_trials=len(expected),observed_trials=len(rs))
        g['totals']={n:dict(value=sum(r[n] for r in rs if r[n] is not None) if any(r[n] is not None for r in rs) else None,observed_count=sum(r[n] is not None for r in rs),expected_count=len(expected)) for n in TELEMETRY}
        if not errors:
            module_rows=defaultdict(list); task_scores={}
            for tid,t in allowed.items():
                trials=[r for r in rs if r['task_id']==tid]
                result=dict(pass_percent=100*sum(r['passed'] for r in trials)/repeats,partial_percent=100*sum(r['partial_score'] for r in trials)/repeats)
                task_scores[tid]=result; module_rows[t['module_id']].append(result)
            mods={m:dict(pass_percent=sum(v['pass_percent'] for v in vs)/len(vs),partial_percent=sum(v['partial_percent'] for v in vs)/len(vs),family_count=len(vs)) for m,vs in module_rows.items()}
            core=[v['pass_percent'] for m,v in mods.items() if m!='M8']
            g.update(task_scores=task_scores,module_scores=mods,core_pass_percent=sum(core)/len(core) if core else None,integration_pass_percent=mods.get('M8',{}).get('pass_percent'),macro_pass_percent=sum(v['pass_percent'] for v in mods.values())/len(mods),macro_partial_percent=sum(v['partial_percent'] for v in mods.values())/len(mods))
            known=[r for r in rs if r['confidence'] is not None]
            g['confidence_brier']=dict(n=len(known),expected_count=len(expected),score=sum((r['confidence']-r['passed'])**2 for r in known)/len(known) if known else None)
        output.append(g)
    return dict(purpose='starter_smoke_test_not_validated_leaderboard',groups=output)

def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--tasks',required=True);ap.add_argument('--results',required=True)
    ap.add_argument('--repeats',type=int,required=True);ap.add_argument('--out',required=True)
    a=ap.parse_args(argv)
    try:
        with open(a.tasks) as f: tasks=[json.loads(x) for x in f if x.strip()]
        with open(a.results,newline='') as f:
            rd=csv.DictReader(f)
            if rd.fieldnames is None or any(c not in rd.fieldnames for c in REQUIRED): raise ValueError('missing required CSV headers')
            rows=list(rd)
        result=evaluate(tasks,rows,a.repeats)
        with open(a.out,'w') as f: json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    except (OSError,ValueError,TypeError) as e:
        print(f'error: {e}',file=sys.stderr);return 2
    return 0
if __name__=='__main__': sys.exit(main())
