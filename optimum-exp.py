#This works for loading LoRAs
import time
import torch 
from optimum.nvidia import AutoModelForCausalLM, AutoTokenizer, TextStreamer
from peft import PeftModel, PeftConfig

start_time = time.time()
path_to_model = "C:\AI\models\TextGenerationModels\Speechless-Llama2-Hermes-Orca-Platypus-WizardLM-13B-GPTQ"
path_to_peft = "C:\AI\models\loras\statblock-alpha"
#config = PeftConfig.from_pretrained(path_to_peft)

model = AutoModelForCausalLM.from_pretrained(path_to_model, use_safetensors=True, device_map = "cuda:0" )
print(model.device)

model.load_adapter(path_to_peft)

tokenizer = AutoTokenizer.from_pretrained(path_to_model)

input_context = "Write only a short, punchy, visually decadent description of what a horse sized lynx monster that is black and silver and size large looks like"
input_ids = tokenizer.encode(input_context, return_tensors="pt").to('cuda')
streamer = TextStreamer(tokenizer)
output = model.generate(input_ids, max_length=1024, do_sample = True, temperature=1.0, streamer=streamer)
output_text = tokenizer.decode(output[0], skip_special_tokens=True)
print(output_text)

print(time.time() - start_time)

