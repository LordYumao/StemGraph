import torch
from diffusers import FluxPipeline

pipe = FluxPipeline.from_pretrained("<Path to your finetuned Flux.1[Dev] model>", torch_dtype=torch.bfloat16)
pipe.load_lora_weights("./Pretrained_Models/Finetuned Flux.1 [Dev]", weight_name="pytorch_lora_weights.safetensors")
pipe.to("cuda")

prompt = '''Design a clean, 1:1 aspect ratio medical flashcard with anime-style illustrations for four knowledge points. Use a two-layer grid layout (two above, two below). Each subfigure should include a clear title and illustration, emphasizing clarity, readability, and an approachable style. Topic (title) of FlashCard: ’Risk factors for stroke’. Subfigure 1 (top left): ’Smoking’ - Illustration: An anime character holding a cigarette with a worried expression. Include a glowing ’no-smoking’ symbol in the frame for emphasis. Subfigure 2 (top right): ’Personal or family history’ - Illustration: An anime character looking at framed family photos, with a single subtle chart or document visible in the background to highlight family history concerns. Subfigure 3 (bottom left): ’Age’ - Illustration: An elderly anime character with a walking stick and glasses, accompanied by simplified icons like a warning sign near a heart or brain diagram. Subfigure 4 (bottom right): ’Race and ethnicity’ - Illustration: An anime-style group of diverse characters looking at a stroke prevention poster or booklet held by an African American character.'''

image = pipe(
    prompt,
    height=1024,
    width=1024,
    guidance_scale=5,
    num_inference_steps=50,
    max_sequence_length=512,
    generator=torch.Generator("cuda").manual_seed(0)
).images[0]

image.save("image.jpg")


