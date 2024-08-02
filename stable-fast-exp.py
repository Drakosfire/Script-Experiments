import torch
import time
from diffusers import (StableDiffusionXLPipeline, EulerAncestralDiscreteScheduler)
from sfast.compilers.stable_diffusion_pipeline_compiler import (compile,
                                                                CompilationConfig
                                                                )
total_time = time.time()
def load_model():
    # NOTE:
    # You could change to StableDiffusionXLPipeline to load SDXL model.
    # If the resolution is high (1024x1024),
    # ensure you VRAM is sufficient, especially when you are on Windows or WSL,
    # where the GPU driver may choose to allocate from "shared VRAM" when OOM would occur.
    # Or the performance might regress.
    # from diffusers import StableDiffusionXLPipeline
    # model = StableDiffusionPipeline.from_pretrained(
    #    'runwayml/stable-diffusion-v1-5', torch_dtype=torch.float16)

    # model = StableDiffusionXLPipeline.from_pretrained(
    #     'stabilityai/stable-diffusion-xl-base-1.0', torch_dtype=torch.float16)
    model_path = ("../models/stable-diffusion/SDXLFaetastic_v24.safetensors")
    model = StableDiffusionXLPipeline.from_single_file(
         model_path, torch_dtype=torch.float16)
    model

    model.scheduler = EulerAncestralDiscreteScheduler.from_config(
        model.scheduler.config)
    model.safety_checker = None
    model.to(torch.device('cuda'))
    return model

model_load_start = time.time()
model = load_model()

config = CompilationConfig.Default()

# xformers and Triton are suggested for achieving best performance.
# It might be slow for Triton to generate, compile and fine-tune kernels.
# config.enable_jit_freeze = False
try:
    import xformers
    config.enable_xformers = True
except ImportError:
    print('xformers not installed, skip')
# NOTE:
# When GPU VRAM is insufficient or the architecture is too old, Triton might be slow.
# Disable Triton if you encounter this problem.
try:
    import triton
    config.enable_triton = True
except ImportError:
    print('Triton not installed, skip')
# NOTE:
# CUDA Graph is suggested for small batch sizes and small resolutions to reduce CPU overhead.
# My implementation can handle dynamic shape with increased need for GPU memory.
# But when your GPU VRAM is insufficient or the image resolution is high,
# CUDA Graph could cause less efficient VRAM utilization and slow down the inference,
# especially when on Windows or WSL which has the "shared VRAM" mechanism.
# If you meet problems related to it, you should disable it.
config.enable_cuda_graph = True

compiled_model = compile(model, config)

kwarg_inputs = dict(
    prompt=
    "Fantasy art drawing colossal creature, taller 10 feet. skin rugged, mottled texture shade grayish-blue. Humanoid structure, arms elongated, menacing three-fingered claws. muscular legs digitigrade in form and culminate in hooves. snout dominates features, multiple layers of eyes. eyes resemble human eyes, others are reminiscent of animals Large, bat-like wings protrude back, fluttering occasionally and casting eerie shadows.",
    # NOTE: If you use SDXL, you should use a higher resolution to improve the generation quality.
    height=1024,
    width=1024,
    num_inference_steps=50,
    num_images_per_prompt=1,
)


time_to_load = str(time.time() - model_load_start)
print(f"Time to compile model {time_to_load}")
def gen_img(batch_size):
    for x in range(batch_size):

    # NOTE: Warm it up.
    # The first call will trigger compilation and might be very slow.
    # After the first call, it should be very fast.
        img_time = time.time()
        output_image = compiled_model(**kwarg_inputs).images[0]
        output_image.save(f'test-{x}.png')
        img_gen_time = time.time() - img_time
        img_its = 50/img_gen_time
        print(f"time to gen {img_gen_time} and {img_its} it/s")
    exit_time = time.time() - total_time
    print(f"Total time to load and gen = {exit_time}")
gen_img(6)