import argparse,gc,json,time
from pathlib import Path
import torch
from safetensors.torch import save_file
from transformers import AutoModelForCausalLM,AutoTokenizer
from novel.activation import prepare_reference_model,forward_reference,ResidualSite,IdentityIntervention,AdditiveIntervention,SemanticAnchor
from novel.generation import generate_reference
from novel.gradients import activation_gradient
from novel.models import model_entry,snapshot_path,verify_snapshot
from novel.profiles import ProfileRequest,configure_determinism,inspect_hardware,resolve_profile,validate_environment,initialize_device,memory_record
from novel.diagnostics import tensor_sha256,numerical_runtime
parser=argparse.ArgumentParser(description='Uncached operational mechanics, separate from full-profile cache qualification')
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args()
out=args.output;out.mkdir(parents=True,exist_ok=False)
report={'scope':'Uncached GPU operational mechanics only; full profile/cache equivalence gates are separate','status':'FAIL','determinism':configure_determinism(),'cases':[]}
for key in ('qwen3_0_6b','qwen3_1_7b'):
 started=time.perf_counter()
 entry=model_entry(Path('configs/models.json'),key)
 resolved=resolve_profile(ProfileRequest(profile='local-2080ti',model=key),inspect_hardware(),entry)
 validate_environment(resolved);initialize_device(resolved)
 snapshot=snapshot_path(Path('.cache/models'),key,entry);hashes=verify_snapshot(snapshot,entry)
 tokenizer=AutoTokenizer.from_pretrained(snapshot,local_files_only=True,trust_remote_code=False)
 model=prepare_reference_model(AutoModelForCausalLM.from_pretrained(snapshot,local_files_only=True,trust_remote_code=False,use_safetensors=True,dtype=torch.float16,attn_implementation='eager').to('cuda:0'))
 torch.set_num_threads(5)
 prompt=tokenizer.apply_chat_template([{'role':'user','content':'Briefly describe what a bridge connects.'}],tokenize=False,add_generation_prompt=True,enable_thinking=False)
 ids=tokenizer(prompt,return_tensors='pt',add_special_tokens=False).input_ids.to('cuda:0')
 site=ResidualSite(14,(ids.shape[1]-1,));anchor=SemanticAnchor('assistant boundary',ids.shape[1]-1,(int(ids[0,-1]),),tuple(ids[0].tolist()),'Operational mechanics probe')
 baseline=forward_reference(model,ids)
 captured=forward_reference(model,ids,capture_site=site)
 checks={'repeat_exact':torch.equal(baseline.logits,forward_reference(model,ids).logits),'capture_logits_exact':torch.equal(baseline.logits,captured.logits),'capture_finite':bool(torch.isfinite(captured.residual).all()),'identity_exact':torch.equal(baseline.logits,forward_reference(model,ids,intervention=IdentityIntervention(site)).logits),'zero_strength_exact':torch.equal(baseline.logits,forward_reference(model,ids,intervention=AdditiveIntervention(site,torch.ones(model.config.hidden_size,device=ids.device),anchor,strength=0)).logits)}
 patch=forward_reference(model,ids,intervention=AdditiveIntervention(site,torch.ones(model.config.hidden_size,device=ids.device)*.1,anchor))
 checks['nonzero_patch_changes_logits']=not torch.equal(patch.logits,baseline.logits)
 generations=[]
 for _ in range(2):
  generation=generate_reference(model,ids,seed=17,max_new_tokens=8,do_sample=False,eos_token_ids=tuple(entry['token_ids']['generation_eos_token_ids']),use_cache=False)
  generations.append({'ids':list(generation.generated_ids),'text':tokenizer.decode(generation.generated_ids,skip_special_tokens=False),'stop':generation.stop_reason})
 checks['uncached_greedy_repeat']=generations[0]==generations[1]
 gradient_record={'status':'SKIP','reason':'1.7B gradient excluded: full profile planning budget rejected it'}
 if key=='qwen3_0_6b':
  objective=baseline.logits[0,-1].topk(2).indices.tolist()
  gradient=activation_gradient(model,ids,site,*objective)
  gradient_record={'status':'PASS','l2':float(gradient.gradient.float().norm()),'finite':bool(torch.isfinite(gradient.gradient).all())}
  save_file({'gradient':gradient.gradient},str(out/f'{key}-gradient.safetensors'))
  checks['gradient_finite_nonzero']=gradient_record['finite'] and gradient_record['l2']>0
 checks['parameters_frozen_without_gradients']=all(not p.requires_grad and p.grad is None for p in model.parameters())
 checks['hooks_removed']=all(not layer._forward_hooks for layer in model.model.layers)
 save_file({'selected_residual':captured.residual},str(out/f'{key}-residual.safetensors'))
 item={'model':key,'revision':entry['revision'],'snapshot_sha256':hashes,'input_ids':ids[0].tolist(),'checks':checks,'gradient':gradient_record,'generations':generations,'memory':memory_record('cuda:0'),'wall_seconds':time.perf_counter()-started,'logits_sha256':tensor_sha256(baseline.logits),'runtime':numerical_runtime()}
 report['cases'].append(item)
 del model,baseline,captured,patch,ids
 gc.collect();torch.cuda.empty_cache()
report['status']='PASS' if all(all(c['checks'].values()) for c in report['cases']) else 'FAIL'
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':report['status'],'cases':[{'model':c['model'],'checks':c['checks'],'gradient':c['gradient'],'generation':c['generations'][0],'memory':c['memory']} for c in report['cases']]},indent=2))
raise SystemExit(0 if report['status']=='PASS' else 1)
