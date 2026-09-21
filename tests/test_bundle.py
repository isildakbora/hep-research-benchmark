# Created 2026-09-21 22:13:12 +03.
import csv
import json
import math
import tempfile
import unittest
from pathlib import Path
from scripts.export_task import export
from scripts.score_results import evaluate, REQUIRED

ROOT=Path(__file__).resolve().parents[1]
TASKS=[json.loads(s) for s in (ROOT/'public/tasks.jsonl').read_text().splitlines()]
KEYS={x['task_id']:x for x in [json.loads(s) for s in (ROOT/'evaluator/answer_key.jsonl').read_text().splitlines()]}

class BundleTests(unittest.TestCase):
    def test_task_rubric_contract(self):
        self.assertEqual(len(TASKS),16)
        self.assertEqual(len({t['family_id'] for t in TASKS}),16)
        for t in TASKS:
            rubric=KEYS[t['task_id']]['rubric']
            self.assertEqual(sum(c['weight'] for c in rubric),1)
            self.assertEqual(t['critical_requirements'],[c['description'] for c in rubric if c['critical']])
            self.assertTrue(2<=sum(c['critical'] for c in rubric)<=4)
    def test_catalog_does_not_claim_96_completed(self):
        with (ROOT/'catalog_96.csv').open() as f: rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),96)
        self.assertEqual(sum(r['status']=='draft_starter' for r in rows),16)
        self.assertEqual(sum(r['proposed_split']=='public_development' for r in rows),24)
    def test_profile_complete_grid_and_missing(self):
        for profile,count in [('text',12),('tools',14),('full',16)]:
            tasks=[t for t in TASKS if profile in t['profiles']]
            self.assertEqual(len(tasks),count)
            rows=[]
            for rep in range(1,4):
                for t in tasks:
                    r={k:'' for k in REQUIRED}
                    r.update(model_id='SYNTHETIC_UNIT_TEST',profile=profile,repeat=str(rep),task_id=t['task_id'],status='completed',passed='1',partial_score='1')
                    rows.append(r)
            g=evaluate(TASKS,rows,3)['groups'][0]
            self.assertEqual(g['core_pass_percent'],100)
            self.assertEqual(g['expected_trials'],count*3)
            self.assertEqual(evaluate(TASKS,rows[:-1],3)['groups'][0]['status'],'incomplete')
    def test_every_model_packet_excludes_keys_and_other_conditions(self):
        with tempfile.TemporaryDirectory() as temp:
            for t in TASKS:
                for p in t['profiles']:
                    dst=export(t['task_id'],p,Path(temp)/p/t['task_id'])
                    condition={**t,**t.get('profile_overrides',{}).get(p,{})}
                    files={str(x.relative_to(dst)) for x in dst.rglob('*') if x.is_file()}
                    self.assertEqual(files,{'TASK.md','SYSTEM.txt','packet_manifest.json',*condition['attachments']})
                    self.assertIn(condition['prompt'],(dst/'TASK.md').read_text())
            with self.assertRaises(ValueError):export('T301','text',Path(temp)/'invalid')
            with self.assertRaises(ValueError):export('T101','text',Path(temp)/'text/T101')
    def test_templates_blank_are_incomplete(self):
        for p in ['text','tools','full']:
            with (ROOT/'templates'/f'results_{p}.csv').open() as f: rows=list(csv.DictReader(f))
            self.assertEqual(evaluate(TASKS,rows,3)['groups'][0]['status'],'incomplete')
    def test_dimuon_reference_from_fixture(self):
        with (ROOT/'public/assets/dimuons.csv').open() as f: raw=list(csv.DictReader(f))
        cut=[len(raw)];data=raw
        for pred in [lambda r:int(r['q1'])*int(r['q2'])<0,lambda r:min(float(r['pt1']),float(r['pt2']))>=20,lambda r:max(abs(float(r['eta1'])),abs(float(r['eta2'])))<2.4]:
            data=[r for r in data if pred(r)];cut.append(len(data))
        def mass(r):return math.sqrt(2*float(r['pt1'])*float(r['pt2'])*(math.cosh(float(r['eta1'])-float(r['eta2']))-math.cos(float(r['phi1'])-float(r['phi2']))))
        data=[r for r in data if 60<=mass(r)<120];cut.append(len(data))
        ref=KEYS['T801']['reference'];self.assertEqual(cut,ref['cutflow']);self.assertEqual([r['event_id'] for r in data],ref['event_ids'])
        sums=[0.,0.];squares=[0.,0.]
        for r in data:
            i=0 if mass(r)<90 else 1;w=float(r['weight']);sums[i]+=w;squares[i]+=w*w
        self.assertEqual(sums,ref['sumw']);self.assertEqual(squares,ref['sumw2'])
    def test_likelihood_reference_and_endpoint_tolerance(self):
        d=json.loads((ROOT/'public/assets/counting_model.json').read_text())
        n,b,s=d['observed'],d['background'],d['signal_at_mu1']
        def ll(mu):return sum(ni*math.log(bi+mu*si)-(bi+mu*si) for ni,bi,si in zip(n,b,s))
        ref=KEYS['T802']['reference'];mu=ref['mu_hat']
        self.assertAlmostEqual(sum(si*(ni/(bi+mu*si)-1) for ni,bi,si in zip(n,b,s)),0)
        self.assertAlmostEqual(2*(ll(mu)-ll(0)),ref['q0'])
        for end in ref['delta_nll2_1_interval']:self.assertAlmostEqual(2*(ll(mu)-ll(end)),1,places=8)
        tol=KEYS['T802']['field_tolerances']['delta_nll2_1_interval']
        for val,truth in zip([.027,2.09],ref['delta_nll2_1_interval']):self.assertLessEqual(abs(val-truth),tol['atol']+tol['rtol']*abs(truth))
    def test_numeric_cross_checks(self):
        self.assertAlmostEqual(KEYS['T202']['reference']['sigma_10GeV_pb'],4*math.pi/(137**2*3*100)*3.89379e8)
        self.assertAlmostEqual(KEYS['T501']['reference']['q0'],2*(30*math.log(1.5)-10))
        self.assertAlmostEqual(KEYS['T502']['reference']['total_uncertainty'],math.sqrt((.2**2)*6000+16**2+80**2))
        r=[2,-2];Cinv=[[4/7,-3/7],[-3/7,4/7]]
        self.assertAlmostEqual(sum(r[i]*Cinv[i][j]*r[j] for i in range(2) for j in range(2)),KEYS['T602']['reference']['chi2_full'])

if __name__=='__main__':unittest.main()
