<!-- Created: 2026-09-21 22:13:12 +03 -->
# Validation record

Status: design and public starter, not a validated leaderboard. No LLM endpoint was called, no model results were measured, and no human domain expert review was performed.

## Completed technical checks

- 16 unique task/family records; 2 per module; matching rubric keys and weights; 2–4 declared critical criteria.
- 96 planned catalog rows, explicitly split into 16 drafted starter families and 80 unwritten candidates. The proposed 24/72 public/private split is a design target, not an existing private test set.
- Profile task counts: text=12, tools=14, full=16. Three-repeat CSV templates contain 36, 42 and 48 pending records respectively.
- Export of all 42 task/profile combinations checked in temporary directories. Packets contain only their condition-specific prompt, system instruction, selected attachments and hashes; no answer keys or other conditions.
- Numeric references checked for QED cross section, kinematics, Poisson likelihood, MC normalization, covariance, dimuon cutflow and the binned likelihood interval. A separate scientific-review agent independently recomputed the main values. This is AI-assisted verification, not independent human expert validation.
- Dimuon event IDs, cutflow and weighted bins reconstructed from the CSV. Likelihood derivative, q0 and interval endpoints checked against the supplied model.
- All four rendered PNGs visually inspected: tree diagram, loop diagram, occupancy and histogram. An ambiguous disconnected momentum arrow was replaced with an explicit textual routing convention.
- T801 bin-edge and statistical-error definitions made explicit. T802 interval-specific numeric tolerance added before any model evaluation.
- Scoring implementation initially delegated to a routine worker, then reviewed and corrected by the primary coordinator. Regression checks cover absent-profile modules, optional telemetry, pending/infra blocking, failure scoring, duplicate/invalid rows, repeat means, module macro averaging and separate integration scoring.

## Reproduce

From the package root:

```bash
python3 -m unittest discover -s tests -v
```

Observed result: **20 tests passed** using Python 3.14.4. The tests use only the Python standard library. Synthetic all-pass/all-fail score rows exist only inside tests; they are not model results.

## Not completed

- Human HEP/statistics expert review or inter-rater agreement study.
- A frozen 96-family corpus or any private test families.
- Provider adapters, automated model execution, sandbox enforcement, or task-specific automatic execution graders for submitted code.
- Difficulty/discrimination calibration, model comparisons, confidence intervals, cost measurements or coverage experiments.
- Formal JSON Schema validation with a third-party validator; the shipped unittest suite checks the operational task/rubric/profile contract directly.

The score aggregator only summarizes externally verified CSV scores. For code tasks, the external evaluator must still execute candidate programs in an isolated environment and check the documented requirements on additional inputs. Do not mark execution gates as passed solely because text matches the answer key.
