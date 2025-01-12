import os
import re
from moviepy.video.io.VideoFileClip import VideoFileClip

# Helper function to convert time format in VTT to seconds
def time_to_seconds(time_str):
    h, m, s = map(float, time_str.replace(',', '.').split(':'))
    return h * 3600 + m * 60 + s

# Create output directories if they don't exist
os.makedirs('videos_who', exist_ok=True)
os.makedirs('labels_who', exist_ok=True)

# Get all video files in the 'videos' folder
video_files = [f for f in os.listdir('.') if f.endswith('.mp4')]
total_videos = len(video_files)

# Process each video file
for video_idx, video_file in enumerate(video_files, start=1):
    print(f"Processing video {video_idx} of {total_videos}: {video_file}")
    
    # Corresponding .vtt file
    vtt_file = os.path.join('.', os.path.splitext(video_file)[0] + '.vtt')
    if not os.path.exists(vtt_file):
        print(f"Warning: No corresponding .vtt file found for {video_file}. Skipping...")
        continue
    
    # Read the .vtt file
    with open(vtt_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Extract timestamps and captions from the .vtt file
    timestamps = []
    captions = []
    for i, line in enumerate(lines):
        match = re.match(r"(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})", line)
        if match:
            start_time, end_time = match.groups()
            timestamps.append((time_to_seconds(start_time), time_to_seconds(end_time)))
            # The caption is typically on the line after the timestamp
            if i + 1 < len(lines) and lines[i + 1].strip():
                captions.append(lines[i + 1].strip())
    
    # Load the video file
    video_path = os.path.join('.', video_file)
    video_clip = VideoFileClip(video_path)
    
    # Process each timestamp and generate shorter videos and text files
    base_name = os.path.splitext(video_file)[0]
    for idx, (start, end) in enumerate(timestamps):
        # Skip invalid timestamps
        if start >= video_clip.duration or end > video_clip.duration:
            print(f"Skipping invalid timestamp ({start}, {end}) for {video_file}")
            continue

        # Generate short video clip
        short_clip = video_clip.subclip(start, end)
        short_video_name = f"{base_name}_{idx + 1}.mp4"
        short_video_path = os.path.join('videos_who', short_video_name)
        
        # Suppress MoviePy output by setting logger=None
        short_clip.write_videofile(short_video_path, codec="libx264", audio_codec="aac", logger=None)
        
        # Save corresponding caption to a text file
        caption_text = captions[idx] if idx < len(captions) else ""
        text_file_name = f"{base_name}_{idx + 1}.txt"
        text_file_path = os.path.join('labels_who', text_file_name)
        with open(text_file_path, 'w', encoding='utf-8') as text_file:
            text_file.write(caption_text)
    
    # Close the video clip to free resources
    video_clip.close()