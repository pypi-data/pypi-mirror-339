import os
import pandas as pd
from moviepy import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip, ColorClip
from gtts import gTTS
from importlib.resources import files

def main():
    # Find asset paths inside the package
    asset_root = files("fact_blitz.assets")
    csv_path = str(asset_root / "fun_facts_10000.csv")
    video_path = str(asset_root / "video_backgrounds" / "fixed_video.mp4")
    
    output_dir = os.path.join(os.getcwd(), "processed_videos")
    os.makedirs(output_dir, exist_ok=True)

    # Load video and data
    video = VideoFileClip(video_path)
    fun_fact = pd.read_csv(csv_path)['Fun Fact'].iloc[0]

    # Font
    font_path = "C:/Windows/Fonts/comic.ttf"  # You can try 'comicbd.ttf' or another rounder font too

    # Text
    text = TextClip(
        text=fun_fact,
        font=font_path,
        font_size=60,
        color='white',
        size=(int(video.w * 0.6), None),
        method='caption'
    ).with_duration(video.duration)

    # Background rectangle
    background = ColorClip(
        size=(text.w + 40, text.h + 20),
        color=(0, 0, 0)
    ).with_opacity(0.5).with_duration(video.duration)

    # Position
    text_x = (video.w - text.w) // 2
    text_y = (video.h - text.h) // 2
    text = text.with_position((text_x, text_y))
    background = background.with_position((text_x - 20, text_y - 10))

    # Combine background + text
    text_with_bg = CompositeVideoClip([background, text], size=video.size)

    # Voiceover
    tts = gTTS(text=fun_fact, lang="en")
    voiceover_path = os.path.join(output_dir, "fun_fact.mp3")
    tts.save(voiceover_path)
    voiceover = AudioFileClip(voiceover_path)

    # Final video
    final_video = CompositeVideoClip([video, text_with_bg])
    final_video = final_video.with_audio(voiceover)

    final_path = os.path.join(output_dir, "processed_video.mp4")
    final_video.write_videofile(final_path, fps=24)

if __name__ == "__main__":
    main()
