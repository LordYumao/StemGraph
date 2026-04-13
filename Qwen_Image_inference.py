from diffsynth.pipelines.qwen_image import QwenImagePipeline, ModelConfig
import torch


pipe = QwenImagePipeline.from_pretrained(
    torch_dtype=torch.bfloat16,
    device="cuda",
    model_configs=[
        # replace the origin_file_pattern with the *full path* to local qwen model path. Example: /home/aaa/HealthCards/DiffSynth-Studio/models/Qwen/Qwen-Image/transformer/diffusion_pytorch_model*.safetensors
        ModelConfig(model_id="Qwen/Qwen-Image", origin_file_pattern="DiffSynth-Studio/models/Qwen/Qwen-Image/transformer/diffusion_pytorch_model*.safetensors"),
        
        # replace the origin_file_pattern with the *full path* to local qwen model path. Example: /home/aaa/HealthCards/DiffSynth-Studio/models/Qwen/Qwen-Image/text_encoder/model*.safetensors
        ModelConfig(model_id="Qwen/Qwen-Image", origin_file_pattern="DiffSynth-Studio/models/Qwen/Qwen-Image/text_encoder/model*.safetensors"),
        # replace the origin_file_pattern with the *full path* to local qwen model path. Example: /home/aaa/HealthCards/DiffSynth-Studio/models/Qwen/Qwen-Image/vae/diffusion_pytorch_model.safetensors
        ModelConfig(model_id="Qwen/Qwen-Image", origin_file_pattern="<Path to your local qwen model path>/vae/diffusion_pytorch_model.safetensors"),
    ],

    # replace the origin_file_pattern with the *full path* to local qwen model path. Example: /home/aaa/HealthCards/DiffSynth-Studio/models/Qwen/Qwen-Image/tokenizer/
    tokenizer_config=ModelConfig(model_id="Qwen/Qwen-Image", origin_file_pattern="<Path to your local qwen model path>/tokenizer/"),
)
pipe.load_lora(pipe.dit, "./Pretrained_Models/Finetuned Qwen-Image/pytorch_lora_weights.safetensors")
prompt = '''Design a clean, 1:1 aspect ratio medical flashcard with anime-style illustrations for four knowledge points. Use a two-layer grid layout (two above, two below). Each subfigure should include a clear title and illustration, emphasizing clarity, readability, and an approachable style. Topic (title) of FlashCard: ’Risk factors for stroke’. Subfigure 1 (top left): ’Smoking’ - Illustration: An anime character holding a cigarette with a worried expression. Include a glowing ’no-smoking’ symbol in the frame for emphasis. Subfigure 2 (top right): ’Personal or family history’ - Illustration: An anime character looking at framed family photos, with a single subtle chart or document visible in the background to highlight family history concerns. Subfigure 3 (bottom left): ’Age’ - Illustration: An elderly anime character with a walking stick and glasses, accompanied by simplified icons like a warning sign near a heart or brain diagram. Subfigure 4 (bottom right): ’Race and ethnicity’ - Illustration: An anime-style group of diverse characters looking at a stroke prevention poster or booklet held by an African American character.'''
image = pipe(prompt, seed=42, num_inference_steps=50, height=1024, width=1024)
image.save("image.jpg")