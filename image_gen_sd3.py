import torch
from diffusers import StableDiffusion3Pipeline

pipe = StableDiffusion3Pipeline.from_pretrained("stabilityai/stable-diffusion-3-medium-diffusers", torch_dtype=torch.float16)
pipe.enable_model_cpu_offload()

image = pipe(
    prompt="Richly detailed, vibrant colors, fantasy world drawing, exaggerated features, from a perfect 90-degree side profile, with full body of the subject and a pure white background of elder woman warrior dressed in well used battle armor, carrying a magical sword ",
    negative_prompt="shadow, ground, mutations",
    num_inference_steps=28,
    height=1024,
    width=1024,
    guidance_scale=7.0,
).images[0]

image.save("sd3_hello_world.png")