import json
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, concatenate_videoclips

# === Charger les données ===
with open("video1_tags.json", "r") as f:
    data = json.load(f)

video_path = data["file"]
segments = data["segments"]

# === Charger la vidéo originale ===
video = VideoFileClip(video_path)

final_clips = []

def format_ranking(ranking):
    return "\n".join([f"{r['position']}. {r['athlete']}" for r in ranking])


for seg in segments:
    start = seg["start"]
    end = seg["end"]

    # Cutting the segment
    clip = video.subclip(start, end)

    # Overlay text: tags + ranking
    text_lines = []

    if "tags" in seg:
        text_lines.append("Tags : " + ", ".join(seg["tags"]))

    if "ranking" in seg:
        text_lines.append("\nRanking:\n" + format_ranking(seg["ranking"]))

    text = "\n".join(text_lines)

    txt_clip = TextClip(
        text,
        fontsize=32,
        color="white",
        stroke_color="black",
        stroke_width=2,
        font="DejaVu-Sans"
    ).set_position(("center", "bottom")).set_duration(clip.duration)

    # Composite video (video + overlay)
    final = CompositeVideoClip([clip, txt_clip])
    final_clips.append(final)

# === Concaténer les clips ===
montage = concatenate_videoclips(final_clips)

# === Exporter ===
montage.write_videofile(
    "output_final.mp4", 
    codec="libx264", 
    fps=30,
    audio_codec="aac"
)

print("🎉 Montage terminé : output_final.mp4")
