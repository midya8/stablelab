"""Strict finite normal-program input. No ASP text parser or implicit atoms."""
import re


def parse(data):
    if not isinstance(data, dict) or set(data) != {'atoms', 'rules'}:
        raise ValueError('Expected atoms and rules only')
    atoms = data['atoms']
    if not isinstance(atoms, list) or len(atoms) > 8 or any(not isinstance(a, str) or not re.fullmatch('[a-z][a-z0-9_]{0,23}', a) for a in atoms) or atoms != sorted(set(atoms)):
        raise ValueError('atoms must be sorted unique names, at most eight')
    rules = data['rules']
    if not isinstance(rules, list) or len(rules) > 32:
        raise ValueError('at most 32 rules')
    ids = set()
    for r in rules:
        if not isinstance(r, dict) or set(r) != {'id', 'head', 'positive', 'negative'}:
            raise ValueError('rule needs id, head, positive, negative only')
        if not isinstance(r['id'], str) or not re.fullmatch('[a-z][a-z0-9_]{0,23}', r['id']) or r['id'] in ids:
            raise ValueError('unique rule ids required')
        ids.add(r['id'])
        if r['head'] is not None and (not isinstance(r['head'], str) or r['head'] not in atoms):
            raise ValueError('head must be a declared atom or null constraint')
        for k in ('positive', 'negative'):
            v = r[k]
            if not isinstance(v, list) or any(not isinstance(a, str) or a not in atoms for a in v) or v != sorted(set(v)):
                raise ValueError('body lists must be sorted unique declared atoms')
    return {'atoms': list(atoms), 'rules': [dict(id=r['id'],head=r['head'],positive=list(r['positive']),negative=list(r['negative'])) for r in rules]}
