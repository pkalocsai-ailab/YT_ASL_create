import os
from pytube import YouTube

# Path to the .txt file containing YouTube video IDs
video_ids_file = "youtube-asl_youtube_asl_video_ids.txt"

# Directory to save downloaded videos
output_dir = "videos"
os.makedirs(output_dir, exist_ok=True)

# Function to download a video by its ID
def download_video(video_id, output_dir):
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        print(f"Downloading: {yt.title}")
        stream.download(output_path=output_dir)
        print(f"Downloaded: {yt.title}")
    except Exception as e:
        print(f"Failed to download video ID {video_id}: {e}")
        with open("failed_downloads.txt", "a") as log_file:
            log_file.write(f"{video_id}: {e}\n")

# Read video IDs from the file and download each video
with open(video_ids_file, "r") as file:
    video_ids = file.readlines()

for video_id in video_ids:
    video_id = video_id.strip()
    if video_id:
        download_video(video_id, output_dir)

print("All videos processed.")