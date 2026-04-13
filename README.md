# HealthCards: Exploring Text-to-Image Generation as Visual Aids for Healthcare Knowledge Democratizing and Education ([Paper](https://drive.google.com/file/d/1HTkfzPJ2rxYbCNlMKl1QKSzBCNPvg54d/view?usp=sharing))

## Overview

![First Figure](Assets/HealthCards.png)


# Conda Env
```
conda create -n healthcards python=3.11
conda activate healthcards
conda install -c nvidia cuda-toolkit=12.1

pip install -U poetry pip
# install requirement for SimpleTuner
cd SimpleTuner
poetry install 
pip install flash-attn --no-build-isolation  

# install requirement for DiffSynth
cd ../DiffSynth-Studio
pip install -e .
pip install -U transformers
```


# Dataset
The HealthCards dataset can be downloaded via [link](https://drive.google.com/file/d/1BuRWYCHpxL4xH-9px0gkRaUSWp_uU4yb/view?usp=drive_link).

Place  `HealthCards_Dataset.zip` under `./Data`. (You could use gdown to download)
```
mkdir Data
cd ./Data
# gdown https://drive.google.com/uc?id=1BuRWYCHpxL4xH-9px0gkRaUSWp_uU4yb      # if you need to download in cmd (pip install gdown first)
unzip HealthCards_Dataset.zip
```
The data structure should be like:
```
HealthCards_Dataset
├── 1
│   ├── image.png
│   ├── metadata.csv
│   └── prompt.txt
├── 10
│   ├── image.png
│   ├── metadata.csv
│   └── prompt.txt
├── 100
│   ├── image.png
│   ├── metadata.csv
│   └── prompt.txt
├── 1000
│   ├── image.png
│   ├── metadata.csv
│   └── prompt.txt
├── 1001
│   ├── image.png
│   ├── metadata.csv
│   └── prompt.txt
├── 1002
│   ├── image.png
│   ├── metadata.csv
│   └── prompt.txt
├── 1003
│   ├── image.png
│   ├── metadata.csv
│   └── prompt.txt
├── 1004
...
```

## Dataset conversion
Make the dataset structure compatible for `DiffSynth-Studio` and `SimpleTuner`, please run the following script:

```
python dataset_conversion.py 
```

It will generate a processed dataset at `Data/HealthCards_Processed`


# Training
## Flux.1[Dev]
We recommend to download the Flux.1[Dev] model from [Hugging Face](https://huggingface.co/black-forest-labs/FLUX.1-dev) to a local dir first.

```
cd SimpleTuner
# Then modify the `--pretrained_model_name_or_path` in `config/flux/config.json`. Please replace it with your local path of the Flux model.

sh train.sh config/flux
```



## Qwen-Image
```
cd DiffSynth-Studio
sh train_Qwen_Image.sh
```




# Models
- Finetuned `Flux.1[Dev]`: [link](https://drive.google.com/drive/folders/1ZJNU7IyxrLeMKOXEAN4rZE_Y8G4KR1na?usp=sharing)

Besides, we also provide a finetuned `Qwen-Image`: [link](https://drive.google.com/drive/folders/1rXkICQ5gHcqUpjSXuX4q_LZpgxFYWDfJ?usp=sharing)

```
#Place them under `Pretrained_Models`
mkdir Pretrained_Models
cd Pretrained_Models
gdown --folder 1ZJNU7IyxrLeMKOXEAN4rZE_Y8G4KR1na # use gdown to download finetuned Flux.1[Dev]
gdown --folder 1rXkICQ5gHcqUpjSXuX4q_LZpgxFYWDfJ # use gdown to download finetuned Qwen-Image
```

# Inference
Please refer to `Flux_Dev_inference.py` and `Qwen_Image_inference.py`



# Acknowledgements
We express our gratitude to the developers of [SimpleTuner](https://github.com/bghira/SimpleTuner) and [DiffSynth-Studio](https://github.com/modelscope/DiffSynth-Studio)
