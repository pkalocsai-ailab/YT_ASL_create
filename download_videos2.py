import os
import subprocess

# Path to the .txt file containing YouTube video IDs
video_ids_file = "youtube-asl_youtube_asl_video_ids.txt"
output_dir = "videos"
os.makedirs(output_dir, exist_ok=True)

# Function to download a video using yt-dlp
def download_video(video_id, output_dir):
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        command = [
            "yt-dlp",
            "-o", f"{output_dir}/%(title)s.%(ext)s",
            url
        ]
        subprocess.run(command, check=True)
        print(f"Downloaded: {url}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to download video ID {video_id}: {e}")
        with open("failed_downloads.txt", "a") as log_file:
            log_file.write(f"{video_id}: {e}\n")

# Read and process the video IDs
with open(video_ids_file, "r") as file:
    video_ids = file.readlines()

for video_id in video_ids:
    video_id = video_id.strip()
    if video_id:
        download_video(video_id, output_dir)

print("All videos processed.")