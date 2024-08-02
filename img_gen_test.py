from diffusers import StableDiffusionXLPipeline
import torch
import time
import os

start_time = time.time()

torch.backends.cuda.matmul.allow_tf32 = True
image_list = []

def generate_image(num_img, prompt) :
    model_start_time = time.time()
    model_path = ("../models/stable-diffusion/SDXLFaetastic_v24.safetensors")
    pipe = StableDiffusionXLPipeline.from_single_file(model_path, custom_pipeline="low_stable_diffusion", torch_dtype=torch.float16, variant="fp16" ).to("cuda")
    
    pipe.enable_vae_slicing()
    # torch compile not worth the loss in time at batch size of 4
    # pipe.unet = torch.compile(pipe.unet, mode='reduce-overhead', fullgraph=True)    

#__call__ arguements belong here
    


    for x in range(num_img):
        img_start = time.time()
        image = pipe(prompt=prompt,num_inference_steps=50).images[0]

        #image.save(f"/output/{timestr} {lch.generate_monster_desc.monster_size} {lch.generate_monster_desc.monster_color} {lch.generate_monster_desc.monster_type}.png")
        
        
        image = image.save(str(x) + prompt)
        img_time = time.time() - img_start
        img_its = 50/img_time
        print(f"image gen time = {img_time} and {img_its} it/s")
        print(f"Memory after image {x} = {torch.cuda.memory_allocated()}")
        
        image_path = str(os.path.abspath(image))
        image_list.append(image_path)
        del image        
        print(f"Memory after del {torch.cuda.memory_allocated()}")
        print(image_list)
    total_time = time.time() - start_time
    
    print(f"Total Time to generate{x} images = {total_time} ")  

x = 2 
prompt = "A Basilisk"
image = generate_image(x, prompt)
               



