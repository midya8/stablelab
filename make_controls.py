"""Developed synthetic normal programs. Historical ideas credited in SOURCES."""
import json
from pathlib import Path

def rule(id,head,pos=(),neg=()):return dict(id=id,head=head,positive=sorted(pos),negative=sorted(neg))
def case(title,description,atoms,rules):return dict(title=title,description=description,program=dict(atoms=sorted(atoms),rules=rules))
controls=[
case('Supported. Minimal. Still not stable.','Every classical model contains p and q. Their circular support survives, but the self-default rule vanishes in that candidate reduct. No atom can start a derivation.', ['p','q'],[rule('default','p',neg=['p']),rule('from_q','p',['q']),rule('from_p','q',['p'])]),
case('Circular support is not grounding.','Both empty and full sets are supported models of a positive cycle. Only the empty candidate equals its reduct least closure.', ['p','q'],[rule('from_q','p',['q']),rule('from_p','q',['p'])]),
case('Two stable alternatives.','An even default-negation cycle has two stable models. Neither atom is skeptical, although each is brave.', ['p','q'],[rule('choose_p','p',neg=['q']),rule('choose_q','q',neg=['p'])]),
case('One odd cycle. No stable model.','p follows from its own absence. The empty candidate derives p; candidate p removes its only rule. Query answers are null, not a claim of evidence through vacuity.', ['p'],[rule('odd','p',neg=['p'])]),
case('A constraint filters a choice.','The even default cycle initially permits p or q. A headless constraint forbids q and leaves p as the unique stable model.', ['p','q'],[rule('choose_p','p',neg=['q']),rule('choose_q','q',neg=['p']),rule('forbid_q',None,['q'])]),
case('A fact grounds the whole chain.','A fact starts a cycle and a longer positive derivation. Every atom has a finite proof height, unlike the unseeded positive cycle.', ['p','q','r','s'],[rule('seed','p'),rule('pq','q',['p']),rule('qp','p',['q']),rule('qr','r',['q']),rule('rs','s',['r'])]),
case('Default conclusions can retract.','A declared bird normally flies; an exception is a fact. Absence of abnormal is tested in the candidate, not treated as classical negation.', ['abnormal','bird','flies'],[rule('bird_fact','bird'),rule('exception','abnormal'),rule('default_flight','flies',['bird'],['abnormal'])]),
case('No atoms. One empty stable model.','The empty program has exactly the empty stable model. This differs from the headless empty-body constraint, which has no model at all.', [],[]),
case('An empty constraint forbids everything.','A constraint with no body is always violated. Even the empty interpretation is not a model.', [],[rule('impossible',None)]),
case('Sixteen stable selections.','Four independent even default cycles give sixteen stable models among all 256 candidates. All reduct, support and unfounded-set evidence is still complete.',list('abcdefgh'),[rule('pick_'+a,a,neg=[b]) for a,b in [('a','b'),('b','a'),('c','d'),('d','c'),('e','f'),('f','e'),('g','h'),('h','g')]])]
if __name__=='__main__':
 root=Path(__file__).parent/'docs';root.mkdir(exist_ok=True);(root/'controls.json').write_text(json.dumps(controls,indent=2)+'\n');(root/'example.json').write_text(json.dumps(controls[0]['program'],indent=2)+'\n')
