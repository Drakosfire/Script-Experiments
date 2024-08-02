import torch 
from torch import autocast
from diffusers import StableDiffusionXLPipeline
from compel import Compel, ReturnedEmbeddingsType
import utilities as u
import time

# Use tf32 instead of fp32 seems to use more sys memory faster
# torch.backends.cuda.matmul.allow_tf32 = True

image_list = []
lora_list = ["None","Ghostly"]
lora_dict = {"None" : "None", "Ghostly" : "models/stable-diffusion/loras/SDXLGhostStyle.safetensors"}
lora_keyword_dict = {"None" : "None","Ghostly" : "Ghostlystyle:1"}
lora = "None"
lora_keyword = str

# Assign path to model to be used and tell torch to be ready for 32 bit
# torch.backends.cuda.matmul.allow_tf32 = True
model_path = ("models/stable-diffusion/SDXLFaetastic_v20.safetensors")


def pick_lora(self):
    global lora
    print(self)
    lora = lora_dict[self]
    lora_keyword = lora_keyword_dict[self]
    print(f"lora loaded :{lora}")
    print(f"lora keyword : {lora_keyword}")
def check_lora():
    print(lora)

def del_image_list() :
    del image_list 

class img_generator :
    def __init__(self, sd_input, num_img):
        self.sd_input = sd_input
        self.num_img = num_img

    
    def generate_image(self):
        # load model locally with single file, using custom pipeline, in floating point 16 and send to VRAM
        pipeline = StableDiffusionXLPipeline.from_single_file(model_path, custom_pipeline="lpw_stable_diffusion", torch_dtype=torch.float16, variant="fp16" ).to("cuda")
        # Compel is a module that could allow longer than 77 token prompts AND adding weights to specific tokens
        compel = Compel(tokenizer=[pipeline.tokenizer, pipeline.tokenizer_2] , 
                text_encoder=[pipeline.text_encoder, pipeline.text_encoder_2], 
                returned_embeddings_type=ReturnedEmbeddingsType.PENULTIMATE_HIDDEN_STATES_NON_NORMALIZED, 
                requires_pooled=[False, True],
               truncate_long_prompts=False)

        # assign prompt as sd_input
        prompt = self.sd_input
        
        # Not sure what conditioning or pooled means, but it's in the demo code from here https://github.com/damian0815/compel/blob/main/compel-demo-sdxl.ipynb
        negative_prompt = "watermark, text, fastnegative2, blurry, ugly, low quality, worst quality, 3d"
        conditioning, pooled = compel([prompt, negative_prompt])
        print(conditioning.shape, pooled.shape)    
        print(prompt)
        
        for x in range(self.num_img):     
        

            image = pipeline(prompt_embeds=conditioning[0:1], pooled_prompt_embeds=pooled[0:1], 
                        negative_prompt_embeds=conditioning[1:2], negative_pooled_prompt_embeds=pooled[1:2],
                        num_inference_steps=30, width=1024, height=1024).images[0]
            image_name = f"test{x}.png"
            image.save(image_name)
            image_list.append(image_name)
    
        
test_prompt = "A kaiju housefly crashing through a city of frog people"
num_img = 4
test_generate = img_generator(test_prompt, num_img)
test_generate.generate_image()
    

