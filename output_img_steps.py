
from diffusers import StableDiffusionXLPipeline,AutoencoderKL, AutoencoderTiny
import torch
import matplotlib.pyplot as plt
from PIL import Image
TINY_AUTOENCODER = AutoencoderTiny.from_pretrained(
    "madebyollin/taesd", torch_dtype=torch.float16)
TINY_AUTOENCODER.to("cuda")
pipe = StableDiffusionXLPipeline.from_single_file(
    "../models/stable-diffusion/SDXLFaetastic_v24.safetensors", vae = TINY_AUTOENCODER, torch_dtype=torch.float16, variant="fp16", use_safetensors=True
).to("cuda")

prompt = "Astronaut in a jungle, cold color palette, muted colors, detailed, 8k"
# pipe has an arguement callback_on_step_end that accepts a callback function with these arguements
# pipe.num_timestep is a way to access the timestep the generation is on
def callback(pipe, step_index, timestep, callback_kwargs):
    latents = callback_kwargs.get("latents")
    if step_index in [30,40,49]:
        latents = 1 / 0.18215 * latents
        image = TINY_AUTOENCODER.decode(latents).sample[0]
        image = (image / 2 + 0.5).clamp(0, 1)
        image = image.cpu().permute(1, 2, 0).numpy()
        image = pipe.numpy_to_pil(image)[0]
        image.save(f"./imgs/{step_index}.png")
        



    return callback_kwargs

pipe(prompt=prompt, callback_on_step_end=callback)

   # with torch.no_grad():
    #    latents = 1 / 0.18215 * latents
     #   image = pipe.vae.decode(latents).sample
      #  image = (image / 2 + 0.5).clamp(0, 1)
        
       # image = image.cpu().permute(0, 2, 3, 1).float().numpy()
        
       # image = pipe.numpy_to_pil(image)[0]
       # image.save(f"./imgs/{step_index}.png")