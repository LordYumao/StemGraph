import streamlit as st
import numpy as np
from PIL import Image
from glob import glob
import os
from streamlit_shortcuts import add_keyboard_shortcuts
from streamlit_shortcuts import button, add_keyboard_shortcuts
import json
import pandas as pd
# Set page to wide mode by default
st.set_page_config(layout="wide")



########### Important Configuration ###########
All_image_Root = "./Sample_Data"        # the dir where the images are stored
# The expected file structure of All_image_Root is as follows:
# All_image_Root/
#    ├── 1.png
#    ├── 2.png
#    ├── 3.png
#    └── ...

Result_Save_Root = "./Annotation_Results" # the dir where the annotationresults are saved
# The expected file structure of Result_Save_Root is as follows:
# Result_Save_Root/
#    ├── 1/
#    │   └── HumanResult_Accept.txt
#    ├── 2/
#    │   └── HumanResult_Discard.txt
#    └── ...
# Note that after a image is annotated, the result will be saved in the corresponding folder.


os.makedirs(Result_Save_Root, exist_ok=True)

#####################################################

# Use st.cache_data decorator to cache image list to avoid duplicate loading
@st.cache_data
def load_image_list(root_path):
    image_list = glob(os.path.join(root_path, "*.png"))
    # Sort images by numeric ID
    image_list = sorted(image_list, key=lambda x: int(x.split('/')[-1].split('.')[0]))
    return image_list

# Use st.cache_data decorator to cache result file list
@st.cache_data(ttl=60)  # Set 60 seconds cache time, refresh periodically
def load_result_files(root_path):
    all_result_files = glob(os.path.join(root_path, "*/HumanResult_*.txt"))
    return all_result_files

# Use cache function to load data
image_list = load_image_list(All_image_Root)
all_result_files = load_result_files(Result_Save_Root)

# Total number of tasks
total_tasks = len(image_list)

# Current progress (number of processed files)
current_progress = len(all_result_files)

# Statistics for different result types
result_types = {}
for result_file in all_result_files:
    # Extract result type (content after HumanResult_)
    result_type = result_file.split("HumanResult_")[-1].split(".")[0]
    if result_type in result_types:
        result_types[result_type] += 1
    else:
        result_types[result_type] = 1

# Create progress information area
st.sidebar.header("Progress Statistics")
st.sidebar.progress(current_progress / total_tasks)
st.sidebar.write(f"Total Progress: {current_progress}/{total_tasks} ({(current_progress/total_tasks*100):.2f}%)")

# Display statistics for each result type
st.sidebar.subheader("Result Type Statistics")
for result_type, count in result_types.items():
    st.sidebar.write(f"{result_type}: {count} ({(count/current_progress*100):.2f}% of processed tasks)")

# Use session_state to save current index
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0

# Create functions for forward and backward
def next_image():
    if st.session_state.current_index < len(image_list) - 1:
        st.session_state.current_index += 1

def prev_image():
    if st.session_state.current_index > 0:
        st.session_state.current_index -= 1

# Jump to the previous image that has not been manually processed
def up_image():
    current = st.session_state.current_index
    for i in range(current - 1, -1, -1):  # Search backward from current position
        img_path = image_list[i]
        human_result_path = os.path.join(os.path.dirname(img_path), f"HumanResult_*.txt")
        if not glob(human_result_path):  # If HumanResult file is not found
            st.session_state.current_index = i
            break

# Jump to the next image that has not been manually processed
def down_image():
    current = st.session_state.current_index
    for i in range(current + 1, len(image_list)):  # Search forward from current position
        img_path = image_list[i]
        human_result_path = os.path.join(os.path.dirname(img_path), f"HumanResult_*.txt")
        if not glob(human_result_path):  # If HumanResult file is not found
            st.session_state.current_index = i
            break

# Optimize image loading function
@st.cache_data
def load_image(image_path):
    return Image.open(image_path)

# Optimize JSON loading function
@st.cache_data
def load_json_content(file_path):
    with open(file_path, "r") as f:
        content = json.loads(f.read())
    return content

# Load current image when needed
image = load_image(image_list[st.session_state.current_index])
selected_image_path = image_list[st.session_state.current_index]
selected_image_id = selected_image_path.split("/")[-1].split(".")[0]

# Find if there is a HumanResult.txt file
human_result_path = os.path.join(os.path.dirname(selected_image_path), f"HumanResult_*.txt")
human_result_path = glob(human_result_path)
if len(human_result_path) > 0:
    # Extract the type of HumanResult
    human_result = human_result_path[0].split("HumanResult_")[-1].split(".")[0]
else:
    human_result = "None"

# Display current image and index information
if human_result == "None":
    st.write(f"Image {st.session_state.current_index + 1}/{len(image_list)}")
else:
    st.write(f"Image {st.session_state.current_index + 1}/{len(image_list)}, Result: {human_result}")

