from diffusers import (StableDiffusionXLPipeline)                   
from diffusers.utils import load_image
import torch
import datetime
from cog import BasePredictor, Input, Path 
import gc

torch.backends.cuda.matmul.allow_tf32 = True

model_path = "/media/drakosfire/Shared/models/stable-diffusion/card-generator-v1/card-generator-v1.safetensors"
lora_path = "/media/drakosfire/Shared/models/stable-diffusion/card-generator-v1/blank-card-template-5.safetensors"
detail_lora_path = "/media/drakosfire/Shared/models/stable-diffusion/card-generator-v1/add-detail-xl.safetensors"
card_pre_prompt = " blank magic card,high resolution, detailed intricate high quality border, textbox, high quality detailed magnum opus drawing of a "
negative_prompts = "text, words, numbers, letters"

user_input_template = "/media/drakosfire/Shared/models/stable-diffusion/card-generator-v1/test_img.png"
class Predictor():

    def setup(self) -> None:
       #Load model once, seperately from inference call.
        print(f"Memory before model load {torch.cuda.memory_allocated()}") 
        self.pipe = StableDiffusionXLPipeline.from_single_file(model_path,
                                                        custom_pipeline="low_stable_diffusion",                                                       
                                                            torch_dtype=torch.float16, 
                                                            variant="fp16").to("cuda")
        print(f"Memory after model load {torch.cuda.memory_allocated()}") 
        self.pipe.enable_vae_slicing()
        print(f"Memory after vase_slicing {torch.cuda.memory_allocated()}") 

    def predict(
    self,
    item: str = Input(description="A DnD Item", default= "A Flaming Sword of Ice"), 
    sd_prompt : str = Input(description="Generated Stable Diffusion Prompt", default=" A sword hilt with a line of flame in front of a pitch black night of monsters"),
    num_images: int = Input(description="Number of images to generate", default = 4 )    
    ) -> Path:
        
        """Run a single prediction on the model based on the prompt.

        Args:
            prompt (str): Description of the image to generate.

        Returns:
            Path: The path to the saved image file.
        """

        if not item:
            raise ValueError("Prompt cannot be empty.")
        prompt = (card_pre_prompt + item  + ' ' + sd_prompt)
        print(prompt)
        init_image = load_image(user_input_template).convert("RGB")
        print(init_image)
        print(type(init_image))
        image_list = []
        image_list.append(init_image)

        while num_images > 0:
            image = self.pipe(prompt=prompt,
                    strength = .9,
                    guidance_scale = 5,
                    image= image_list,
                    negative_prompt = negative_prompts,
                    num_inference_steps=40,
                    height = 1024, width = 768).images[0]
            num_images = num_images -1

            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"output_{timestamp}.png"
            image_path = Path(filename)
            image.save(image_path)
            num_images = num_images -1
            print(f"Number of images left : {num_images}")
            del image
            torch.cuda.empty_cache()
            gc.collect()  # Force garbage collection
            print(f"Memory after cleanup {torch.cuda.memory_allocated()}")
            # Delete the image variable to keep VRAM open to load the LLM
            print(f"Memory after del {torch.cuda.memory_allocated()}")

caller = Predictor()
caller.setup()
prompt = f"{card_pre_prompt} A detailed illustration of a mystical DnD sword glowing with magical energy"
sd_prompt = "A golden ring with a malevolvent golden glow infused with lightning anf red fire"
output_path = caller.predict(item = prompt,sd_prompt = sd_prompt, num_images =2 )