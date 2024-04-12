from moviepy.video.io.VideoFileClip import VideoFileClip


video_path = "name of the video file here.mp4"
clip = VideoFileClip(video_path)

# Define start and end times (in seconds) for the scene.
start_time = 37*60 + 20  # 37 min 20 sec
end_time = 38*60 + 31  # 38 min 31 sec

cut_clip = clip.subclip(start_time, end_time)

output_path = "cut_scene.mp4"
cut_clip.write_videofile(output_path, codec="libx264", fps=clip.fps)