# # Find the "MedFlashCard_Content.txt" file in the same directory
# med_flash_card_content_path = os.path.join(os.path.dirname(selected_image_path), "MedFlashCard_Content.txt")
# # Find the "MedFlashCard_Content_CN.txt" file in the same directory
# med_flash_card_content_cn_path = os.path.join(os.path.dirname(selected_image_path), "MedFlashCard_Content_CN.txt")

# # Use cache function to load file content
# med_flash_card_content = load_json_content(med_flash_card_content_path)
# med_flash_card_content_cn = load_json_content(med_flash_card_content_cn_path)


HealthCard_content_file = os.path.join(os.path.dirname(selected_image_path), "HealthCard_{}.csv".format(selected_image_id))
HealthCard_content = pd.read_csv(HealthCard_content_file)

# Original_Material,HealthCard,Number_of_Knowledge_Points,T2I_prompt
Original_Material = str(HealthCard_content["Original_Material"].values[0])
HealthCard = json.loads(str(HealthCard_content["HealthCard"].values[0]))
Number_of_Knowledge_Points = str(HealthCard_content["Number_of_Knowledge_Points"].values[0])
T2I_prompt = str(HealthCard_content["T2I_prompt"].values[0])



# Create three column layout
col_1, col_2, col_3 = st.columns([1, 1, 1])

# Display JSON in the first column
with col_1:
    st.title("Original Material")
    st.markdown(Original_Material, unsafe_allow_html=True)

# Display image and navigation buttons in the second column
with col_2:
    # The top row displays the image
    st.title("Health Card")
    st.image(image, use_container_width=True)

    st.divider()
    # The bottom row displays prev button and next button
    button_col1, button_col2, button_col3, button_col4 = st.columns(4)
    with button_col1:
        prev_button = button("←: Previous", "ArrowLeft", on_click=prev_image, key="prev")
    with button_col2:
        next_button = button("→: Next", "ArrowRight", on_click=next_image, key="next")
    with button_col3:   # Up key, jump to the previous image that has not been manually processed
        up_button = button("↑: Last Unprocessed", "ArrowUp", on_click=up_image, key="up")
    with button_col4:   # Down key, jump to the next image that has not been manually processed
        down_button = button("↓: Next Unprocessed", "ArrowDown", on_click=down_image, key="down")
        
    # Add a function for the three new buttons
    def save_human_result(result):
        # Get the image ID from the selected image path
        image_id = selected_image_path.split("/")[-1].split(".")[0]
        
        # Create a directory for this image ID in the Result_Save_Root
        result_dir = os.path.join(Result_Save_Root, image_id)
        os.makedirs(result_dir, exist_ok=True)
        
        # Check if there is an existing HumanResult file
        existing_result_files = glob(os.path.join(result_dir, "HumanResult_*.txt"))
        
        # If it exists, delete it first
        for file in existing_result_files:
            os.remove(file)
            
        # Save the new result file
        result_path = os.path.join(result_dir, f"HumanResult_{result}.txt")
        with open(result_path, "w") as f:
            f.write(result)
        
        # Clear the cache of the result file to update the progress
        load_result_files.clear()
        
        st.success(f"Result saved: {result} to {result_path}")
        # # Optional: Automatically move to the next image
        # next_image()
    st.divider()
    # Create three new buttons
    button_row = st.columns(5)  # Changed to 5 columns to accommodate new buttons
    with button_row[0]:
        accept_button = button("A: Accept", "a", 
                              on_click=lambda: save_human_result("Accept"), 
                              key="accept")
    with button_row[1]:
        regen_button = button("S: Regenerate", "s", 
                             on_click=lambda: save_human_result("Regenerate"), 
                             key="regen")
    with button_row[2]:
        discard_button = button("D: Discard", "d", 
                               on_click=lambda: save_human_result("Discard"), 
                               key="discard")
    with button_row[3]:
        check_button = button("L: Check", "l", 
                             on_click=lambda: save_human_result("NeedCheck"), 
                             key="check")
    with button_row[4]: # prompt need to regenerate
        prompt_button = button("P: PromptModify", "p", 
                             on_click=lambda: save_human_result("PromptModify"), 
                             key="prompt")
        

# The third column displays Chinese CN
with col_3:
    st.title("Health Card Content")
    st.json(HealthCard)
    # Here you can add other related content

# add_keyboard_shortcuts({
#     "ArrowLeft": prev_button,
#     "ArrowRight": next_button,
#     "a": accept_button,
#     "s": regen_button,
#     "d": discard_button,
#     "l": check_button,
#     "p": prompt_button,
#     "ArrowUp": up_button,
#     "ArrowDown": down_button
# })

# Add usage instructions
st.info("Tip: You can use the left and right arrow keys to browse images, press A to accept an image, press S to mark for regeneration, press D to discard content, and press L to mark for further verification")
















