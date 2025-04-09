from moviepy import VideoFileClip, TextClip, CompositeVideoClip
import openai


# Function to get AI-generated fun fact
def generate_fun_fact():
    openai.api_key = "your_openai_api_key"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Give me a random fun fact."}]
    )
    return response["choices"][0]["message"]["content"]


# Load video
video = VideoFileClip("your_video.mp4")

# Get a fun fact from AI
fun_fact = generate_fun_fact()

# Create text overlay
text = TextClip(fun_fact, fontsize=50, color='white', size=(video.w * 0.8, None), method='caption')
text = text.set_position(("center", "bottom")).set_duration(video.duration)

# Overlay text on video
final = CompositeVideoClip([video, text])
final.write_videofile("output.mp4", fps=24)
