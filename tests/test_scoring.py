# Created 2026-09-21 22:13:12 +03. Regression tests for score integrity.
import unittest
from scripts.score_results import evaluate, REQUIRED

def task(t,m='M1',profiles=None):
 return dict(task_id=t,module_id=m,profiles=profiles or ['text','tools','full'])
def row(t,rep=1,passed=1,part=1,status='completed',profile='text'):
 r={k:'' for k in REQUIRED};r.update(model_id='m',profile=profile,repeat=str(rep),task_id=t,status=status,passed=str(passed) if passed is not None else '',partial_score=str(part) if part is not None else '')
 return r
class ScoreTests(unittest.TestCase):
 def test_macro_equal_modules(self):
  g=evaluate([task('a'),task('b'),task('c','M2')],[row('a'),row('b',passed=0,part=0),row('c')],1)['groups'][0]
  self.assertEqual(g['core_pass_percent'],75)
 def test_excluded_modules_not_zeros(self):
  g=evaluate([task('a'),task('b','M3',['full']),task('c','M8',['tools','full'])],[row('a')],1)['groups'][0]
  self.assertEqual(g['core_pass_percent'],100);self.assertIsNone(g['integration_pass_percent']);self.assertEqual(set(g['module_scores']),{'M1'})
 def test_integration_separate(self):
  g=evaluate([task('a'),task('b','M8')],[row('a'),row('b',passed=0,part=.5)],1)['groups'][0]
  self.assertEqual(g['core_pass_percent'],100);self.assertEqual(g['integration_pass_percent'],0);self.assertEqual(g['macro_pass_percent'],50)
 def test_missing_grid(self):
  g=evaluate([task('a')],[row('a')],2)['groups'][0];self.assertEqual(g['status'],'incomplete');self.assertNotIn('core_pass_percent',g)
 def test_pending_infra_blank(self):
  for s in ['pending','infra_error']:
   g=evaluate([task('a')],[row('a',status=s,passed=None,part=None)],1)['groups'][0]
   self.assertEqual(g['status'],'incomplete');self.assertNotIn('confidence_brier',g)
 def test_failures_zero(self):
  for s in ['timeout','model_error']:
   g=evaluate([task('a')],[row('a',status=s,passed=None,part=None)],1)['groups'][0]
   self.assertEqual(g['core_pass_percent'],0)
   with self.assertRaises(ValueError):evaluate([task('a')],[row('a',status=s)],1)
 def test_duplicate(self):
  with self.assertRaises(ValueError):evaluate([task('a')],[row('a'),row('a')],1)
 def test_invalid_inputs(self):
  for r in [row('x'),row('a',profile='bad'),row('a',rep=4),row('a',part='nan'),row('a',passed=.5)]:
   with self.assertRaises(ValueError):evaluate([task('a')],[r],3)
  with self.assertRaises(ValueError):evaluate([task('a',profiles=['full'])],[row('a')],1)
 def test_repeat_mean(self):
  g=evaluate([task('a')],[row('a',1),row('a',2,passed=0,part=0)],2)['groups'][0]
  self.assertEqual(g['core_pass_percent'],50)
 def test_optional_telemetry(self):
  g=evaluate([task('a')],[row('a')],1)['groups'][0]
  self.assertIsNone(g['totals']['cost_usd']['value']);self.assertEqual(g['totals']['cost_usd']['observed_count'],0)
 def test_brier(self):
  r=row('a');r['confidence']='0.8';g=evaluate([task('a')],[r],1)['groups'][0]
  self.assertAlmostEqual(g['confidence_brier']['score'],.04)
 def test_family_duplicates(self):
  a=task('a');b=task('b');a['family_id']=b['family_id']='same'
  with self.assertRaises(ValueError):evaluate([a,b],[row('a'),row('b')],1)
if __name__=='__main__':unittest.main()
