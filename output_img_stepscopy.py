import io
from diffusers import StableDiffusionXLPipeline, LMSDiscreteScheduler, AutoencoderTiny, AutoencoderKL
import numpy as np
import torch
from PIL import Image

vae = AutoencoderKL.from_pretrained("sdxl_vae/", torch_dtype=torch.float16)
pipe = StableDiffusionXLPipeline.from_single_file(
    "../models/stable-diffusion/SDXLFaetastic_v24.safetensors", torch_dtype=torch.float16,
).to("cuda")

scheduler = LMSDiscreteScheduler(
    beta_start=0.00085, beta_end=0.012, beta_schedule="scaled_linear", num_train_timesteps=1000)


TINY_AUTOENCODER = AutoencoderTiny.from_pretrained(
    "madebyollin/taesd", torch_dtype=torch.float16)
TINY_AUTOENCODER.to("cuda")


prompt = "A capybara holding a sword whilst wearing a knights costuem,"


def to_png_image(img_np):
    """Convert a numpy array to PNG format image."""
    img = Image.fromarray((img_np * 255).astype(np.uint8))
    buf = io.BytesIO()
    img.save(buf, format='png', compress_level=0)
    return buf.getvalue()


def decode_tensors(pipe, step, timestep, callback_kwargs):
    latents = callback_kwargs["latents"]
    img = TINY_AUTOENCODER.decode(latents)
    img_np = img[0].squeeze(0).permute(
        1, 2, 0).cpu().detach().numpy().astype('float32')
    img_np = np.clip((img_np + 1) / 2.0, 0, 1)
    buf = to_png_image(img_np)
    with open(f"./imgs/{step}.png", 'wb') as f:
        f.write(buf)

    return callback_kwargs


image = pipe(
    height=1024,
    width=1024,
    prompt=prompt,
    negative_prompt="",
    guidance_scale=7.5,
    num_inference_steps=20,
    callback_on_step_end=decode_tensors,
    
).images[0]

image.save("./imgs/final.png")