import os
import re

# Create the output directory if it doesn't exist
input_folder = 'captions'
output_folder = 'cleaned_captions'
os.makedirs(output_folder, exist_ok=True)

def clean_vtt_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    cleaned_lines = []
    buffer = []  # Temporary storage for timestamp and associated text
    
    for line in lines:
        line = line.strip()
        
        # Check if the line is a timestamp
        if re.match(r'^\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}$', line):
            # If there's content in the buffer, add it to cleaned_lines
            if len(buffer) > 1:  # Ensure both timestamp and valid text exist
                cleaned_lines.extend(buffer)
            buffer = [line]  # Start a new buffer with the current timestamp
        elif line:  # If it's not empty and not a timestamp, process it as text
            # Remove all non-ASCII characters (including emojis and special symbols)
            cleaned_text = re.sub(r'[^\x00-\x7F]+', '', line)  # Remove non-ASCII characters
            
            # Remove any remaining unwanted characters (including underscores)
            cleaned_text = re.sub(r'[^\w\s.,!?\'"-]', '', cleaned_text)  # Strict filtering
            cleaned_text = cleaned_text.replace('_', '')  # Explicitly remove underscores
            
            # Replace multiple punctuation marks with a single one
            cleaned_text = re.sub(r'([.,!?\'"-])\1+', r'\1', cleaned_text)
            
            if cleaned_text.strip():  # If there's still text left after cleaning
                buffer.append(cleaned_text)
        else:
            continue  # Skip empty lines
    
    # Add any remaining valid buffer to cleaned_lines
    if len(buffer) > 1:  # Ensure there is both a timestamp and valid text
        cleaned_lines.extend(buffer)
    
    # Write the cleaned content to the output file
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(cleaned_lines) + '\n')

# List all .vtt files in the input folder and sort them
all_files = sorted([f for f in os.listdir(input_folder) if f.endswith('.vtt')])
total_files = len(all_files)

# Process all files in the directory
for i, filename in enumerate(all_files, start=1):
    input_path = os.path.join(input_folder, filename)
    output_path = os.path.join(output_folder, filename)
    
    print(f"Processing file {i} of {total_files}: {filename}")
    clean_vtt_file(input_path, output_path)

print(f"Processing complete. Cleaned files are saved in '{output_folder}' folder.")
