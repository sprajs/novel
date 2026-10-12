import argparse,json
from pathlib import Path
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from novel.activation import prepare_reference_model, forward_reference, ResidualSite
from novel.gradients import activation_gradient
from novel.profiles import configure_determinism
from novel.diagnostics import numerical_runtime
parser=argparse.ArgumentParser(description='Bounded diagnostic of FP16 cache drift; no acceptance thresholds change')
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args()
args.output.mkdir(parents=True,exist_ok=False)
configure_determinism()
torch.set_num_threads(5)
snapshot=Path('.cache/models/qwen3_0_6b-c1899de289a04d12100db370d81485cdf75e47ca')
tokenizer=AutoTokenizer.from_pretrained(snapshot,local_files_only=True)
model=prepare_reference_model(AutoModelForCausalLM.from_pretrained(snapshot,local_files_only=True,dtype=torch.float16,attn_implementation='eager').to('cuda:0'))
config=json.loads(Path('configs/cpu-smoke.json').read_text())
prompt=tokenizer.apply_chat_template([{'role':'user','content':config['prompt']}],tokenize=False,add_generation_prompt=True,enable_thinking=False)
ids=tokenizer(prompt,add_special_tokens=False,return_tensors='pt').input_ids.to('cuda:0')
suffix=[tokenizer.encode(t,add_special_tokens=False)[0] for t in (' A',' B',' A')]
report={'model':'qwen3_0_6b','runtime':numerical_runtime(),'conditions':[]}
for reduced in (True,False):
 torch.backends.cuda.matmul.allow_fp16_reduced_precision_reduction=reduced
 item={'allow_fp16_reduced_precision_reduction':reduced,'steps':[]}
 with torch.no_grad():
  full=forward_reference(model,ids).logits
  item['exact_forward_repeat']=torch.equal(full,forward_reference(model,ids).logits)
  past=model(ids,attention_mask=torch.ones_like(ids),position_ids=torch.arange(ids.shape[1],device=ids.device)[None],cache_position=torch.arange(ids.shape[1],device=ids.device),use_cache=True,logits_to_keep=1).past_key_values
  extended=ids
  for token in suffix:
   length=extended.shape[1]
   current=torch.tensor([[token]],device=ids.device)
   extended=torch.cat((extended,current),dim=1)
   cached=model(current,past_key_values=past,attention_mask=torch.ones_like(extended),position_ids=torch.tensor([[length]],device=ids.device),cache_position=torch.tensor([length],device=ids.device),use_cache=True,logits_to_keep=1)
   past=cached.past_key_values
   reference=forward_reference(model,extended,last_logits_only=True).logits
   item['steps'].append({'max_abs_error':float((reference.float()-cached.logits.float()).abs().max()),'mismatches':int((~torch.isclose(reference,cached.logits,atol=.02,rtol=.002)).sum()),'top1_match':bool(torch.equal(reference.argmax(-1),cached.logits.argmax(-1)))})
  del cached,past
 objective=full[0,-1].topk(2).indices.tolist()
 gradient=activation_gradient(model,ids,ResidualSite(14,(ids.shape[1]-1,)),*objective)
 item['gradient_l2']=float(gradient.gradient.float().norm())
 item['gradient_finite']=bool(torch.isfinite(gradient.gradient).all())
 report['conditions'].append(item)
(args.output/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report['conditions'],indent=2))
