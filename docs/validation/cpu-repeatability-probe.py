import argparse
from dataclasses import asdict
import hashlib
import json
import os
from pathlib import Path
import time

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from novel.activation import (AdditiveIntervention, IdentityIntervention, ResidualSite, SemanticAnchor,
                              forward_reference, prepare_reference_model)
from novel.artifacts import environment_record, sha256_file
from novel.models import model_entry, snapshot_path, verify_snapshot
from novel.profiles import ProfileRequest, configure_determinism, inspect_hardware, resolve_profile, validate_environment
from novel.runner import load_config

parser=argparse.ArgumentParser()
parser.add_argument('--threads',type=int,required=True)
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args()
assert args.threads in (1,5)
assert not args.output.exists()
started=time.perf_counter()
config=load_config(Path('docs/validation/cpu-repeatability-original-config.json'))
config['threads']=args.threads
entry=model_entry(Path('configs/models.json'),'qwen3_0_6b')
request=ProfileRequest(gradient=True)
determinism=configure_determinism()
hardware=inspect_hardware()
resolved=resolve_profile(request,hardware,entry)
validate_environment(resolved)
snapshot=snapshot_path(Path('.cache/models'),'qwen3_0_6b',entry)
hashes=verify_snapshot(snapshot,entry)
torch.set_num_threads(config['threads']);torch.manual_seed(config['seeds']['fixture'])
tokenizer=AutoTokenizer.from_pretrained(snapshot,local_files_only=True,trust_remote_code=False)
model=AutoModelForCausalLM.from_pretrained(snapshot,local_files_only=True,trust_remote_code=False,
                                        use_safetensors=True,dtype=torch.float32,attn_implementation='eager')
model.to('cpu');prepare_reference_model(model)
rendered=tokenizer.apply_chat_template([{'role':'user','content':config['prompt']}],tokenize=False,add_generation_prompt=True,enable_thinking=False)
ids=tokenizer(rendered,add_special_tokens=False,return_tensors='pt').input_ids
site=ResidualSite(config['layer'],(ids.shape[1]-1,))
anchor=SemanticAnchor('assistant_response_boundary',ids.shape[1]-1,tuple(ids[0,-1:].tolist()),tuple(ids[0].tolist()),'Same pinned mechanics prompt as original failure')

def digest(tensor):
 return hashlib.sha256(tensor.detach().cpu().contiguous().view(torch.uint8).numpy().tobytes()).hexdigest()

def state():
 return {'cpu_rng_sha256':digest(torch.get_rng_state()),
         'buffer_sha256':{name:digest(b) for name,b in model.named_buffers()},
         'parameter_versions':{name:p._version for name,p in model.named_parameters()},
         'parameter_grads_absent':all(p.grad is None for p in model.parameters()),
         'hook_counts':[len(layer._forward_hooks) for layer in model.model.layers]}

report={'schema_version':1,'source_commit':environment_record()['git_commit'],'environment':environment_record(),
        'original_failure':'20261011T121557Z-92d81a5e278a','config':config,'rendered_prompt':rendered,
        'input_ids':ids.tolist(),'site':asdict(site),'snapshot_files_sha256':hashes,'determinism':determinism,
        'torch_build':torch.__config__.show(),'parallel_info':torch.__config__.parallel_info(),
        'runtime':{'threads':torch.get_num_threads(),'interop_threads':torch.get_num_interop_threads(),
                   'mkldnn_enabled':torch.backends.mkldnn.enabled,'matmul_precision':torch.get_float32_matmul_precision(),
                   'environment_controls':{k:os.environ.get(k) for k in ('MKL_NUM_THREADS','MKL_DYNAMIC','MKL_CBWR','OMP_NUM_THREADS','OMP_DYNAMIC','CUBLAS_WORKSPACE_CONFIG')}},
        'initial_state':state(),'comparisons':[],
        'scope':'Bounded replay of the original clean->capture ordering. No warmup, sampling, cache or backward occurs.'}
base=None
for name,kwargs in [('clean0',{}),('capture0',{'capture_site':site}),('clean1',{}),('capture1',{'capture_site':site}),
                    ('identity',{'intervention':IdentityIntervention(site)}),
                    ('zero',{'intervention':AdditiveIntervention(site,torch.ones(model.config.hidden_size),anchor,strength=0)}),('clean2',{})]:
 before=state()
 result=forward_reference(model,ids,**kwargs)
 after=state()
 if base is None: base=result.logits
 diff=(result.logits-base).abs()
 values,indices=diff.flatten().topk(8)
 row={'condition':name,'logits_sha256':digest(result.logits),'max_abs_error':float(diff.max()),
      'mismatch_count':int(torch.count_nonzero(diff)), 'exact_equal':bool(torch.equal(base,result.logits)),
      'state_unchanged':before==after,'matches_initial_state':after==report['initial_state']}
 if row['mismatch_count']:
  row['largest_errors']=[{'flat_index':i,'baseline':float(base.flatten()[i]),'observed':float(result.logits.flatten()[i]),'abs_error':float(v)} for v,i in zip(values.tolist(),indices.tolist())]
 report['comparisons'].append(row)
report['status']='PASS' if all(r['exact_equal'] and r['state_unchanged'] and r['matches_initial_state'] for r in report['comparisons']) else 'FAIL'
report['wall_seconds']=time.perf_counter()-started
args.output.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
print(json.dumps({'report':str(args.output),'status':report['status'],'threads':args.threads,'errors':[r['max_abs_error'] for r in report['comparisons']]}),flush=True)
