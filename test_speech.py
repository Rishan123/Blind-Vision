from gtts import gTTS
import os

text = "Hello. I am Google Text to Speech"
language = 'en'
sp = gTTS(text=text, lang=language, slow=False)
sp.save('/home/pi/tf/test.mp3')
os.system('omxplayer /home/pi/tf/test.mp3')