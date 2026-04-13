import os
import shutil
import csv
from pathlib import Path

def convert_dataset():
    """
    Convert HealthCards dataset from folder structure to flat structure.
    
    Source: Data/HealthCards_Dataset
    - Structure: {id}/image.png, {id}/prompt.txt
    
    Target: Data/HealthCards_Processed
    - Structure: {id}.png, {id}.txt, metadata.csv
    """
    
    # Define paths (relative to script location)
    source_dir = Path("Data/HealthCards_Dataset")
    target_dir = Path("Data/HealthCards_Processed")
    
    # Create target directory if it doesn't exist
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # List to store metadata
    metadata_entries = []
    
    # Get all subdirectories (numbered folders)
    subdirs = [d for d in source_dir.iterdir() if d.is_dir()]
    
    # Sort by numeric value
    subdirs.sort(key=lambda x: int(x.name))
    
    print(f"Found {len(subdirs)} folders to process...")
    
    # Process each folder
    processed_count = 0
    skipped_count = 0
    
    for folder in subdirs:
        folder_id = folder.name
        
        # Define source paths
        source_image = folder / "image.png"
        source_prompt = folder / "prompt.txt"
        
        # Check if required files exist
        if not source_image.exists():
            print(f"Warning: Missing image.png in folder {folder_id}")
            skipped_count += 1
            continue
            
        if not source_prompt.exists():
            print(f"Warning: Missing prompt.txt in folder {folder_id}")
            skipped_count += 1
            continue
        
        # Define target paths
        target_image = target_dir / f"{folder_id}.png"
        target_prompt = target_dir / f"{folder_id}.txt"
        
        # Copy image file
        shutil.copy2(source_image, target_image)
        
        # Copy prompt file
        shutil.copy2(source_prompt, target_prompt)
        
        # Read prompt text for metadata
        with open(source_prompt, 'r', encoding='utf-8') as f:
            prompt_text = f.read().strip()
        
        # Add to metadata
        metadata_entries.append({
            'image': f"{folder_id}.png",
            'prompt': prompt_text
        })
        
        processed_count += 1
        
        if processed_count % 100 == 0:
            print(f"Processed {processed_count} files...")
    
    # Write metadata.csv
    metadata_path = target_dir / "metadata.csv"
    with open(metadata_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['image', 'prompt']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(metadata_entries)
    
    print(f"\n{'='*60}")
    print(f"Conversion completed!")
    print(f"Processed: {processed_count} files")
    print(f"Skipped: {skipped_count} files")
    print(f"Output directory: {target_dir}")
    print(f"Metadata file: {metadata_path}")
    print(f"{'='*60}")

if __name__ == "__main__":
    convert_dataset()

