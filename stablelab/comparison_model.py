"""Strict shared comparison request parsing, not a semantic oracle."""
from .model import parse

def parse_comparison(data):
    if not isinstance(data,dict) or set(data)!={'atoms','left','right'}:raise ValueError('Expected atoms, left and right only')
    if not isinstance(data['atoms'],list) or len(data['atoms'])>5:raise ValueError('At most five comparison atoms')
    for side in ('left','right'):
        parse({'atoms':data['atoms'],'rules':data[side]})
        if len(data[side])>24:raise ValueError('At most 24 rules per comparison side')
    return {'atoms':list(data['atoms']),'left':[dict(id=r['id'],head=r['head'],positive=list(r['positive']),negative=list(r['negative'])) for r in data['left']],'right':[dict(id=r['id'],head=r['head'],positive=list(r['positive']),negative=list(r['negative'])) for r in data['right']]}
