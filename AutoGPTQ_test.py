#This works pretty fast, 12.94 s 
import time
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

start_time = time.time()
model_id = "models/Speechless-Llama2-Hermes-Orca-Platypus-WizardLM-13B-GPTQ"
#peft_model_id = "C:\AI\models\loras\statblock-alpha\\adapter_model.bin"

llm = AutoModelForCausalLM.from_pretrained(model_id, device_map = "cuda:0",use_safetensors=True)
tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=True)
#llm.load_adapter(peft_model_id)

prompt = ("Write only a short, punchy, visually decadent description of what a horse sized lynx monster that is black and silver and size large looks like")
prompt_template =f'''{prompt}
'''
print("*** Pipeline:")
pipe = pipeline(
    "text-generation",
    model=llm,
    tokenizer=tokenizer,
    max_new_tokens=512,
    do_sample=True,
    temperature=0.7,
    top_p=0.95,
    top_k=40,
    repetition_penalty=1.1
)

print(pipe(prompt_template)[0]['generated_text'])
#model.load_adapter(peft_model_id).to("cuda")
print(time.time() - start_time)