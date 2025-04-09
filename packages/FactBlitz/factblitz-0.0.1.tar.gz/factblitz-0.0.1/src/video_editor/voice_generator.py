from gtts import gTTS
from overlay import generate_fun_fact

# Generate speech from the fun fact
fun_fact = generate_fun_fact()
tts = gTTS(text=fun_fact, lang="en")
tts.save("fun_fact.mp3")
