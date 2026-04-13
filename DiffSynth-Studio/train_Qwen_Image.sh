accelerate launch examples/qwen_image/model_training/train.py \
  --dataset_base_path ../Data/HealthCards_Processed \
  --dataset_metadata_path ../Data/HealthCards_Processed/metadata.csv \
  --max_pixels 1048576 \
  --dataset_repeat 2 \
  --model_id_with_origin_paths "Qwen/Qwen-Image:transformer/diffusion_pytorch_model*.safetensors,Qwen/Qwen-Image:text_encoder/model*.safetensors,Qwen/Qwen-Image:vae/diffusion_pytorch_model.safetensors" \
  --learning_rate 1e-4 \
  --num_epochs 5 \
  --remove_prefix_in_ckpt "pipe.dit." \
  --output_path "./finetuned_models/Qwen-Image_lora_r128" \
  --lora_base_model "dit" \
  --lora_target_modules "to_q,to_k,to_v,add_q_proj,add_k_proj,add_v_proj,to_out.0,to_add_out,img_mlp.net.2,img_mod.1,txt_mlp.net.2,txt_mod.1" \
  --lora_rank 128 \
  --use_gradient_checkpointing \
  --dataset_num_workers 8 \
  --find_unused_parameters

