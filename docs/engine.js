/* Bounded finite normal programs. Browser reports need Python verification. */
export function parse(data){
 const exact=(o,keys)=>o!==null&&typeof o==='object'&&!Array.isArray(o)&&Object.keys(o).sort().join('|')===keys.sort().join('|');
 if(!exact(data,['atoms','rules']))throw Error('Expected atoms and rules only');
 const names=x=>Array.isArray(x)&&x.every(a=>typeof a==='string'&&/^[a-z][a-z0-9_]{0,23}$/.test(a))&&JSON.stringify(x)===JSON.stringify([...new Set(x)].sort());
 const {atoms,rules}=data;if(!names(atoms)||atoms.length>8)throw Error('atoms must be sorted unique names, at most eight');
 if(!Array.isArray(rules)||rules.length>32)throw Error('at most 32 rules');
 const ids=new Set();for(const r of rules){
  if(!exact(r,['id','head','positive','negative'])||typeof r.id!=='string'||!/^[a-z][a-z0-9_]{0,23}$/.test(r.id)||ids.has(r.id))throw Error('unique rule ids and exact fields required');ids.add(r.id);
  if(r.head!==null&&!atoms.includes(r.head))throw Error('head must be a declared atom or null constraint');
  for(const key of ['positive','negative'])if(!names(r[key])||r[key].some(a=>!atoms.includes(a)))throw Error('body lists must be sorted unique declared atoms');
 }
 return JSON.parse(JSON.stringify(data));
}
export function analyze(data){
 const program=parse(data),{atoms,rules}=program,sets=Array.from({length:2**atoms.length},(_,mask)=>new Set(atoms.filter((_,i)=>mask&(1<<i))));
 const subset=(a,b)=>[...a].every(x=>b.has(x)),sorted=s=>[...s].sort();
 const candidates=sets.map((m,mask)=>{
  const rows=rules.map(r=>{const missing_positive=r.positive.filter(a=>!m.has(a)),present_negative=r.negative.filter(a=>m.has(a)),body_true=!missing_positive.length&&!present_negative.length;return {id:r.id,missing_positive,present_negative,body_true,satisfied:!body_true||m.has(r.head)}});
  const kept=rules.filter((r,i)=>!rows[i].present_negative.length),closure=new Set(),closure_rounds=[];
  while(true){const ready=kept.filter(r=>r.head!==null&&r.positive.every(a=>closure.has(a))),new_atoms=sorted(new Set(ready.map(r=>r.head).filter(a=>!closure.has(a))));closure_rounds.push({before:sorted(closure),ready_rules:ready.map(r=>r.id),new_atoms});if(!new_atoms.length)break;new_atoms.forEach(a=>closure.add(a));}
  const closure_violated_constraints=kept.filter(r=>r.head===null&&r.positive.every(a=>closure.has(a))).map(r=>r.id),supports=sorted(m).map(atom=>({atom,rules:rules.filter((r,i)=>r.head===atom&&rows[i].body_true).map(r=>r.id)}));
  const unfounded_subsets=[];sets.forEach((u,mask)=>{if(!u.size||!subset(u,m))return;const relevant=rules.map((r,i)=>[r,rows[i]]).filter(([r])=>u.has(r.head));if(relevant.some(([r,row])=>row.body_true&&!r.positive.some(a=>u.has(a))))return;unfounded_subsets.push({mask,atoms:sorted(u),obligations:relevant.map(([r,row])=>({rule:r.id,missing_positive:row.missing_positive,present_negative:row.present_negative,internal_positive:r.positive.filter(a=>u.has(a))}))});});
  const model=rows.every(r=>r.satisfied);return {mask,atoms:sorted(m),rules:rows,reduct_rules:kept.map(r=>({id:r.id,head:r.head,positive:r.positive})),closure_rounds,least_reduct_closure:sorted(closure),closure_violated_constraints,missing_from_candidate:sorted(new Set([...closure].filter(a=>!m.has(a)))),ungrounded_candidate_atoms:sorted(new Set([...m].filter(a=>!closure.has(a)))),supports,unfounded_subsets,model,supported:model&&supports.every(s=>s.rules.length>0),stable:model&&subset(m,closure)&&subset(closure,m)&&!closure_violated_constraints.length};
 });
 candidates.forEach((r,i)=>{r.proper_subset_models=candidates.filter((s,j)=>s.model&&sets[j].size<sets[i].size&&subset(sets[j],sets[i])).map(s=>s.mask);r.minimal_model=r.model&&!r.proper_subset_models.length;});
 const stable=candidates.filter(r=>r.stable);
 return {schema:'stablelab-evidence-v1',program,candidates,model_masks:candidates.filter(r=>r.model).map(r=>r.mask),supported_masks:candidates.filter(r=>r.supported).map(r=>r.mask),minimal_model_masks:candidates.filter(r=>r.minimal_model).map(r=>r.mask),stable_masks:stable.map(r=>r.mask),queries:atoms.map(atom=>({atom,brave:stable.length?stable.some(r=>r.atoms.includes(atom)):null,skeptical:stable.length?stable.every(r=>r.atoms.includes(atom)):null,stable_with:stable.filter(r=>r.atoms.includes(atom)).map(r=>r.mask),stable_without:stable.filter(r=>!r.atoms.includes(atom)).map(r=>r.mask)}))};
}
